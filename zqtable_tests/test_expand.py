import unittest

from zqtable.table import Table, Schema, InvalidSchema, InvalidData, ExpandedTable


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
