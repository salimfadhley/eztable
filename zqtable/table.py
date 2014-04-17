import itertools

from six import string_types
from weakref import WeakValueDictionary, WeakSet

from .columns import DerivedColumn, Column, DerivedTableColumn, StaticColumn
from .row import TableRow
from .exceptions import InvalidData
from .index import Index


class Table(object):
    """The basic table class.
    """

    def __init__(self, schema, data=[]):
        self._columns = []
        self.indexes = WeakValueDictionary()
        self._listeners = WeakSet()

        for s in schema:
            if isinstance(s, string_types):
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
            l.notify('append', len(self) - 1)

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
        for r in itertools.izip(*self._columns):
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
        if len(col_names) and not isinstance(col_names[0], string_types):
            col_names = col_names[0]

        if (not col_names or
                not all(isinstance(c, string_types) for c in col_names)):
            raise TypeError(
                "anti_project() takes either a list of strings, or positional "
                "arguments of type string"
            )

        keep_cols = [c for c in self.column_names if not c in col_names]
        return self._project(keep_cols)

    def project(self, *col_names):
        if len(col_names) and not isinstance(col_names[0], string_types):
            col_names = col_names[0]

        if (not col_names or
                not all(isinstance(c, string_types) for c in col_names)):
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

    def add_index(self, cols):
        i = Index(self, cols=cols)
        index_key = tuple(cols)
        self.indexes[index_key] = i
        return i

    def left_join(self, keys, other):
        """Left join the other table onto this, return a table"""
        pass

    def restrict(self, col_names, fn=None):
        cols = [self._get_column(cn) for cn in col_names]

        def indices_func():
            for i in self._indices_func():
                vals = [c[i] for c in cols]
                if fn(*vals):
                    yield i
        return DerivedTable(
            indices_func=indices_func,
            columns=self._columns
        )

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.step and key.step < 0:
                # islice doesn't support negative indices, convert to a list
                f = lambda: list(self._indices_func())[key]
            else:
                f = lambda: itertools.islice(
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

        for a, b in itertools.izip_longest(self, ano):
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
    """A view on an actual table, can include
    a smaller number of rows or columns than the orginal
    for performance reasons, certain functions are prohibited.
    """

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

    def _get_column(self, name):
        actual_col = Table._get_column(self, name)
        return DerivedTableColumn(self._indices_func, actual_col)

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
            idx = next(itertools.islice(self._indices_func(), key, None))
        except StopIteration:
            raise IndexError(key)
        return Table.get_row(self, idx)
