import unittest
import collections
from toytable import Table, InvalidIndex, table_literal, TableTestMixin
from toytable.table import JoinTable


class TestJoin(unittest.TestCase):

    def setUp(self):
        self.pokedex = Table(['pokemon', 'owner', ('level', 'i')])
        self.pokedex.extend([
            ['Charmander', 'Ash', 12],
            ['Pikachu', 'Ash', 15],
            ['Squirtle', 'Ash', 19],
            ['Starmie', 'Misty', 19],
            ['Togepi', 'Misty', 5],
            ['Onyx', 'Brock', 22],
            ['Meowth', 'Team Rocket', 22],
            ['Mew', None, 99],
        ])

        self.types = Table(['pokemon', 'type'])
        self.types.extend([
            ['Togepi', 'Fairy'],
            ['Onyx', 'Rock'],
            ['Meowth', 'Normal'],
            ['Pikachu', 'Electric'],
            ['Squirtle', 'Water'],
            ['Starmie', 'Water'],
            ['Charmander', 'Fire'],
        ])

    def test_join_interface(self):
        t = self.pokedex.left_join(
            keys=('pokemon',),
            other=self.types
        )
        self.assertEquals(
            t._key_columns,
            [t.pokemon, ]
        )
        self.assertEquals(
            t.column_names,
            ['pokemon', 'owner', 'level', 'type']
        )

    def test_join_schema(self):
        t = self.pokedex.left_join(
            keys=('pokemon',),
            other=self.types
        )
        expected = [
            ('pokemon', object),
            ('owner', object),
            ('level', 'i'),
            ('type', object),
        ]
        self.assertEquals(
            t.schema,
            expected
        )

    def test_join_indeces_function(self):
        t = self.pokedex.left_join(
            keys=('pokemon',),
            other=self.types
        )
        self.assertEquals(
            list(t._join_indices_func()),
            [6, 3, 4, 5, 0, 1, 2, None]
        )

    def test_join_row(self):
        t = self.pokedex.left_join(
            keys=('pokemon',),
            other=self.types
        )
        self.assertEquals(
            t[0],
            ('Charmander', 'Ash', 12, 'Fire')
        )

    def test_join_iter(self):
        t = self.pokedex.left_join(
            keys=('pokemon',),
            other=self.types
        )
        tl = list(t)
        self.assertEquals(
            tl[1],
            ('Pikachu', 'Ash', 15, 'Electric')
        )

    def test_impossible_join(self):
        t = self.pokedex.left_join(
            keys=('pokemon',),
            other=self.types
        )
        self.assertEquals(
            t[7],
            ('Mew', None, 99, None)
        )

    def test_over_read(self):
        t = self.pokedex.left_join(
            keys=('pokemon',),
            other=self.types
        )
        with self.assertRaises(IndexError):
            t[99]

class TestInnerJoin(unittest.TestCase, TableTestMixin):

    def setUp(self):
        self.pokedex = Table([('pokemon', str), ('owner', str), ('level', 'i')])
        self.pokedex.extend([
            ['Charmander', 'Ash', 12],
            ['Pikachu', 'Ash', 15],
            ['Squirtle', 'Ash', 19],
            ['Starmie', 'Misty', 19],
            ['Togepi', 'Misty', 5],
            ['Onyx', 'Brock', 22],
            ['Meowth', 'Team Rocket', 22],
            ['Mew', None, 1],
            ['Mewtwo', None, 1],
        ])

        self.types = Table([('pokemon', str), ('type', str)])
        self.types.extend([
            ['Togepi', 'Fairy'],
            ['Onyx', 'Rock'],
            ['Meowth', 'Normal'],
            ['Charmander', 'Fire'],
            ['Snorlax', 'Normal']
        ])

    def test_inner_join_simple(self):
        j = self.pokedex.inner_join(
            keys=('pokemon',),
            other=self.types
        )

        expected = table_literal("""
            | pokemon (str) | owner (str) | level (i) | type (str) |
            | Charmander    | Ash         | 12        | Fire       |
            | Togepi        | Misty       | 5         | Fairy      |
            | Onyx          | Brock       | 22        | Rock       |
            | Meowth        | Team Rocket | 22        | Normal     |
        """)

        self.assertTablesEqual(
            j.copy(),
            expected
        )


class TestJoinWithNonMatchingKeys(unittest.TestCase):

    def setUp(self):
        self.pokedex = Table(['pokemon', 'owner', 'level'])
        self.pokedex.extend([
            ['Charmander', 'Ash', 12],
            ['Pikachu', 'Ash', 15],
            ['Squirtle', 'Ash', 19],
            ['Starmie', 'Misty', 19],
            ['Togepi', 'Misty', 5],
            ['Onyx', 'Brock', 22],
            ['Meowth', 'Team Rocket', 22],
        ])

        self.types = Table(['pkmn', 'type'])
        self.types.extend([
            ['Togepi', 'Fairy'],
            ['Onyx', 'Rock'],
            ['Meowth', 'Normal'],
            ['Pikachu', 'Electric'],
            ['Squirtle', 'Water'],
            ['Starmie', 'Water'],
            ['Charmander', 'Fire'],
        ])

    def test_basic_join(self):

        t = self.pokedex.left_join(
            keys=('pokemon',),
            other=self.types,
            other_keys=('pkmn',),
        )

        self.assertIsInstance(t, JoinTable)

        self.assertEquals(
            t._key_columns,
            [t.pokemon, ]
        )

        self.assertEquals(
            t.column_names,
            ['pokemon', 'owner', 'level', 'type']
        )


class TestBrokenJoin(unittest.TestCase):

    def test_incomplete_join(self):
        p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])

        p.extend([
            [1, 'Pikachu', 18],
            [2, 'Blastoise', 22],
            [3, 'Weedle', 4],
        ])

        o = Table([('Owner Id', int), ('Owner Name', str)])
        o.append([1, 'Ash Ketchum'])
        o.append([2, 'Brock'])
        o.append([2, 'Misty'])

        j = p.left_join(
            keys=('Owner Id',),
            other=o
        )

        self.assertEquals(
            j.column_names,
            ['Owner Id', 'Pokemon', 'Level', 'Owner Name']
        )

    def test_joined_table_repr(self):
        p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
        o = Table([('Owner Id', int), ('Owner Name', str)])
        j = p.left_join(keys=('Owner Id',), other=o)
        self.assertEquals(
            repr(j),
            "| Owner Id (int) | Pokemon | Level (int) | Owner Name (str) |"
        )

    def test_joined_table_repr_one_row(self):
        p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
        p.extend([
            [1, 'Pikachu', 18],
        ])
        o = Table([('Owner Id', int), ('Name', str)])
        o.append([1, 'Ash Ketchum'])
        j = p.left_join(
            keys=('Owner Id',),
            other=o
        )

        self.assertEquals(
            j[0],
            (1, 'Pikachu', 18, 'Ash Ketchum')

        )

        self.assertEquals(
            list(j)[0],
            (1, 'Pikachu', 18, 'Ash Ketchum'),
        )


if __name__ == '__main__':
    unittest.main()
