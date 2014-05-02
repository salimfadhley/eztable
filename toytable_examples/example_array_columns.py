from toytable import table_literal, Table

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
    keys=('Type Id', ),
    other=types
)

print pokedex