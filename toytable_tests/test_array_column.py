import unittest
import array
from toytable import Table, table_literal
from toytable.columns import ArrayColumn



class TestArrayColumn(unittest.TestCase):
    def test_array_column(self):
        c = ArrayColumn(name='foo', type='u', values=None)
        self.assertIsInstance(c, array.array)

    def test_array_column_unpack(self):
        c = ArrayColumn(name='foo', type='i', values=[1, 2, 3, 4])
        self.assertEqual(
            list(c),
            [1, 2, 3, 4]
        )

    def test_array_column_invalid_type(self):
        with self.assertRaises(ValueError):
            ArrayColumn(name='foo', type='X', values=[1, 2, 3, 4])
        

    def test_array_column_unpack(self):
        c = ArrayColumn(name='foo', type='i')
        c.append(1)
        c.append(2)
        self.assertEqual(
            list(c),
            [1, 2, ]
        )

    def test_array_column_type_f(self):
        c = ArrayColumn(name='foo', type='f')
        c.append(2.2)
        self.assertEqual(c.type, 'f')

    def test_array_column_type_i(self):
        c = ArrayColumn(name='foo', type='i')
        c.append(3)
        self.assertEqual(c.type, 'i')

    def test_array_column_description(self):
        c = ArrayColumn(name='foo', type='f')
        c.append(2.2)
        self.assertEqual(c.description, 'foo (f)')

    def test_array_column_description_u(self):
        c = ArrayColumn(name='foo', type='u')
        c.append(u'j')
        self.assertEqual(c.description, 'foo (u)')

if __name__ == '__main__':
    unittest.main()
