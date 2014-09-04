import unittest

from toytable import Table, InvalidSchema, InvalidData


class TestExpandTable(unittest.TestCase):

    def setUp(self):
        self.s = [
            ('A', int),
            ('B', float),
            ('C', str),
        ]
        self.t = Table(self.s)

        self.t.extend([
            [1, 1.1, 'hello'],
            [2, 2.2, 'yello'],
        ])

    def test_expand_const(self):
        t = self.t.expand_const(
            name='D',
            value='X',
            type=str
        )

        self.assertEqual(
            t.column_names,
            ['A', 'B', 'C', 'D']
        )

        self.assertEqual(
            t[0],
            (1, 1.1, 'hello', 'X')
        )

    def test_expand_const_does_not_affect_length(self):
        t = self.t.expand_const(
            name='D',
            type=str,
            value='X'
        )
        self.assertEqual(len(t), len(self.t))

    def test_simple_expand(self):
        t = self.t.expand(
            name='D',
            type=int,
            input_columns=['C'],
            fn=lambda C: len(C)
        )
        self.assertEqual(list(t.D), [5, 5])

    def test_simple_expand_and_materialize(self):
        t = self.t.expand(
            name='D',
            type=int,
            input_columns=['C'],
            fn=lambda C: len(C) + 1
        ).copy()

        expected = [
            (1, 1.1, 'hello', 6),
            (2, 2.2, 'yello', 6),
        ]

        self.assertEqual(list(t), expected)
        self.assertIsInstance(t, Table)

    def test_simple_expand_and_slice(self):
        t = self.t.expand(
            name='D',
            type=int,
            input_columns=['C'],
            fn=lambda C: len(C) + 1
        )[1:]

        expected = [
            (2, 2.2, 'yello', 6),
        ]

        self.assertEqual(list(t), expected)

if __name__ == '__main__':
    unittest.main()
