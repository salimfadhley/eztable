import unittest
from eztable import table_literal, TableTestMixin


class ExampleTest(TableTestMixin, unittest.TestCase):

    """An example of how to do test-driven
    development with toytable.
    """

    def test_foo(self):
        t0 = table_literal("""
            | A (int) | B (int) | C (str) |
            | 1       | 2       | 3       |
            | 2       | 3       | 4       |
        """)

        t1 = table_literal("""
            | A (int) | B (int) | C (str) |
            | 1       | 2       | 3       |
            | 999     | 3       | 4       |
        """)

        self.assertTablesEqual(t0, t1)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
