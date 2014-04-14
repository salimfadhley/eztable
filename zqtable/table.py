from .schema import Schema
from .exceptions import InvalidSchema, InvalidData
from .colmeta import ColMeta


class BaseTable(object):

    def project(self, col_names):
        return ProjectedTable(self, col_names)

    def to_list(self):
        return list(self)

    def expand_const(self, column_name, column_type, value):
        return ExpandedTable(
            t=self,
            column_name=column_name,
            column_type=column_type,
            value=value)

    def expand(self, column_name, column_type, input_columns, fn):
        return ExpandedTable(
            t=self,
            column_name=column_name,
            column_type=column_type,
            input_columns=input_columns,
            fn=fn)

    def hash(self, column_name, input_columns):
        return ExpandedTable(
            t=self,
            column_name=column_name,
            column_type=int,
            input_columns=input_columns,
            fn=hash
        )

    def column_order(self, column_names):
        return [self.schema.get_column_index_by_name(cn) for cn in column_names]

    def materialize(self):
        t = Table(self.schema)
        t.extend(self.to_list())
        return t

    def __getitem__(self, key):
        if isinstance(key, slice):
            return SlicedTable(t=self, sl=key)
        return list.__getitem__(self, key)

    def __getattr__(self, key):
        if key in self.schema.name_to_col:
            return Column(self, key)
        raise AttributeError(key)


class Table(BaseTable, list):

    def __init__(self, schema):
        if not isinstance(schema, Schema):
            raise InvalidSchema(schema)
        self.schema = schema

    def append(self, row):
        if not self.schema.validate(row):
            raise InvalidData(row)
        list.append(self, row)

    def extend(self, rows):
        for row in rows:
            self.append(row)

    def __getslice__(self, start, stop):
        return self.__getitem__(slice(start, stop, 1))


class ExpandedTable(BaseTable):

    def __init__(self, t, column_name, column_type, input_columns=None, value=None, fn=None):
        self.t = t
        self.column_name = column_name
        self.column_type = column_type
        self.value = value
        self.input_columns = input_columns or []
        self.input_column_order = self.column_order(self.input_columns)
        self.fn = fn

    @property
    def schema(self):
        return self.t.schema + Schema(ColMeta(self.column_name, self.column_type))

    def compute_value(self, row):
        if not self.fn:
            return self.value
        return self.fn(*self.args_tuple(row))

    def args_tuple(self, row):
        return tuple(row[i] for i in self.input_column_order)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return SlicedTable(t=self, sl=key)
        else:
            row = list(self.t[key])
            return row + [self.compute_value(row)]

    def __len__(self):
        return self.t.__len__()

    def __getattr__(self, key):
        if key == self.column_name:
            return Column(self, key)
        raise AttributeError(key)


class SlicedTable(BaseTable):

    def __init__(self, t, sl):
        assert isinstance(sl, slice), 'Expected a slice, got %s' % repr(sl)
        self.t = t
        self.sl = sl

    def __len__(self):
        start, stop, stride = self.sl.indices(len(self.t))
        return abs(stop - start) / stride

    @property
    def schema(self):
        return self.t.schema

    def __getitem__(self, key):
        start, stop, stride = self.sl.indices(len(self.t))
        adjusted_key = start + (stride * key)
        return self.t[adjusted_key]


class Column(BaseTable):

    def __init__(self, t, column_name):
        self.t = t
        self.column_name = column_name

    @property
    def schema(self):
        return self.t.schema.project([self.column_name])

    def to_list(self):
        col_index = self.t.schema.get_column_index_by_name(self.column_name)
        return [row[col_index] for row in self.t.to_list()]


class ProjectedTable(BaseTable):

    def __init__(self, t, column_names):
        self.t = t
        self.column_names = column_names

    @property
    def schema(self):
        return self.t.schema.project(self.column_names)

    def _to_list(self):
        index_order = self.column_order(self.column_names)
        for row in self.t:
            yield [row[i] for row in index_order]

    def to_list(self):
        return list(self._to_list())

    def _projected_column_order(self):
        return self.column_order(self.column_names)

    def column_order(self, column_names):
        return [self.t.schema.get_column_index_by_name(cn) for cn in column_names]

    def __getitem__(self, key):
        index_order = self._projected_column_order()
        return [self.t[key][i] for i in index_order]
