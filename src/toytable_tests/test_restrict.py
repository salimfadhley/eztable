import unittest
from toytable import Table


class TestRestrict(unittest.TestCase):

    def setUp(self):
        self.s = ['A', 'B', 'C']
        self.t = Table(self.s)

        self.t.extend([
            (1, True, 'charmander'),
            (2, False, 'bulbasaur'),
            (3, True, 'squirtle'),
            (4, True, 'pikachu'),
            (5, False, 'butterfree'),
        ])

    def test_restrict_with_materialize(self):
        r = self.t.restrict(
            col_names=('B'),
            fn=lambda b: b
        )

        # We also need to be able to do this
        # operation without a materilize!
        self.assertEquals(
            list(r.copy().A),
            [1, 3, 4]
        )

    def test_restrict_without_materialize(self):
        r = self.t.restrict(
            col_names=('B'),
            fn=lambda b: b
        )

        # No copy operation
        self.assertEquals(
            list(r.A),
            [1, 3, 4]
        )

    def test_that_restricted_columns_are_consistent(self):
        r = self.t.restrict(
            col_names=('B'),
            fn=lambda b: b
        )

        self.assertEquals(len(r), len(r.A))

        self.assertEquals(
            list(r),
            list(zip(list(r.A),
                     list(r.B),
                     list(r.C)
                     ))

        )


if __name__ == '__main__':
    unittest.main()
