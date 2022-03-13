# Filter Auto Generator

## Create filters from json-file(s).

Source file structure must correspond to `filter_source.json`.

Nevertheless, you can place source data for one filter in one file or 
make it for several filters in one file as List[Dict] or you can 
provide several source files at once.

New file with filter will have a name such `filter_<for>` where `<for>` is 
model name. Full example is `filter_email.py`.

Feel free to adjust imports.

### Run


`python WORK_DIR -S/--source <source_file> -D/--destination <destination_dir>`

where:

   `WORK_DIR` - project directory

   `-S/-source <source_file>, Required, String` - source file name(s) 
   to create filter. You can set up `<source_file>` as one file name or
   sequence of several file names with delimiters either while space or coma

   `-D/--destination <destination_dir>, Optional, String` - destination 
   directory to save filters, by default is WORK_DIR

