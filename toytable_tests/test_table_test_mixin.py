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

    def test_error_unequal_lengths(self):
        A = table_literal("""
            | A (int) | B (int) |
            | 1       | 2       |
        """)

        B = table_literal("""
            | A (int) | B (int) |
        """)

        with self.assertRaises(AssertionError) as ae:
            self.assertTablesEqual(A, B)

        self.assertTrue(
            "Table lengths are different" in ae.exception.args[0]
        )

    def test_inconsistent_column_names(self):
        A = table_literal("""
            | A (int) | B (int) |
            | 1       | 2       |
        """)

        B = table_literal("""
            | A (int) | B (int) | D (str) |
        """)

        with self.assertRaises(AssertionError) as ae:
            self.assertTablesEqual(A, B)

        self.assertTrue(
            "Column names are different" in ae.exception.args[0]
        )

    def test_inconsitent_column_types(self):
        A = table_literal("""
            | A (int) | B (int) | D (float) |
            | 1       | 2       | 2.2       |
        """)

        B = table_literal("""
            | A (int) | B (int) | D (str) |
        """)

        with self.assertRaises(AssertionError) as ae:
            self.assertTablesEqual(A, B)

        self.assertTrue(
            "Column types are different" in ae.exception.args[0]
        )

    def test_detect_first_dfferent_row(self):
        A = table_literal("""
            | A (int) | B (int) | D (float) |
            | 1       | 2       | 2.2       |
            | 1       | 2       | 2.1       |
        """)

        B = table_literal("""
            | A (int) | B (int) | D (float) |
            | 1       | 2       | 2.2       |
            | 1       | 2       | 2.3       |
        """)

        with self.assertRaises(AssertionError) as ae:
            self.assertTablesEqual(A, B)

        self.assertTrue(
            "Differences at row 1" in ae.exception.args[0],
            ae.exception.args[0]
        )

    def test_assert_equal_any_order(self):
        A = table_literal("""
            | A (int) | B (int) | D (float) |
            | 1       | 2       | 1.1       |
            | 1       | 2       | 2.2       |
        """)

        B = table_literal("""
            | A (int) | B (int) | D (float) |
            | 1       | 2       | 2.2       |
            | 1       | 2       | 1.1       |
        """)

        self.assertTablesEqualAnyOrder(A, B)

    def test_assert_equal_any_order(self):
        A = table_literal("""
            | A (int) | B (int) | D (float) |
            | 1       | 2       | 1.1       |
            | 1       | 2       | 9.9       |
        """)

        B = table_literal("""
            | A (int) | B (int) | D (float) |
            | 1       | 2       | 2.2       |
            | 1       | 2       | 1.1       |
        """)

        with self.assertRaises(AssertionError):
            self.assertTablesEqualAnyOrder(A, B)


if __name__ == '__main__':
    unittest.main()
