
from eztable import Table

t = Table([
    ('A', int),
    ('B', float),
    ('C', str),
])


t.extend([
    [1, 1.1, 0],
])
