import unittest
from toytable import table_literal


class TestRow(unittest.TestCase):

    def test_row_can_be_cast_to_tuple(self):
        t = table_literal("""
            | A (int) | B (str) |
            | 3       |   hello |
        """)
        r = t[0]
        self.assertEquals(
            tuple(r),
            (3, "hello")
        )

    def test_row_can_be_accessed_like_a_tuple(self):
        t = table_literal("""
            | A (int) | B (str) |
            | 3       |   hello |
        """)
        r = t[0]
        self.assertEquals(r[0], 3)
        self.assertEquals(r[1], 'hello')

    def test_row_can_be_accessed_by_names(self):
        t = table_literal("""
            | A (int) | B (str) |
            | 3       |   hello |
        """)
        r = t[0]
        self.assertEquals(r['A'], 3)
        self.assertEquals(r['B'], 'hello')

if __name__ == '__main__':
    unittest.main()
