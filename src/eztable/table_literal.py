import re
from eztable.table import Table

EXP_COLUMN = re.compile("([^\(]+)(\s*\(([a-zA-Z0-9\.]+)\))?")


def parse_column_string(cs):
    grps = EXP_COLUMN.search(cs).groups()
    return grps[0].strip(), grps[2]


def import_something(path):
    mod = __import__(path)
    components = path.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def col_tuple_to_schema_item(ct, default_type):
    name, typestr = ct
    if not typestr:
        return name, default_type
    if len(typestr) == 1:
        return name, typestr  # Array
    modpath, _, classname = typestr.rpartition('.')
    if modpath:
        return name, getattr(import_something(modpath), classname)
    return name, __builtins__[classname]


def split_row(str_row):
    return [hs.strip() for hs in str_row.split('|')[1:-1]]


def clean_rows(repr_string):
    for row in repr_string.split('\n'):
        clean_row = row.strip()
        if not clean_row:
            continue
        yield split_row(clean_row)


def table_literal(repr_string, default_type=str):
    """Create a toytable.Table object from a multi-line
    string expression. The input format is exactly the
    same as the Table class's repr format::

        >>> from toytable import table_literal
        >>> pokedex = table_literal(\"\"\"
        ...     | Pokemon (str) | Level (int) | Owner (str) | Type (str) |
        ...     | Pikchu        | 12          | Ash Ketchum | Electric   |
        ...     | Bulbasaur     | 16          | Ash Ketchum | Grass      |
        ...     | Charmander    | 19          | Ash Ketchum | Fire       |
        ...     | Raichu        | 23          | Lt. Surge   | Electric   |
        ...     \"\"\")
        >>>
        >>> print pokedex.column_names
        ['Pokemon', 'Level', 'Owner', 'Type']
        >>> print pokedex.column_types
        [<type 'str'>, <type 'int'>, <type 'str'>, <type 'str'>]
        >>> print list(pokedex.Pokemon)
        ['Pikchu', 'Bulbasaur', 'Charmander', 'Raichu']

    Since table literal expressions are strings all columns
    require a type to be explicitly specified. All untyped columns
    are presumed to be strings.

    The type column can be any importable object or function
    capable of building the contents of the column from the 
    string values of each element in the column.

    :param repr_string: table definition
    :type repr_string: str
    :param default_type: optional type to apply to columns where no type is given
    :type default_type: type
    """
    rows_iter = clean_rows(repr_string)
    column_names_and_types = [col_tuple_to_schema_item(parse_column_string(h), default_type=str)
                              for h in next(rows_iter)  ]

    t = Table(column_names_and_types)
    fns = [c.fn_from_string() for c in t._columns]

    def process_row(lst_row):
        for ty, val in zip(fns, lst_row):
            yield ty(val)

    data = (list(process_row(row)) for row in rows_iter)
    t.extend(data)

    return t
