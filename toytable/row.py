from six import string_types


class TableRow(tuple):

    """Table row tuple.

    Also has dict-like behaviour.

    Attribute access acts somewhat like a namedtuple, but doesn't validate its
    schema, so arbitrary column names are allowed, even if they can't be
    accessed as attributes.

    """
    def __new__(cls, row, schema):
        return tuple.__new__(cls, row)

    def __init__(self, row, schema):
        self.schema = schema

    def __getattr__(self, name):
        try:
            i = self.schema[name]
        except KeyError:
            raise AttributeError(name)
        else:
            return tuple.__getitem__(self, i)

    def __getitem__(self, k):
        if isinstance(k, string_types):
            try:
                return self.__getattr__(k)
            except AttributeError:
                raise KeyError(k)
        else:
            return tuple.__getitem__(self, k)

    def keys(self):
        return tuple(self.schema.keys())

    def values(self):
        return list(self)

    def items(self):
        return zip(self.schema, self)
