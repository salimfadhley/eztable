import unittest

from zqtable.table import Table, Schema, InvalidSchema, InvalidData, ExpandedTable, SlicedTable


class TestExpandTable(unittest.TestCase):

    def setUp(self):
        self.s = Schema(
            ('A', int),
            ('B', float),
            ('C', str),
        )
        self.t = Table(self.s)

        self.t.extend([
            [1, 1.1, 'hello'],
            [2, 2.2, 'yello'],
        ])

    def test_expand_const(self):

        t = self.t.expand_const(
            column_name='D',
            column_type=str,
            value='X'
        )

        self.assertIsInstance(t, ExpandedTable)

        self.assertEquals(
            t.schema.column_names,
            ['A', 'B', 'C', 'D']
        )

        self.assertEquals(
            t[0],
            [1, 1.1, 'hello', 'X']
        )

    def test_expand_const_does_not_affect_length(self):
        t = self.t.expand_const(
            column_name='D',
            column_type=str,
            value='X'
        )
        self.assertEquals(len(t), len(self.t))

    def test_expand_const_on_project(self):
        t0 = self.t.project(['C'])
        t1 = t0.expand_const('D', int, 0)
        self.assertEquals(
            t1.D.to_list(),
            [0] * len(self.t)
        )

    def test_simple_project(self):
        t = self.t.project(['A', 'C'])
        self.assertEquals(t.schema.column_names, ['A', 'C'])
        self.assertEquals(t.schema.column_types, [int, str])
        self.assertEquals(t.column_order(['A', 'C']), [0, 2])
        self.assertEquals(t._projected_column_order(), [0, 2])
        self.assertEquals(t[0], [1, 'hello'])

    def test_simple_expand(self):
        t = self.t.expand(
            column_name='D',
            column_type=int,
            input_columns=['C'],
            fn=lambda C: len(C)
        )
        self.assertEquals(t.D.to_list(), [5, 5])

    def test_simple_expand_and_materialize(self):
        t = self.t.expand(
            column_name='D',
            column_type=int,
            input_columns=['C'],
            fn=lambda C: len(C) + 1
        ).materialize()

        expected = [
            [1, 1.1, 'hello', 6],
            [2, 2.2, 'yello', 6],
        ]

        self.assertEquals(t.to_list(), expected)
        self.assertIsInstance(t, Table)

    def test_simple_expand_and_slice(self):
        t = self.t.expand(
            column_name='D',
            column_type=int,
            input_columns=['C'],
            fn=lambda C: len(C) + 1
        )[1:]

        expected = [
            [2, 2.2, 'yello', 6],
        ]

        self.assertIsInstance(t, SlicedTable)
        self.assertEquals(t.to_list(), expected)
