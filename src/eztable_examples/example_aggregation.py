from eztable import table_literal
t = table_literal("""
| Attack(str)   | Pokemon(str) | Level Obtained(int) | Attack Type(str) |
| Thunder Shock | Pikachu      | 1                   | Electric         |
| Tackle        | Pikachu      | 1                   | Normal           |
| Tail Whip     | Pikachu      | 1                   | Normal           |
| Growl         | Pikachu      | 5                   | Normal           |
| Quick Attack  | Pikachu      | 10                  | Normal           |
| Thunder Wave  | Pikachu      | 13                  | Electric         |
| Electro Ball  | Pikachu      | 18                  | Electric         |
| Charm         | Pikachu      | 0                   | Fairy            |
| Sweet Kiss    | Pikachu      | 0                   | Fairy            |
""")

agg = t.aggregate(
    keys=('Pokemon', 'Attack Type'),
    aggregations=[
        ('Count', int, lambda t:len(t))
    ]
)

print agg
