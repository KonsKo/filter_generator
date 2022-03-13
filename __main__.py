"""Main module to start application."""
import argparse
import os
import re
import sys
from typing import Optional

from filter_auto_generator import FilterAutoGenerator


def is_file_exists(file_name: str) -> bool:
    """
    Check file existence.

    Args:
        file_name (str): file name to check

    Returns:
        result (bool): result of checking

    """
    return os.path.isfile(
        os.path.abspath(
            file_name,
        ),
    )


def check_dir_existence(dir_name: str) -> Optional[str]:
    """
    Check dir existence.

    Args:
        dir_name (str): dir name to check

    Returns:
        dir_name (str): dir name if it exists

    """
    if os.path.isdir(os.path.abspath(dir_name)):
        return dir_name
    sys.stdout.write(
        '[WARNING] Destination directory `{0}` does not exists.\n'.format(
            os.path.abspath(dir_name),
        ),
    )


def generate_filters(
    source_files: str,
    destination_dir: Optional[str] = None,
    load_local: bool = False,
):
    """
    Run filter generator.

    Args:
        source_files (str): source files names to make filters
        destination_dir (Optional[str]): dir to save ready files
        load_local (bool): flag to load local filter fields

    """
    if not destination_dir:
        destination_dir = os.getcwd()
    source_files = re.split(r'\s*,\s*|\s+', source_files)
    for source_file in source_files:
        if is_file_exists(source_file):
            FilterAutoGenerator(
                source_file=source_file,
                destination_dir=check_dir_existence(destination_dir),
                load_local=load_local,
            ).generate()
        else:
            sys.stdout.write(
                '[ERROR] File `{0}` does not exists\n'.format(
                    source_file,
                ),
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-S',
        '--source',
        help='Required. Source file to make filters.',
        required=True,
        type=str,
        dest='source_file',
    )
    parser.add_argument(
        '-D',
        '--destination',
        help='Optional. Destination directory to save ready filters.',
        required=False,
        const=None,
        type=str,
        dest='destination_dir',
    )
    parser.add_argument(
        '-L',
        '--add_local',
        help='Optional. Set up flag to add local filter fields.',
        required=False,
        action='store_true',
        dest='add_local',
    )
    parsed_args = parser.parse_args()

    generate_filters(
        source_files=parsed_args.source_file,
        destination_dir=parsed_args.destination_dir,
        load_local=parsed_args.add_local,
    )
