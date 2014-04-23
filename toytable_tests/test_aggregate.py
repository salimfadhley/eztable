import unittest
from toytable import table_literal


class TestAggregate(unittest.TestCase):

    """Verify the correctness of aggegation functions.
    """

    def setUp(self):
        self.t = table_literal("""
            | Attack (str)  | Pokemomn (str) | Level Obtained (int) | Attack Type (str) |
            | Thunder Shock | Pikachu        | 1                    | Electric          |
            | Tackle        | Pikachu        | 1                    | Normal            |
            | Tail Whip     | Pikachu        | 1                    | Normal            |
            | Growl         | Pikachu        | 5                    | Normal            |
            | Quick Attack  | Pikachu        | 10                   | Normal            |
            | Thunder Wave  | Pikachu        | 13                   | Electric          |
            | Electro Ball  | Pikachu        | 18                   | Electric          |
            | Charm         | Pikachu        | 0                    | Fairy             |
            | Sweet Kiss    | Pikachu        | 0                    | Fairy             |
        """)

    # def test_split_tables(self):

    #     expected = [
    #         self.t.restrict(('Attack Type',), lambda at: at == 'Electric'),
    #         self.t.restrict(('Attack Type',), lambda at: at == 'Fairy'),
    #         self.t.restrict(('Attack Type',), lambda at: at == 'Normal'),
    #     ]

    #     self.assertEquals(
    #         list(self.t.split(key=('Attack Type',))),
    #         expected
    #     )


if __name__ == '__main__':
    unittest.main()
