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