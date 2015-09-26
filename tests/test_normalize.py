import unittest
from eztable import TableTestMixin
from eztable import table_literal
from eztable import Table


class TestNormalize(unittest.TestCase, TableTestMixin):

    def setUp(self):
        self.s = [
            ('A', int),
            ('B', float),
            ('C', str),
        ]
        self.t = Table(self.s)

        self.t.extend([
            [1, 0.0, 'x'],
            [2, 5.0, 'y'],
            [3, 10.0, 'z'],
        ])

    def test_basic_normalize(self):
        t = self.t.normalize({"B":1.0})
        self.assertEqual(list(t.B), [0, 0.5, 1])

    def test_basic_standardization(self):
        t = self.t.standardize({"B":1.0})
        result = list(t.B)
        self.assertEqual(result[1], 0)
        self.assertEqual(result[0], result[2]*-1)

    def test_whole_of_normalized_table(self):
        tn = self.t.normalize({"B":1.0})

        expected = table_literal("""
        | A (int) | B (float) | C (str) |
        | 1       | 0         | x       |
        | 2       | 0.5       | y       |
        | 3       | 1.0       | z       |
        """)

    def test_whole_of_normalized_table_100(self):
        tn = self.t.normalize({"B":100})

        expected = table_literal("""
        | A (int) | B (float) | C (str) |
        | 1       | 0         | x       |
        | 2       | 50        | y       |
        | 3       | 100       | z       |
        """)

        self.assertTablesEqual(tn, expected)

    def test_expand_of_normalized_table(self):
        tn = self.t.normalize({"B":1.0}).expand(
            name='D',
            col_type=float,
            input_columns=['A','B'],
            fn=lambda A,B: A * B
        )

        expected = table_literal("""
        | A (int) | B (float) | C (str) | D (float) |
        | 1       | 0         | x       | 0.0       |
        | 2       | 0.5       | y       | 1.0       |
        | 3       | 1.0       | z       | 3.0       |
        """)

        self.assertTablesEqual(tn, expected)


    def test_simple_expand(self):
        t = self.t.expand(
            name='D',
            col_type=int,
            input_columns=['C'],
            fn=lambda C: len(C)
        )
        self.assertEqual(list(t.D), [1,1,1])

    def test_derived_columns_are_iterable(self):
        t = self.t.expand(
            name='D',
            col_type=int,
            input_columns=['C'],
            fn=lambda C: len(C)
        )
        for _ in t.D:
            pass

    def test_derived_columns_can_be_printed(self):
        t = self.t.expand(
            name='D',
            col_type=int,
            input_columns=['C'],
            fn=lambda C: len(C)
        )
        str(t.D)
        repr(t.D)

    def test_derived_columns_have_descriptions(self):
        t = self.t.expand(
            name='D',
            col_type=int,
            input_columns=['C'],
            fn=lambda C: len(C)
        )
        self.assertEqual(t.D.description, "D (int)")

    def test_that_float_columns_have_descriptions(self):
        t = self.t.expand(
            name='D',
            input_columns=['A', 'B', 'C'],
            fn=lambda a,b,c: float(len(c) + a + b),
            col_type=float
        )
        self.assertEqual(t.D.description, "D (float)")

    def test_simple_expand_and_materialize(self):
        t = self.t.expand(
            name='D',
            col_type=int,
            input_columns=['A', 'C'],
            fn=lambda A, C: len(C) + A
        ).copy()

        expected = [
            (1, 0.0, 'x', 2),
            (2, 5.0, 'y', 3),
            (3, 10.0, 'z', 4),
        ]

        self.assertEqual(list(t), expected)
        self.assertIsInstance(t, Table)

    def test_simple_expand_and_slice(self):
        t = self.t.expand(
            name='D',
            col_type=int,
            input_columns=['C'],
            fn=lambda C: len(C) + 2
        )[1:2]

        expected = [
            (2, 5.0, 'y', 3),
        ]

        self.assertEqual(list(t), expected)

if __name__ == '__main__':
    unittest.main()