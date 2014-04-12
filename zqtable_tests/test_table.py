import unittest

from zqtable.table import Table, Schema, InvalidSchema, InvalidData

class TestTable(unittest.TestCase):

    def test_simple_table(self):
        s = Schema(
                ('A', int),
                ('B', float),
                ('C', str),
            )
        t = Table(s)
        self.assertEquals(s, t.schema)

    def test_invalid_schema(self):
        with self.assertRaises(InvalidSchema):
            Table('Hello')

    def test_append_row(self):
        s = Schema(
                ('A', int),
                ('B', float),
                ('C', str),
            )
        t = Table(s)
        t.append([1, 2.2, 'hello'])

    def test_extend_rows(self):
        t = Table(Schema(
            ('A', int),
            ('B', float),
            ('C', str),
        ))
        t.extend([
            [1, 1.1, 'hello'],
            [2, 2.2, 'goodbye']
        ])
        self.assertEquals(len(t), 2)

    def test_append_invalid_row(self):
        t = Table(Schema(
            ('A', int),
            ('B', float),
            ('C', str),
        ))

        with self.assertRaises(InvalidData):
            t.append([2, 2.2, int])

    def test_extend_invalid_rows(self):
        t = Table(Schema(
            ('A', int),
            ('B', float),
            ('C', str),
        ))

        with self.assertRaises(InvalidData):
            t.extend([
                [1, 1.1, 0],
            ])

    def test_append_invalid_row(self):
        s = Schema(
                ('A', int),
                ('B', float),
                ('C', int),
            )
        t = Table(s)
        with self.assertRaises(InvalidData):
            t.append([1, 2.2, 'hello'])


