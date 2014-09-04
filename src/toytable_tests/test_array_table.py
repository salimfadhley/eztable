import unittest
from toytable import Table
from toytable.columns import Column, ArrayColumn

class TestArrayTable(unittest.TestCase):

    def setUp(self):
        self.t = Table([
            ('A', 'i'),
            ('B', 'u'),
            ('C', 'f'),
            ('D', int)
        ])

    def test_array_columns(self):
        self.assertIsInstance(self.t._get_column('A'), ArrayColumn)
        self.assertIsInstance(self.t._get_column('D'), Column)

    def test_append(self):
        self.t.append(
            (3, u'h', 2.2, 9)
        )


    def test_repr_column(self):
        self.t.append(
            (3, u'h', 2.5, 9)
        )

        expected = '\n'.join([
            '| A (i) | B (u) | C (f) | D (int) |',
            '| 3     | h     | 2.5   | 9       |'

        ])

        self.assertEquals(
            self.t._get_column('A').type,
            'i'
        )

        self.assertEquals(
            self.t._get_column('C').type,
            'f'
        )

        self.assertEquals(
            repr(self.t),
            expected
        )


if __name__ == '__main__':
    unittest.main()
