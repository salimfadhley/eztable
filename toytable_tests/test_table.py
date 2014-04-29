import unittest
import datetime

from toytable import Table, InvalidSchema, InvalidData


class TestTable(unittest.TestCase):

    def test_simple_table(self):
        s = [
            ('A', int),
            ('B', float),
            ('C', str)
        ]
        t = Table(s)
        self.assertEqual(s, t.schema)

    def test_column_types(self):
        s = [
            ('A', int),
            ('B', float),
            ('C', str),
            ('D', datetime.datetime),
            'F'
        ]
        t = Table(s)
        self.assertEqual(
            t.column_types,
            [int, float, str, datetime.datetime, object]
        )

    def test_formatted_column_descriptions(self):
        s = [
            ('A', int),
            ('B', float),
            ('C', str),
            ('D', datetime.datetime),
            'E'
        ]
        t = Table(s)
        self.assertEqual(
            t._column_descriptions,
            ['A (int)',
             'B (float)',
             'C (str)',
             'D (datetime.datetime)',
             'E']
        )

    def test_append_row(self):
        t = Table([
            ('A', int),
            ('B', float),
            ('C', str),
        ])
        t.append([1, 2.2, 'hello'])
        self.assertEqual(list(t), [(1, 2.2, 'hello')])

    def test_extend_rows(self):
        t = Table([
            ('A', int),
            ('B', float),
            ('C', str),
        ])
        t.extend([
            [1, 1.1, 'hello'],
            [2, 2.2, 'goodbye']
        ])

        self.assertEqual(len(t), 2)

    def test_append_invalid_row(self):
        t = Table([
            ('A', int),
            ('B', float),
            ('C', str),
        ])

        with self.assertRaises(InvalidData):
            t.append([2, 2.2, int])

    def test_extend_invalid_rows(self):
        t = Table([
            ('A', int),
            ('B', float),
            ('C', str),
        ])

        with self.assertRaises(InvalidData):
            t.extend([
                [1, 1.1, 0],
            ])

    def test_append_invalid_row2(self):
        t = Table([
            ('A', int),
            ('B', float),
            ('C', int),
        ])
        with self.assertRaises(InvalidData):
            t.append([1, 2.2, 'hello'])

    def test_nones_always_valid(self):
        t = Table([
            ('A', int),
            ('B', float),
            ('C', int),
        ])
        t.append([1, 2.2, None])

    def test_empty_table_equivalence_when_schemas_same(self):
        s = [
            ('A', int),
            ('B', float),
            ('C', int),
        ]
        t0 = Table(s)
        t1 = Table(s)

        self.assertEqual(t0, t1)

    def test_empty_table_not_equal_when_schemas_same_but_data_different(self):
        s = [
            ('A', int),
            ('B', float),
            ('C', int),
        ]
        t0 = Table(s)
        t1 = Table(s)
        t0.append([2, 2.22, 1])
        self.assertNotEqual(t0, t1)


if __name__ == '__main__':
    unittest.main()
