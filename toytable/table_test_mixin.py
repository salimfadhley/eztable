class TableTestMixin(object):
    """Mix this class into any unit test test-cases in order
    to add methods for asserting equality on toytable objects.

    Typically the class definition for a unittest will look
    something like this::

        class ExampleTestCase(TableTestMixin, unittest.TestCase):
            ...
    """

    def __validate_table_structures(self, A, B):
        self.assertEquals(
            A.column_names,
            B.column_names,
            "Column names are different")

        self.assertEquals(
            A.column_types,
            B.column_types,
            "Column types are different")

        if len(A) != len(B):
            raise AssertionError(
                "Table lengths are different: %i != %i" % 
                (len(A), len(B))
            )

    def assertTablesEqual(self, A, B, msg=None):
        """Verfy that two tables are exactly equal.
        Raises an AssertionError if not.
        """
        self.__validate_table_structures(A, B)
        for i, (a, b) in enumerate(zip(A, B)):
            if not a == b:
                brokenA = A[i:i + 1]
                brokenB = B[i:i + 1]

                _msg = 'Differences at row %i\n\n%r\n\n%s' % (
                    i,
                    brokenA,
                    brokenB
                )
                raise AssertionError(_msg)

    def assertTablesEqualAnyOrder(self, A, B, msg=None):
        """Verify that two tables contain the exact same
        set of rows. Rows may be in any order.
        Raises an AssertionError the sets of rows are different.
        """
        self.__validate_table_structures(A, B)
        rows_a = set(A)
        rows_b = set(B)
        self.assertEqual(rows_a, rows_b)

    def assertTablesNotEquals(self, A, B, msg=None):
        """Verify that two tables are not equal.
        Raises an AssertionError if the two tables are equal.
        """
        self.assertNotEquals(A, B)

    assertTablesEquals = assertTablesEqual
