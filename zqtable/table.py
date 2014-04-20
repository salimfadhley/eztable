import itertools
from collections import namedtuple
from six import string_types
from weakref import WeakValueDictionary, WeakSet

from .columns import DerivedColumn, Column, DerivedTableColumn, StaticColumn, JoinColumn
from .row import TableRow
from .exceptions import InvalidData
from .index import Index


class Table(object):

    """The basic table class. Table objects contain
    any Python data type, however some features may be unavailable
    if the types are non-hashable."""

    def __init__(self, schema, data=[]):
        """
        Every Table     object has a sschema. In it's simple form, the schema can be
        nothing more than a list of string column-names. Specifying a schema
        this way will produce a non-typed table, in which any Python type can be stored in
        any column.

        Alternativly the schema can include type information. Instead of Specifying the
        schema item as a string, use (column_name, type), where type is a python type
        or class object, for example int, str.

        It is expected that most of the values stored in the table will be simple objects or native
        types such as numbers and strings, however it is also possible to store any python
        object as long as they are hashable.

        param schema: Column names as a sequence of strings, or ('col_name', type)
        type schema: list
        param data: Optional rows of data to initialize the table.
        type data: list of lists
        """
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

    def append(self, row):
        """Append a single row to this table. The row must match the table's
        schema, typically this means that the row should have the same number
        of items, however if types were specified then the type of each
        positional element must conform to the required type of the corresponding
        schema column.

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
        """Append all rows in iterable to this table. Each row
        must conform to this table's schema.
        """
        for row in iterable:
            self.append(row)

    @property
    def schema(self):
        """Get the table's schema. This is a list of
        (name (string), type) tuples.
        """
        s = []
        for c in self._columns:
            s.append((c.name, c.type))
        return s

    @property
    def _all_columns(self):
        return self._columns

    @property
    def column_names(self):
        """Get the table's column names as a list of strings.
        """
        return [c.name for c in self._all_columns]

    @property
    def column_types(self):
        """Get the table's column types as a list of types.
        """
        return [c.type for c in self._all_columns]

    @property
    def _column_descriptions(self):
        return [c.description for c in self._all_columns]

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
        """Get a single Column object by name. Columns are list-like sequences.
        """
        for c in self._columns:
            if c.name == name:
                return c
        raise KeyError(name)

    def anti_project(self, *col_names):
        """Returns a new DerivedTable in which the named columns
        have been removed.

        Unless the new table is materialised it shares the same
        data as the table it was made from, hence extending or appending
        from the new table will also modify the projected table.

        Ordering of the original columns will be retained, except that
        the specified columns will no longer be accessible.
        """
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
        """Returns a new DerivedTable in which only the named
        columns remain in the order specified by col_names.
        """
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
        """Internal function: This specifies the order in which the
        __iter__ method retreives rows.
        """
        return xrange(len(self))

    def rename(self, old_names, new_names):
        """Rename columns in the table. Does not affect the order of
        columns.

        :param old_names: list of column names to rename.
        :param new_names: list of the new names to asign to the renamed columns.
        """
        rename_dict = dict(zip(old_names, new_names))
        return self._project(
            col_names=self.column_names,
            rename_dict=rename_dict
        )

    def _project(self, col_names, rename_dict=None):
        """Implementation of project, anti_project and rename function"""
        rename_dict = rename_dict or {}
        cols = [self._get_column(c) for c in col_names]
        column_names = [rename_dict.get(cn) for cn in self.column_names]
        return (
            DerivedTable(self._indices_func, cols, rename_dict=rename_dict)
        )

    def expand_const(self, name, value, type=object):
        """Returns a new DerivedTable in which a single column of
        static data has been added.
        """
        return DerivedTable(
            self._indices_func,
            self._columns + [StaticColumn(name, value, self.__len__, type)],
        )

    def expand(self, name, input_columns, fn, type=object):
        """Returns a new DerivedTable in which a new calculated
        column has been added.

        This column's value is determined by a function and
        a set of input columns.

        param name: The name of the new derived coulumn.
        type name: str
        param input_columns: The input column names.
        type input_columns: list of str
        param fn; A function or lambda
        param type: Optionally, constrain the value of this column by type
        """
        incols = []
        for c in input_columns:
            incols.append(self._get_column(c))
        return DerivedTable(
            self._indices_func,
            self._columns + [DerivedColumn(name, incols, fn, type)]
        )

    def hash(self, name, input_columns):
        """A convenience function that expands the table
        with a new hash column.
        """
        return self.expand(name, input_columns, hash, int)

    def copy(self):
        """Create a 'materialised' copy of this table.

        This converts all dynamically generated columns into
        StaticColumn objects.
        """
        t = Table(self.schema)
        t.extend(self)
        return t

    def add_index(self, cols):
        """Create a new index on a set of columns.

        Indexes are list-like objects which can be used to
        speed-up access to rows of data. Indexes improve the
        preformance of operations (e.g. joins).

        The Table class only holds a weak-reference to this object,
        hence the user must retain a reference to the index
        in order to prevent it from being garbage collected.

        param cols: Column names to be included into the index.
        type cols: List of strings.
        """
        i = Index(table=self, cols=cols)
        index_key = tuple(cols)
        self.indexes[index_key] = i
        return i

    def left_join(self, keys, other, other_keys=None):
        """Left join the other table onto this, return a table.

        :param keys: List of column names which will be matched.
        :param other: the other table to join on to this table.
        :param other_keys: Optional list of foreign keys
        """
        other_keys = other_keys or keys
        return JoinTable(
            indices_func=self._indices_func,
            left_columns=self._columns,
            keys=keys,
            other=other,
            other_keys=other_keys
        )

    def restrict(self, col_names, fn=None):
        """
        Return a new DerivedTable object in which
        all visible rows satisfy some kind of logical
        constraint given by fn.

        param col_names: List of column names to feed into fn
        type col_names: list of strings
        param fn: Should return True for any retained row.
        type fn: fuunction or lambda
        """
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
            return DerivedTable(
                f,
                self._columns[:],
            )
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
        cl = [len(cn) for cn in self._column_descriptions]
        for r in self:
            for i, (m, c) in enumerate(zip(cl, r)):
                this_col_len = len(repr(c))
                if this_col_len > m:
                    cl[i] = this_col_len

        out = []

        def row(r):
            out.append(
                '| %s |' % (' | '.join(str(c).ljust(l) for l, c in zip(cl, r)))
            )
        row(c.description for c in self._columns)
        for r in self:
            row(r)
        return '\n'.join(out)


class DerivedTable(Table):

    """A view on an actual table, can include
    a smaller number of rows or columns than the orginal
    for performance reasons, certain functions are prohibited.
    """

    def __init__(self, indices_func, columns, rename_dict=None):
        self._indices_func = indices_func
        self._columns = columns
        self._rename_dict = rename_dict or {}
        self._inv_rename_dict = {v: k for k, v in self._rename_dict.items()}

    @property
    def column_names(self):
        rd = self._rename_dict
        return [rd.get(c.name, c.name) for c in self._columns]

    def __iter__(self):
        cs = self._columns
        s = dict((c.name, i) for i, c in enumerate(cs))
        cls = TableRow
        for i in self._indices_func():
            # Slightly optimised, eg. we don't do LOAD_GLOBAL in this loop
            r = (c[i] for c in cs)
            yield cls(r, s)

    def _get_column(self, name):
        actual_name = self._inv_rename_dict.get(name, name)
        actual_col = Table._get_column(self, actual_name)
        return DerivedTableColumn(self._indices_func, actual_col, name=name)

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


class JoinTable(DerivedTable):

    """The result of a table join operation.
    """

    def __init__(self, indices_func, left_columns, keys, other, other_keys):
        self._indices_func = indices_func
        self._left_columns = left_columns
        self._keys = keys
        self._other = other
        self._other_keys = other_keys

        # Finally build an index
        self._join_index = other.add_index(
            cols=other_keys
        ).reindex()

    @property
    def _columns(self):
        return self._left_columns + self._join_columns

    def _both_indices_func(self):
        """Generator function which gives a sequence of pairs:
        The first value is the index for the row in this table.
        The second value is the index for the row in the joined table.
        """
        kcs = self._key_columns
        for i in self._indices_func():
            key = tuple(kc[i] for kc in kcs)
            try:
                yield i, self._join_index.index(key)
            except ValueError:
                yield i, None

    def _join_indices_func(self):
        """Generator function giving only the sequence
        of indices in the joined columns
        """
        for _, ji in self._both_indices_func():
            yield ji

    def _get_column(self, name):
        """Get a single Column object by name. Columns are list-like sequences.
        """
        for c in self._columns + self._join_columns:
            if c.name == name:
                return c
        raise KeyError(name)

    @property
    def _key_columns(self):
        return [self._get_column(k) for k in self._keys]

    @property
    def _join_columns(self):
        all_keys = set(self._keys + self._other_keys)
        return (
            [JoinColumn(indices_func=self._join_indices_func, column=c)
             for c in self._other._columns if not c.name in all_keys]
        )

    @property
    def column_names(self):
        """Get the table's column names as a list of strings.
        """
        return [c.name for c in (self._left_columns + self._join_columns)]

    @property
    def schema(self):
        """Get the table's schema. This is a list of
        (name (string), type) tuples.

        The method on Table is overriden because
        we need to get the schema from both the original
        and joined columns.
        """
        s = []
        for c in self._columns:
            s.append((c.name, c.type))
        return s

    def __getitem__(self, key):
        cs = self._left_columns
        jcs = self._join_columns
        i, ji = itertools.islice(
            self._both_indices_func(), key, key + 1).next()

        s = dict((c.name, i) for i, c in enumerate(self._columns))
        r = itertools.chain(
            (c[i] for c in cs),
            (jc._column[ji]
             for jc in jcs)  # Act on the underlying columns here
        )
        return TableRow(r, s)

    def __iter__(self):
        cs = self._left_columns
        jcs = self._join_columns
        kcs = self._key_columns
        s = dict((c.name, i) for i, c in enumerate(self._all_columns))
        for i, ji in self._both_indices_func():
            if ji:
                r = itertools.chain(
                    (c[i] for c in cs),
                    (jc._column[ji] for jc in jcs)
                )
            else:
                r = itertools.chain(
                    (c[i] for c in cs),
                    (None for jc in jcs)
                )
            yield TableRow(r, s)
