from unittest import TestCase
from toytable.columns import Column


class TestColumn(TestCase):

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
