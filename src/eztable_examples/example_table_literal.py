from eztable import table_literal
pokedex = table_literal("""
    | Pokemon (str) | Level (int) | Owner (str) | Type (str) |
    | Pikchu        | 12          | Ash Ketchum | Electric   |
    | Bulbasaur     | 16          | Ash Ketchum | Grass      |
    | Charmander    | 19          | Ash Ketchum | Fire       |
    | Raichu        | 23          | Lt. Surge   | Electric   |
    """)

print pokedex.column_names
print pokedex.column_types
print list(pokedex.Pokemon)
