import unittest
import datetime
from toytable import Table
from toytable import table_literal
from toytable.table_literal import parse_column_string, col_tuple_to_schema_item


class TestTableLiteral(unittest.TestCase):

    def test_table_literal_one_row(self):
        t = table_literal("""
        | A | B | C |
        | 1 | 2 | 3 |
        """, default_type=int)
        self.assertIsInstance(t, Table)

    def test_table_literal_one_row(self):
        t = table_literal("""
        | A | B | C | D |
        | 1 | 2 | 3 | 4 |
        """, default_type=int)

        self.assertEquals(
            t.column_names,
            ['A', 'B', 'C', 'D']
        )

    def test_table_literal_columns_can_have_whitespace(self):
        t = table_literal("""
        | Attack Type (str) | Special Def (int) |
        | Fire              | 2                 |
        """)

        self.assertEquals(
            t.column_names,
            ['Attack Type', 'Special Def']
        )

    def test_parse_column_expression(self):
        self.assertEquals(
            ('foo', 'bar.baz'),
            parse_column_string('foo (bar.baz)')
        )

    def test_parse_column_expression_without_type(self):
        self.assertEquals(
            ('foo', None),
            parse_column_string('foo')
        )

    def test_convert_col_tuple_to_schema(self):
        self.assertEquals(
            col_tuple_to_schema_item(('foo', None), default_type='ssqsswws'),
            ('foo', 'ssqsswws')
        )

    def test_convert_col_tuple_to_schema_with_type(self):
        self.assertEquals(
            col_tuple_to_schema_item(('foo', 'int')),
            ('foo', int)
        )

    def test_convert_col_tuple_to_schema_with_type(self):
        self.assertEquals(
            col_tuple_to_schema_item(('bar', 'str')),
            ('bar', str)
        )

    def test_convert_col_tuple_to_schema_with_type(self):
        self.assertEquals(
            col_tuple_to_schema_item(
                ('bof', 'datetime.datetime'), default_type='zzzzz'),
            ('bof', datetime.datetime)
        )

    def test_table_literal_one_row_with_types(self):
        t = table_literal("""
        | A (int) | B (float) | C (bool) | D (int) |
        | 1       | 2.2       | True     | 4       |
        """)
        self.assertEquals(
            t.column_names,
            ['A', 'B', 'C', 'D']
        )

        self.assertEquals(
            t[0],
            (1, 2.2, True, 4)

        )


if __name__ == '__main__':
    unittest.main()
