import blist
import itertools
from weakref import WeakValueDictionary, WeakSet
from itertools import izip, repeat, islice, izip_longest


class InvalidSchema(TypeError):

    """Raised when a schema appears to be invalid"""


class InvalidColumn(TypeError):

    """Raised when a column in a schema appears to be invalid"""


class InvalidData(TypeError):

    "An insert cannot complete because the row does not conform to the schema"


class Column(list):

    def __init__(self, name, values=[], type=object):
        list.__init__(self)
        self.name = name
        self.type = type
        self[:] = values


class StaticColumn(object):

    def __init__(self, name, value, len_func, type=object):
        self.name = name
        self._value = value
        self._len_func = len_func
        self.type = type

    def __iter__(self):
        return islice(repeat(self._value), self._len_func())

    def __getitem__(self, _):
        return self._value


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
        for row in izip(*self.inputs):
            yield self.func(*row)


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
        if isinstance(k, basestring):
            try:
                return self.__getattr__(k)
            except AttributeError:
                raise KeyError(k)
        else:
            return tuple.__getitem__(self, k)

    def keys(self):
        return self.schema

    def values(self):
        return list(self)

    def items(self):
        return zip(self.schema, self)


class Index(blist.blist):

    def __init__(self, table, cols):
        self.cols = [getattr(table, c) for c in cols] 
        table._listeners.add(self)

    def __hash__(self):
        return hash(c.name for c in self.cols)

    def notify(self, op, pos):
        if op=='append':
            value = tuple(c[pos] for c in self.cols) + (pos,)
            self.append(value)

    def reindex(self):
        del self[:]
        self.extend(itertools.izip(*self.cols))


class Table(object):

    def __init__(self, schema, data=[]):
        self._columns = []
        self.indexes = WeakValueDictionary()
        self._listeners = WeakSet()

        for s in schema:
            if isinstance(s, basestring):
                self._columns.append(Column(s))
            else:
                name, type = s
                self._columns.append(Column(name, type=type))

        for row in data:
            self.append(row)

    @property
    def schema(self):
        s = []
        for c in self._columns:
            s.append((c.name, c.type))
        return s

    @property
    def column_names(self):
        return [c.name for c in self._columns]

    def _create_index(self, cols):
        cols = tuple(cols)
        self._indexes[cols] = Index(self, cols)

    def append(self, row):
        """Append a row to this table.

        row must match the table's schema.

        """
        if len(row) != len(self._columns):
            raise InvalidData(
                "Expected %d columns, got %d" % (len(row), len(self._columns))
            )
        zipped = zip(row, self._columns)
        for v, c in zipped:
            if not isinstance(v, c.type):
                raise InvalidData(
                    '%r is incompatible with type %s for column %s' % (
                        v, c.type, c.name
                    )
                )
        for v, c in zipped:
            c.append(v)

        for l in self._listeners:
           l.notify('append',len(self) - 1)

    def extend(self, iterable):
        """Append all rows in iterable to this table.

        Each row must conform to this table's schema.

        """
        for row in iterable:
            self.append(row)

    def __iter__(self):
        """Iterate through the rows of this table.

        Each row is a namedtuple.

        """
        s = self._tablerow_schema()
        for r in izip(*self._columns):
            yield TableRow(r, s)

    def _tablerow_schema(self):
        return dict((c.name, i) for i, c in enumerate(self._columns))

    def __getslice__(self, start, stop):
        return self.__getitem__(slice(start, stop, 1))

    def _get_column(self, name):
        for c in self._columns:
            if c.name == name:
                return c
        raise KeyError(name)

    def anti_project(self, *col_names):
        if len(col_names) and not isinstance(col_names[0], basestring):
            col_names = col_names[0]

        if (not col_names or
                not all(isinstance(c, basestring) for c in col_names)):
            raise TypeError(
                "anti_project() takes either a list of strings, or positional "
                "arguments of type string"
            )

        keep_cols = [c for c in self.column_names if not c in col_names]
        return self._project(keep_cols)

    def project(self, *col_names):
        if len(col_names) and not isinstance(col_names[0], basestring):
            col_names = col_names[0]

        if (not col_names or
                not all(isinstance(c, basestring) for c in col_names)):
            raise TypeError(
                "project() takes either a list of strings, or positional "
                "arguments of type string"
            )

        return self._project(col_names)

    def _indices_func(self):
        return xrange(len(self))

    def _project(self, col_names):
        cols = [self._get_column(c) for c in col_names]
        return DerivedTable(self._indices_func, cols)

    def expand_const(self, name, value, type=object):
        return DerivedTable(
            self._indices_func,
            self._columns + [StaticColumn(name, value, self.__len__, type)]
        )

    def expand(self, name, input_columns, fn, type=object):
        incols = []
        for c in input_columns:
            incols.append(self._get_column(c))
        return DerivedTable(
            self._indices_func,
            self._columns + [DerivedColumn(name, incols, fn, type)]
        )

    def hash(self, name, input_columns):
        return self.expand(name, input_columns, hash, int)

    def copy(self):
        """Create a materialised copy of this table."""
        t = Table(self.schema)
        t.extend(self)
        return t

    def add_index(self, name, cols):
        i = Index(self, cols=cols)
        self.indexes[name] = i
        return i

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.step and key.step < 0:
                # islice doesn't support negative indices, convert to a list
                f = lambda: list(self._indices_func())[key]
            else:
                f = lambda: islice(
                    self._indices_func(),
                    key.start,
                    key.stop,
                    key.step or None
                )
            return DerivedTable(f, self._columns[:])
        else:
            return self.get_row(key)

    def __getattr__(self, attr):
        try:
            return self._get_column(attr)
        except KeyError:
            raise AttributeError(
                "%r object has no attribute %r" % (
                    self.__class__.__name__, attr
                )
            )

    def get_row(self, key):
        s = self._tablerow_schema()
        return TableRow([c[key] for c in self._columns], s)

    def __len__(self):
        return len(self._columns[0])

    def __eq__(self, ano):
        if not isinstance(ano, Table):
            return False

        if self.schema != ano.schema:
            return False

        for a, b in izip_longest(self, ano):
            if a != b:
                return False

        return True

    def __repr__(self):
        cl = [len(c.name) for c in self._columns]
        for r in self:
            for i, (m, c) in enumerate(zip(cl, r)):
                if c > m:
                    cl[i] = c

        out = []

        def row(r):
            out.append(
                '| %s |' % (' | '.join(str(c).ljust(l) for l, c in zip(cl, r)))
            )
        row(c.name for c in self._columns)
        for r in self:
            row(r)
        return '\n'.join(out)


class DerivedTable(Table):

    def __init__(self, indices_func, columns):
        self._indices_func = indices_func
        self._columns = columns

    def __iter__(self):
        cs = self._columns
        s = dict((c.name, i) for i, c in enumerate(cs))
        cls = TableRow
        for i in self._indices_func():
            # Slightly optimised, eg. we don't do LOAD_GLOBAL in this loop
            r = (c[i] for c in cs)
            yield cls(r, s)

    def append(self, row):
        raise TypeError("Cannot do append on a non-materialised table.")

    def extend(self, rows):
        raise TypeError("Cannot do extend on a non-materialised table.")

    def __len__(self):
        idxs = self._indices_func()
        try:
            return len(idxs)
        except (AttributeError, TypeError):
            return sum(1 for _ in idxs)

    def get_row(self, key):
        try:
            idx = next(islice(self._indices_func(), key, None))
        except StopIteration:
            raise IndexError(key)
        return Table.get_row(self, idx)
