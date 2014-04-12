import unittest

from zqtable.schema import ColMeta, InvalidColumn, Schema


class TestSchema(unittest.TestCase):

    def testColumnMetadata(self):
        cm = ColMeta('A', int)

    def testInvalidSchemaBadName(self):
        with self.assertRaises(InvalidColumn):
            ColMeta(3, int)

    def testInvalidSchemaBadTyoe(self):
        with self.assertRaises(InvalidColumn):
            ColMeta('Hello', 3)

    def testValidateValueForColumn(self):
        col = ColMeta('Hello', int)
        self.assertTrue(col.validate(3))

    def testValidateForColumnInvalid(self):
        col = ColMeta('Hello', int)
        self.assertFalse(col.validate(3.333))

    def testSimpleSchema(self):
        s = Schema(('A', int), ('B', float))
        self.assertEquals(s[0], ColMeta('A', int))

    def testSimpleSchemaSecondElement(self):
        s = Schema(('A', int), ('B', float))
        self.assertEquals(s[1], ColMeta('B', float))

    def testValidateValueForNone(self):
        col = ColMeta('Hello', int)
        self.assertTrue(col.validate(None))

    def testValidateForNoneAllowed(self):
        col = ColMeta('Hello', int, allow_none=False)
        self.assertFalse(col.validate(None))

    def testValidateRow(self):
        s = Schema(('A', int), ('B', float))
        self.assertTrue(s.validate([3, 3.333]))

    def testInvalidRowLength(self):
        s = Schema(('A', int), ('B', float, False))
        self.assertFalse(s.validate([3, ]))

    def testRowLengthWhenNonesAllowed(self):
        s = Schema(('A', int), ('B', float))
        self.assertTrue(s.validate([3, ]))

    def testCanOnlyPutColsInSchema(self):
        s = Schema(('A', int), ('B', float))
        with self.assertRaises(InvalidColumn):
            s.append('honey boo boo')

    def testStr(self):
        s = Schema(('A', int), ('B', float))
        self.assertTrue(str(s[0]) in str(s))

    def testRepr(self):
        s = Schema(('A', int), ('B', float))
        self.assertTrue(str(s[0]) in repr(s))


    def testSchemaConcat(self):
        a = Schema(('A', int))
        b = Schema(('B', str))
        s = Schema(('A', int), ('B', str))

        self.assertEquals(a + b, s)


if __name__ == '__main__':
    unittest.main()
