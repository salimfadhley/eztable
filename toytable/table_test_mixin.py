class TableTestMixin(object):

    """Intended to be mixed into unittests, provides
    table checking behaviors.
    """

    def assertTablesEqual(self, A, B, msg=None):

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

        self.assertEquals(A, B)

    def assertTablesNotEquals(self, A, B, msg=None):

        self.assertNotEquals(A, B)

    assertTablesEquals = assertTablesEqual
