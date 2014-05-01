import itertools
import array
import six

if six.PY2:
    import types
    builtin_types = vars(types).values()
else:
    import builtins
    builtin_types = vars(builtins).values()


def describe_column(name, typ):
    if typ is object:
        return name
    if typ in builtin_types:
        return "%s (%s)" % (name, typ.__name__)

    return "%s (%s.%s)" % (
        name,
        typ.__module__,
        typ.__name__
    )


class Column(list):
    def __init__(self, name, values=[], type=object):
        list.__init__(self)
        self.name = name
        self.type = type
        self[:] = values

    @property
    def description(self):
        return describe_column(self.name, self.type)

    def validate(self, v):
        return v is None or isinstance(v, self.type)

    def fn_from_string(self):
        return self.type


class ArrayColumn(array.array):

    PY_TYPE_MAPPING = {
        'c':str,
        'b':int,
        'B':int,
        'u':six.u,
        'h':int,
        'H':int,
        'i':int,
        'I':int,
        'l':int,
        'L':int,
        'f':float,
        'd':float
    }

    def __new__(cls, name, values=None, type='i'):
        return array.array.__new__(cls, type)

    def __init__(self, name, values=None, type='i'):
        self.name = name
        self.extend(values or [])


    def fn_from_string(self):
        return self.PY_TYPE_MAPPING[self.typecode]

    @property
    def type(self):
        return self.typecode

    def validate(self, v):
        return True # Delegate to underlying class

    @property
    def description(self):
        return '%s (%s)' % (self.name, self.type)

class StaticColumn(object):

    def __init__(self, name, value, len_func, type=object):
        self.name = name
        self._value = value
        self._len_func = len_func
        self.type = type

    def __iter__(self):
        return (
            itertools.islice(itertools.repeat(self._value), self._len_func())
        )

    def __getitem__(self, _):
        return self._value

    @property
    def description(self):
        return describe_column(self.name, self.type)


class DerivedColumn(object):

    def __init__(self, name, inputs, func, type=object):
        self.name = name
        self.type = type

        self.func = func
        self.inputs = inputs

    def __getitem__(self, idx):
        row = tuple(c[idx] for c in self.inputs)
        return self.func(*row)

    def __iter__(self):
        for row in itertools.izip(*self.inputs):
            yield self.func(*row)

    @property
    def description(self):
        return describe_column(self.name, self.type)


class AggregationColumn(object):

    def __init__(self):
        pass


class DerivedTableColumn(object):

    """Not so much a derived column, but a column on a
    derived table"""

    def __init__(self, indices_func, column, name=None):
        self._indices_func = indices_func
        self._column = column

    @property
    def name(self):
        return self._column.name

    @property
    def type(self):
        return self._column.type

    @property
    def description(self):
        return self._column.description

    def __iter__(self):
        for i in self._indices_func():
            yield self._column[i]

    def __len__(self):
        return len([None for i in self._indices_func()])

    def __getitem__(self, key):
        if isinstance(key, int):
            i = next(itertools.islice(
                self._indices_func(),
                key,
                key + 1
            ))
            return None if i is None else self._column[i]


class JoinColumn(DerivedTableColumn):
    pass
