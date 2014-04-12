from .schema import Schema
from .exceptions import InvalidSchema, InvalidData

class Table(list):
    
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

    def __getitem__(self, key):
        if isinstance(key, slice):
            return SlicedTable(t=self, sl=key)
        return list.__getitem__(self, key)

class SlicedTable(object):
    def __init__(self, t, sl):
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