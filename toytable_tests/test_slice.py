import unittest
from toytable import Table, InvalidSchema, InvalidData


class TestTableRowAccess(unittest.TestCase):

    def setUp(self):
        self.s = [
            ('A', int),
            ('B', float),
            ('C', str),
        ]
        self.t = Table(self.s)

        self.t.extend([
            (1, 1.1, 'hello'),
            (2, 2.2, 'goodbye'),
            (3, 3.3, 'yaloo'),
            (4, 4.4, 'fnuu'),
        ])

    def test_basic_slice(self):
        t = self.t[0:2:]
        self.assertEqual(len(t), 2)
        self.assertEqual(t.schema, self.s)

    def test_get_row(self):
        self.assertEqual(
            self.t[0],
            (1, 1.1, 'hello')
        )

    def test_get_sliced_row(self):
        t = self.t[1:]
        self.assertEqual(
            t[0],
            (2, 2.2, 'goodbye'),
        )

    def test_get_sliced_row_reverse(self):
        t = self.t[::-1]
        self.assertEqual(
            t[0],
            (4, 4.4, 'fnuu'),
        )

    def test_get_sliced_row_indexerror(self):
        t = self.t[1:]
        with self.assertRaises(IndexError):
            t[3]
