import unittest
import collections
from zqtable import Table, InvalidIndex
from zqtable.table import JoinTable


class TestJoin(unittest.TestCase):

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
            keys=('pokemon', ),
            other = self.types
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

    def test_join_schema(self):
        t = self.pokedex.left_join(
            keys=('pokemon', ),
            other = self.types
        )

        expected = [
            ('pokemon', object),
            ('owner', object),
            ('level', object),
            ('type', object),
        ]

        self.assertEquals(
            t.schema,
            expected
        )

    def test_join_indeces_function(self):
        t = self.pokedex.left_join(
            keys=('pokemon', ),
            other = self.types
        )
        self.assertEquals(
            list(t._join_indices_func()),
            [6, 3, 4, 5, 0, 1, 2]
        )

    def test_join_row(self):
        t = self.pokedex.left_join(
            keys=('pokemon', ),
            other = self.types
        )
        self.assertEquals(
            t[0],
            ('Charmander', 'Ash', 12, 'Fire')
        )

    def test_join_iter(self):
        t = self.pokedex.left_join(
            keys=('pokemon', ),
            other = self.types
        )
        tl = list(t)
        self.assertEquals(
            tl[1],
            ('Pikachu', 'Ash', 15, 'Electric')
        )


if __name__ == '__main__':
    unittest.main()
