class TableTestMixin(object):

    """Intended to be mixed into unittests, provides
    table checking behaviors.
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
        self.__validate_table_structures(A, B)
        rows_a = set(A)
        rows_b = set(B)
        self.assertEqual(rows_a, rows_b)

    def assertTablesNotEquals(self, A, B, msg=None):
        self.assertNotEquals(A, B)

    assertTablesEquals = assertTablesEqual
