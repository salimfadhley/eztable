
from zqtable.table import Table, Schema

t = Table(Schema(
            ('A', int),
            ('B', float),
            ('C', str),
        ))


t.extend([
    [1, 1.1, 0],
])