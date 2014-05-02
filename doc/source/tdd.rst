Test Driven Development
-----------------------

Toytable provides a testing mixin called TableTestMixin which can be used
to provide more helpful table output::

    import unittest
    from toytable import table_literal, TableTestMixin


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

    if __name__ == '__main__':
        unittest.main()

Toytable can be used as an alternative to Lettuce style tests. 

Testing Mixin
-------------

.. autoclass:: toytable.TableTestMixin
    :members:
    :undoc-members:
    :show-inheritance: