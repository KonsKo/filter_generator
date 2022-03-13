"""Filter auto generator module."""
import json
import os
import sys
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader


COMPARE_OPERATORS = ('gt', 'lt', 'ge', 'le', 'like', 'in')
LOCAL_SOURCE_FILE = 'local_source/local_source.json'


def convert_order_by(order_by: list):
    for inx, ob in enumerate(order_by):
        if ob.startswith('-'):
            order_by[inx] = '{0} desc'.format(
                ob.replace('-', ''),
            )
    return order_by


class FilterAutoGenerator(object):
    """Filter auto generator."""

    current_dir = os.path.dirname(os.path.abspath(__file__))
    filter_template = 'template_filter.txt'
    db_schema_location = 'db.schema'  # it uses for import model

    def __init__(
        self,
        source_file: str,
        load_local: bool,
        destination_dir: Optional[str] = None,
    ):
        """
        Init class instance.

        Args:
            source_file (str): name of source file `.json`
            load_local (bool): load local filter fields
            destination_dir (Optional[str]): directory to save ready files

        """
        self.source_file = source_file
        self.load_local = load_local
        self.destination_dir = destination_dir
        self.filter_source = []
        self.load_filter_source()
        self.datatype_ts_to_python = {
            'String': 'str',
            'Date': 'datetime',
            'Boolean': 'bool',
            'Number': 'int',
            'Array': 'list',
            'Tuple': 'tuple',
        }

    def load_filter_source(self):
        """
        Load source data from file.

        Raises:
            NotImplementedError: if error

        """
        if not self.source_file.endswith('.json'):
            sys.stdout.write(
                '[ERROR] Wrong source file format. It must be `.json`\n',
            )
            raise NotImplementedError
        try:
            with open(self.source_file, 'r') as fs:
                self.filter_source = json.load(fs)
        except Exception as exception:
            sys.stdout.write(
                '[ERROR] Loading source file: {0}. \n Exception: {1}\n'.format(
                    self.source_file,
                    exception,
                ),
            )
            raise NotImplementedError
        if self.load_local:
            self.filter_source['fields'].append(
                self._load_local_source(),
            )
        if isinstance(self.filter_source, dict):
            self.filter_source = [self.filter_source]
        self._preprocess_filter_source()
        sys.stdout.write(
            '[GEN] Source file `{0}` has been loaded.\n'.format(
                self.source_file,
            ),
        )

    def generate(self):
        """
        Generate filter.

        Raises:
            NotImplementedError: if error

        """
        for source in self.filter_source:
            new_file = self._make_destination(
                'filter_class_{0}.py'.format(
                    str(source.get('for')).lower(),
                ),
            )
            try:
                new_filter = self.make_filter(source)
            except Exception:
                sys.stdout.write(
                    '[ERROR] Filter generating was failed.\n',
                )
                raise NotImplementedError
            sys.stdout.write(
                '[GEN] Filter `{0}` has been created successfully.\n'.format(
                    source.get('name'),
                ),
            )
            try:
                with open(new_file, 'w') as nf:
                    nf.write(new_filter)
            except Exception:
                sys.stdout.write(
                    '[ERROR] Writing new filter to file was failed.\n',
                )
                continue
            sys.stdout.write(
                '[GEN] Filter `{0}` has been written to file `{1}`.\n'.format(
                    source.get('name'),
                    os.path.abspath(new_file),
                ),
            )
        sys.stdout.write(
            '[GEN] It is finished. \n',
        )

    def make_filter(self, source_filter: dict) -> str:
        """
        Make filter.

        Args:
            source_filter (dict): filter source data

        Returns:
            filter (str): new filter

        """
        j2_env = Environment(  # noqa:S701
            loader=FileSystemLoader(self.current_dir),
            trim_blocks=True,
        )

        return j2_env.get_template(
            self.filter_template,
        ).render(
            db_schema_location=self.db_schema_location,
            filter_name=source_filter.get('name'),
            in_filter_name=source_filter.get('name'),
            in_filter_model=source_filter.get('for'),
            in_filter_order_by=convert_order_by(
                source_filter.get('orderBy').split(';'),
            ),
            filter_fields=self.make_filter_field(
                source_filter.get('fields'),
            ),
        )

    def make_filter_field(self, source_fields: List[dict]) -> List[dict]:
        """
        Make filter fields.

        Args:
            source_fields (List[dict): source filter fields data

        Returns:
            filter field (List[dict]): new filter fields

        """
        filter_fields_source = []
        for source_field in source_fields:
            field_name = ''.join(
                prt.capitalize() for prt in source_field.get('name').split('_')
            )
            filter_fields_source.append(
                {
                    'field_name': field_name,
                    'filter_field_name': str(
                        source_field.get('name'),
                    ).capitalize(),
                    'in_field_name': source_field.get('name'),
                    'in_field_datatype': self.datatype_ts_to_python.get(
                        source_field.get('type'),
                        'str',
                    ),
                    'in_field_op': source_field.get('op'),
                    'in_field_field_names': source_field.get('fieldNames'),
                },
            )
        return filter_fields_source

    def _preprocess_filter_source(self):
        for filter_source_entity in self.filter_source:
            for field_entity in filter_source_entity['fields']:
                if field_entity['op'] == '..':
                    tmp_name = field_entity['name']
                    field_entity['name'] = '{0}_from'.format(tmp_name)
                    field_entity['op'] = 'from'
                    filter_source_entity['fields'].append(
                        {
                            'name': '{0}_to'.format(tmp_name),
                            'op': 'to',
                            'type': 'Date',
                        },
                    )
                elif field_entity['op'] == 'T':
                    field_entity['name'] = 'T'
                elif field_entity['op'] in COMPARE_OPERATORS:
                    field_entity['name'] = '{0}_{1}'.format(
                        field_entity['name'],
                        field_entity['op'],
                    )

    def _make_destination(self, file_name):
        if self.destination_dir and os.path.isdir(self.destination_dir):
            return os.path.join(
                self.destination_dir,
                file_name,
            )
        sys.stdout.write(
            '[INFO] New file will be saved to current directory.\n',
        )
        return os.path.join(
            self.current_dir,
            file_name,
        )

    def _load_local_source(self):
        local_source_file = os.path.join(
            os.getcwd(),
            LOCAL_SOURCE_FILE,
        )
        try:
            with open(local_source_file, 'r') as fs:
                return json.load(fs)
        except Exception as exception:
            sys.stdout.write(
                '[ERROR] Loading local source file.\n Exception: {0}\n'.format(
                    exception,
                ),
            )
            raise NotImplementedError
