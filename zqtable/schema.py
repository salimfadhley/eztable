import itertools
from .colmeta import ColMeta
from .exceptions import InvalidColumn, InvalidSchema


NONES = itertools.cycle([None, ])




class Schema(list):

    def __init__(self, *cols):
        self.name_to_col = {}
        for col in cols:
            if isinstance(col, ColMeta):
                self.append(col)
            else:
                self.append(ColMeta(*col))

    def validate(self, row):
        padded_row = itertools.chain(row, NONES)
        return all(c.validate(v) for c, v in zip(self, padded_row))

    def append(self, c):
        if not isinstance(c, ColMeta):
            raise InvalidColumn(c)
        
        if c.name in self.name_to_col:
            raise InvalidSchema(c) 

        list.append(self, c)
        self.name_to_col[c.name] = c

    def __str__(self):
        return ", ".join(str(c) for c in self)

    def __repr__(self):
        return "<%s.%s %s>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            str(self)
        )

    def __add__(self, other):
        s = Schema(*self)
        s.extend(other)
        return s

    def project(self, order):
        return Schema(
            self.name_to_col[cn] for cn in order
        )


    @property
    def column_names(self):
        return [cm.name for cm in self]

    @property
    def column_types(self):
        return [cm.col_type for cm in self]


