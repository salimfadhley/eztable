import unittest

from zqtable import Table, InvalidSchema, InvalidData


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

        self.assertEquals(
            t.column_names,
            ['A', 'B', 'C', 'D']
        )

        self.assertEquals(
            t[0],
            (1, 1.1, 'hello', 'X')
        )

    def test_expand_const_does_not_affect_length(self):
        t = self.t.expand_const(
            name='D',
            type=str,
            value='X'
        )
        self.assertEquals(len(t), len(self.t))

    def test_expand_const_on_project(self):
        t0 = self.t.project(['C'])
        t1 = t0.expand_const('D', 0)
        self.assertEquals(
            list(t1.D),
            [0] * len(self.t)
        )

    def test_simple_project(self):
        t = self.t.project(['A', 'C'])
        self.assertEquals(t.schema, [('A', int), ('C', str)])
        self.assertEquals(t[0], (1, 'hello'))

    def test_simple_expand(self):
        t = self.t.expand(
            name='D',
            type=int,
            input_columns=['C'],
            fn=lambda C: len(C)
        )
        self.assertEquals(list(t.D), [5, 5])

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

        self.assertEquals(list(t), expected)
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

        self.assertEquals(list(t), expected)
