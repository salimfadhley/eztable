import unittest
from toytable import Table
from toytable.columns import describe_column


class TestRepr(unittest.TestCase):

    def test_describe_builtins(self):
        self.assertEqual(
            describe_column('foo', int),
            'foo (int)'
        )

    def test_repr_headers(self):
        t = Table([('A', int), 'B', ('C', float)])
        self.assertEqual(
            repr(t),
            "| A (int) | B | C (float) |"
        )

    def test_repr(self):
        t = Table([('A', int), 'B', ('C', float)])
        t.extend([
            [1, "hello", 1.1],
            [2, "goodbye", 2.2],
        ])
        print(repr(t))

    def test_column_descriptions_on_join(self):
        p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
        p.extend([
            [1, 'Pikachu', 18],
        ])
        o = Table([('Owner Id', int), ('Name', str)])
        o.append([1, 'Ash Ketchum'])
        j = p.left_join(
            keys=('Owner Id',),
            other=o
        )

        self.assertEqual(
            ['Owner Id (int)', 'Pokemon', 'Level (int)', 'Name (str)'],
            j._column_descriptions
        )

    def test_get_maximum_column_widths_for_join(self):
        p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
        p.extend([
            [1, 'Pikachu', 18],
        ])
        o = Table([('Owner Id', int), ('Name', str)])
        o.append([1, 'Ash Ketchum'])
        j = p.left_join(
            keys=('Owner Id',),
            other=o
        )
        expected = [
            len(j._get_column('Owner Id').description),
            len(j._get_column('Pokemon').description),
            len(j._get_column('Level').description),
            len('Ash Ketchum'),
        ]

        widths = j._get_column_widths()

        self.assertEqual(
            expected,
            widths
        )

    def test_repr_joined_table(self):
        p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
        p.extend([
            [1, 'Pikachu', 18],
            [99, 'Mew', 43],  # Cannot be joined
        ])
        o = Table([('Owner Id', int), ('Name', str)])
        o.append([1, 'Ash Ketchum'])
        j = p.left_join(
            keys=('Owner Id',),
            other=o
        )

        expected = [
            "| Owner Id (int) | Pokemon | Level (int) | Name (str)  |",
            "| 1              | Pikachu | 18          | Ash Ketchum |",
            "| 99             | Mew     | 43          | None        |"
        ]

        for resultrow, expectedrow in zip(
            repr(j).split('\n'),
                expected):
                self.assertEqual(
                    resultrow,
                    expectedrow
                )

    def test_repr_bigger_broken_join_with_project(self):
        p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
        p.extend([
            [1, 'Pikachu', 18],
            [1, 'Bulbasaur', 22],
            [1, 'Charmander', 12],
            [3, 'Togepi', 5],
            [1, 'Starmie', 44],
            [9, 'Mew', 99],
        ])
        o = Table([('Owner Id', int), ('Name', str)])
        o.append([1, 'Ash Ketchum'])
        o.append([2, 'Brock'])
        o.append([3, 'Misty'])
        j = p.left_join(
            keys=('Owner Id',),
            other=o
        )
        j2 = j.project('Pokemon', 'Level', 'Name')
        print(repr(j2))

    def test_repr_on_expands(self):
        t = Table([('A', int), ('B', int)])
        t.append([1, 2])
        e = t.expand('C', ['A', 'B'], lambda *args: sum(args), int)
        self.assertEqual(repr(e),
                         "\n".join([
                             "| A (int) | B (int) | C (int) |",
                             "| 1       | 2       | 3       |"
                         ])
                         )

    def test_repr_on_expand_const(self):
        t = Table([('A', int), ('B', int)])
        t.append([1, 2])
        e = t.expand_const('C', 3, int)
        self.assertEqual(repr(e),
                         "\n".join([
                             "| A (int) | B (int) | C (int) |",
                             "| 1       | 2       | 3       |"
                         ])
                         )


if __name__ == '__main__':
    unittest.main()
