import unittest
from zqtable import Table, InvalidIndex


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
            keys = ('pokemon'),
            other = self.types
        )
        