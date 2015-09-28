from eztable import table_literal
pokedex = table_literal("""
    | Owner Id (int) | Pokemon    | Level (int) |
    | 1              | Pikachu    | 18          |
    | 1              | Bulbasaur  | 22          |
    | 1              | Charmander | 12          |
    | 3              | Togepi     | 5           |
    | 1              | Starmie    | 44          |
    | 9              | Mew        | 99          |
    """)
print(pokedex)
