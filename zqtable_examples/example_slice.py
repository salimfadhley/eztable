
from zqtable.table import Table, Schema

s = Schema(
                ('A', int),
                ('B', float),
                ('C', str),
            )
t = Table(s)

t.extend([
    (1, 1.1, 'hello'),
    (2, 2.2, 'goodbye'),
    (3, 3.3, 'yaloo'),
    (4, 4.4, 'fnuu'),
])

print t[::]