class TableTestMixin(object):

    """Intended to be mixed into unittests, provides
    table checking behaviors.
    """

    def assertTablesEqual(self, A, B, msg=None):
        self.assertEquals(A, B)

    def assertTablesNotEquals(self, A, B, msg=None):
        self.assertNotEquals(A, B)

    assertTablesEquals = assertTablesEqual
