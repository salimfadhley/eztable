from toytable import Table
import re


EXP_COLUMN = re.compile("([^\(\) ]+)(\s*\(([a-zA-Z0-9\.]+)\))?")


def parse_column_string(cs):
    grps = EXP_COLUMN.search(cs).groups()
    return grps[0], grps[2]


def import_something(path):
    mod = __import__(path)
    components = path.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def col_tuple_to_schema_item(ct):
    name, typestr = ct
    if not typestr:
        return name
    modpath, _, classname = typestr.rpartition('.')
    if modpath:
        return name, getattr(import_something(modpath), classname)
    return name, __builtins__[classname]


def table_literal(repr_string):
    for row in repr_string.split('\n'):
        clean_row = row.strip()
        if not clean_row:
            continue
        header_strings = [hs.strip() for hs in clean_row.split('|')[1:-1]]
        types_and_strings = [parse_column_string(h) for h in header_strings]

        return Table(header_strings)
