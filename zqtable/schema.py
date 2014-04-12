import itertools
from .exceptions import InvalidColumn, InvalidSchema


NONES = itertools.cycle([None, ])


class ColMeta(object):

    def __init__(self, name, col_type, allow_none=True):
        if not isinstance(name, str):
            raise InvalidColumn('Bad name: %s' % name)
        if not isinstance(col_type, type):
            raise InvalidColumn('Bad type: %r' % col_type)

        self.name = name
        self.col_type = col_type
        self.allow_none = allow_none

    def __eq__(self, other):
        return self.name == other.name and self.col_type == other.col_type

    def validate(self, obj):
        if self.allow_none and obj == None:
            return True
        return isinstance(obj, self.col_type)

    def __str__(self):
        if self.col_type == str:
            return self.name
        else:
            return '%s (%s)' % (self.name, self.col_type.__name__)

    def __repr__(self):
        return "<%s.%s %s>" % (
            self.__class__.___module__,
            self.__class__.__name__,
            str(self)
        )


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
        return self


    @property
    def column_names(self):
        return [cm.name for cm in self]

    @property
    def column_types(self):
        return [cm.col_type for cm in self]


