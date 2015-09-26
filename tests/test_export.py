import unittest
from six import StringIO
from eztable import TableTestMixin
from eztable import Table
import csv


class TestExport(unittest.TestCase, TableTestMixin):

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

    def test_export_csv(self):
        output_file = StringIO()
        self.t.to_csv(output_file=output_file)
        output_file.seek(0)
        reader = csv.DictReader(output_file)
        row = next(reader)
        self.assertEqual(row, {"A":"1", "B":"0.0", "C":"x"})

    def test_export_csv_with_dialect(self):
        output_file = StringIO()
        self.t.to_csv(output_file=output_file, dialect="excel")
        output_file.seek(0)
        reader = csv.DictReader(output_file, dialect="excel")
        row = next(reader)
        self.assertEqual(row, {"A":"1", "B":"0.0", "C":"x"})

    def test_export_csv_with_dialect_types(self):
        output_file = StringIO()
        self.t.to_csv(output_file=output_file, dialect="excel", descriptions=True)
        output_file.seek(0)
        reader = csv.DictReader(output_file, dialect="excel")

        self.assertEqual(next(reader), {"A (int)":"1", "B (float)":"0.0", "C (str)":"x"})

    def test_simple_expand(self):
        t = self.t.expand(
            name='D',
            col_type=int,
            input_columns=['C'],
            fn=lambda C: len(C)
        )
        self.assertEqual(list(t.D), [1, 1, 1])


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
            input_columns=['C'],
            fn=lambda C: len(C) + 1
        ).copy()

    def test_export_csv_with_dialect_tab(self):
        output_file = StringIO()
        self.t.to_csv(output_file=output_file, dialect="excel-tab")
        output_file.seek(0)
        reader = csv.DictReader(output_file, dialect="excel-tab")
        row = next(reader)
        self.assertEqual(row, {"A":"1", "B":"0.0", "C":"x"})


    def test_simple_expand_and_slice(self):
        t = self.t.expand(
            name='D',
            col_type=int,
            input_columns=['C'],
            fn=lambda C: len(C) + 1
        )[1:2]

        expected = [
            (2, 5.0, 'y', 2),
        ]

        self.assertEqual(list(t), expected)

if __name__ == '__main__':
    unittest.main()