import unittest

from toytable import TableTestMixin, table_literal


class TestTableTestMixin(unittest.TestCase, TableTestMixin):

    def test_equal_tables(self):
        A = table_literal("""
            | A (int) | B (int) |
            | 1       | 2       |
        """)
        self.assertTablesEqual(A, A)
        self.assertTablesEquals(A, A)

        with self.assertRaises(AssertionError):
            self.assertTablesNotEquals(A, A)

    def test_unequal_tables(self):
        A = table_literal("""
            | A (int) | B (int) |
            | 1       | 2       |
        """)

        B = table_literal("""
            | A (int) | B (int) |
            | 2       | 3       |
        """)

        with self.assertRaises(AssertionError):
            self.assertTablesEqual(A, B)


if __name__ == '__main__':
    unittest.main()
