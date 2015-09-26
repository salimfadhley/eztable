from eztable import table_literal, Table

types = Table([('Type Id', 'i'), ('Type', str)])
types.append([1, 'water'])
types.append([2, 'bug'])

t = table_literal("""
| Pokedex Number (i) | Pokemon (str) | Type Id (i) |
| 7                  | Squirtle      | 1           |
| 8                  | Wartortle     | 1           |
| 9                  | Blastoise     | 1           |
| 10                 | Caterpie      | 2           |
| 11                 | Metapod       | 2           |
| 12                 | Butterfree    | 2           |
""")

pokedex = t.left_join(
    keys=('Type Id',),
    other=types
)
print pokedex

table0 = table_literal("""
| foo (c) | bar (i) | baz (f) |
| x       | 2       | 2.2     |
""")

table1 = Table([('foo', 'c'), ('bar', 'i'), ('baz', 'f')])
table1.append(['x', 2, 2.2])

assert table0 == table1

table1.append(['x', '!!!', 2.2])
