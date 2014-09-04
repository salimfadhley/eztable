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

    def test_row_keyerror(self):
        t = table_literal("""
            | A (int) | B (str) |
            | 3       |   hello |
        """)
        r = t[0]

        with self.assertRaises(KeyError):
            r['X']

    def test_row_attributerror(self):
        t = table_literal("""
            | A (int) | B (str) |
            | 3       |   hello |
        """)
        r = t[0]

        with self.assertRaises(AttributeError):
            r.X

    def test_keys_on_regular_columns(self):
        t = table_literal("""
            | A (i) | B (f) |
            | 3     | 2.2   |
        """)
        r = t[0]
        self.assertEquals(
            r.keys(),
            ('A', 'B')
        )

    def test_keys_on_array_columns(self):
        t = table_literal("""
            | A (int) | B (str) |
            | 3     |   hello   |
        """)
        r = t[0]
        self.assertEquals(
            r.keys(),
            ('A', 'B')
        )

    def test_values(self):
        t = table_literal("""
            | A (i) | B (str) |
            | 3     |   hello |
        """)
        r = t[0]
        self.assertEquals(
            r.values(),
            [3, 'hello']
        )

    def test_items(self):
        t = table_literal("""
            | A (i) | B (str) |
            | 3     |   hello |
        """)
        r = t[0]

        self.assertEquals(
            list(r.items()),
            [('A', 3), ('B', 'hello')]
        )


if __name__ == '__main__':
    unittest.main()
