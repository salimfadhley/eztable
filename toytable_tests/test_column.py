import array
import unittest
from toytable.columns import Column, ArrayColumn


class TestColumn(unittest.TestCase):

    def test_column(self):
        """A column can be constructed with no data."""
        c = Column('foo')
        self.assertEqual(list(c), [])

    def test_column_data(self):
        """A column can be constructed with initial data."""
        c = Column('foo', range(3))
        self.assertEqual(list(c), [0, 1, 2])

    def test_column_type(self):
        """A column can be constructed specifying a type."""
        c = Column('foo', range(3), type=int)
        self.assertEqual(list(c), [0, 1, 2])

    def test_array_column(self):
        c = ArrayColumn(name='foo', type='u', values=None)
        self.assertIsInstance(c, array.array)

    def test_array_column_unpack(self):
        c = ArrayColumn(name='foo', type='i', values=[1,2,3,4])
        self.assertEqual(
            list(c),
            [1,2,3,4]
        )

    def test_array_column_invalid_type(self):
        with self.assertRaises(ValueError):
            ArrayColumn(name='foo', type='X', values=[1,2,3,4])
        

    def test_array_column_unpack(self):
        c = ArrayColumn(name='foo', type='i')
        c.append(1)
        c.append(2)
        self.assertEqual(
            list(c),
            [1,2,]
        )

    def test_array_column_type(self):
        c = ArrayColumn(name='foo', type='f')
        c.append(2.2)
        self.assertEqual(c.type, 'f')



if __name__ == '__main__':
    unittest.main()
