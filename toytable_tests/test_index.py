import unittest
from toytable import Table, InvalidIndex


class TestIndex(unittest.TestCase):

    def setUp(self):
        self.s = ['A', 'B', 'C']
        self.t = Table(self.s)

        self.t.extend([
            (1, 1.1, 'hello'),
            (2, 2.2, 'goodbye'),
            (3, 3.3, 'yaloo'),
            (4, 4.4, 'fnuu'),
            (5, 6.4, 'Animal Crossing'),
        ])

    def test_indexes_must_have_at_least_one_col(self):
        with self.assertRaises(InvalidIndex):
            self.t.add_index([])

    def test_can_only_index_columns_which_exist(self):
        with self.assertRaises(InvalidIndex):
            self.t.add_index(['ZQx9'])

    def test_there_can_be_only_one(self):
        i = self.t.add_index(
            cols=('A', 'C')
        )

        j = self.t.add_index(
            cols=('A', 'C')
        )

        self.assertTrue(i is j)

    def test_indexes_have_reprs(self):
        i = self.t.add_index(
            cols=('A', 'C')
        )
        expected_str = 'A,C'
        expected_repr = '<toytable.index.Index %s>' % expected_str

        self.assertEquals(str(i), expected_str)
        self.assertEquals(repr(i), expected_repr)

    def test_create_and_destroy_index(self):
        """Verify that indexes can be both created, detected and removed.

        For the correct plural of index see:
        http://grammarist.com/usage/indexes-indices/
        """
        self.assertEquals(len(self.t.indexes), 0)
        i = self.t.add_index(
            cols=('A', 'C')
        )

        self.assertTrue(('A', 'C') in self.t.indexes)
        self.assertIn(i, self.t._listeners)

        # Indexes are automatically deleted when references
        # are destroyed
        i = None
        self.assertFalse('my_first_index' in self.t.indexes)
        self.assertFalse(i in self.t._listeners)

    def test_indexes_can_be_hashed(self):
        i = self.t.add_index(
            cols=('A', 'C')
        )
        self.assertIsInstance(hash(i), int)

    def test_indexes_start_out_empty(self):
        i = self.t.add_index(
            cols=('A', 'C')
        )
        self.assertEquals(len(i), 0)

    def test_indexes_can_receive_events(self):
        i = self.t.add_index(
            cols=('A', 'C')
        )
        i.notify(
            op='do_nothing!',
            pos=0,
        )

    def test_adding_to_a_table_adds_to_indexes(self):
        i = self.t.add_index(
            cols=('A', 'C')
        )
        self.t.append((6, 7.4, 'Starfox Adventures'))
        self.assertEquals(len(i), 1)

    def test_indexes_can_be_reindexed(self):
        i = self.t.add_index(
            cols=('C')
        )
        i.reindex()
        self.assertEquals(len(i), len(self.t))

    def test_indexes_can_be_used_to_look_things_up(self):
        i = self.t.add_index(
            cols=('C')
        )
        i.reindex()

        self.assertEquals(
            i[('fnuu',)][0],
            self.t[3]
        )

    def test_indexes_can_be_used_to_locate_a_record(self):
        i = self.t.add_index(
            cols=('C')
        )
        i.reindex()

        self.assertEquals(
            i.index(('fnuu',))[0],
            3
        )

if __name__ == '__main__':
    unittest.main()
