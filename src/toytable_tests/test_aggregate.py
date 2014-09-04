import unittest
from toytable import table_literal, TableTestMixin
from toytable.table import AggregationTable
from toytable.row import TableRow


class TestAggregate(TableTestMixin, unittest.TestCase):

    """Verify the correctness of aggegation functions.
    """

    def setUp(self):
        self.t = table_literal("""
            | Attack (str)  | Pokemon (str)  | Level Obtained (int) | Attack Type (str) |
            | Thunder Shock | Pikachu        | 1                    | Electric          |
            | Tackle        | Pikachu        | 1                    | Normal            |
            | Tail Whip     | Pikachu        | 1                    | Normal            |
            | Growl         | Pikachu        | 5                    | Normal            |
            | Quick Attack  | Pikachu        | 10                   | Normal            |
            | Thunder Wave  | Pikachu        | 13                   | Electric          |
            | Electro Ball  | Pikachu        | 18                   | Electric          |
            | Charm         | Pikachu        | 0                    | Fairy             |
            | Sweet Kiss    | Pikachu        | 0                    | Fairy             |
        """)

    def test_get_unique_values_from_index(self):
        i = self.t.add_index(('Pokemon', 'Attack Type')).reindex()
        self.assertEquals(
            i.unique_values(),
            set([('Pikachu', 'Electric'),
                ('Pikachu', 'Normal'), ('Pikachu', 'Fairy')])
        )

    def test_get_iterator_for_value(self):
        i = self.t.add_index(('Pokemon', 'Attack Type')).reindex()
        result = i._get_iterator_fn_for_value(('Pikachu', 'Electric'))
        self.assertEquals(
            list(result()),
            [0, 5, 6]
        )

    def test_get_key_and_subtable(self):
        agg = self.t.aggregate(
            keys=('Pokemon', 'Attack Type'),
            aggregations=[
                ('Count', int, lambda t:len(t))
            ]
        )
        gen = agg._iter_subtables()
        expected = table_literal("""
            | Attack (str)  | Pokemon (str)  | Level Obtained (int) | Attack Type (str) |
            | Tackle        | Pikachu        | 1                    | Normal            |
            | Tail Whip     | Pikachu        | 1                    | Normal            |
            | Growl         | Pikachu        | 5                    | Normal            |
            | Quick Attack  | Pikachu        | 10                   | Normal            |
            """
        )
        for (k, st) in gen:
            if k == ('Pikachu', 'Normal'):
                st = st.copy()
                self.assertTablesEqualAnyOrder(st, expected)

    def simple_aggregate(self):

        expected = table_literal("""
            | Pokemon (str) | Attack Type (str) | Count (int) |
            | Pikachu       | Normal            | 4           |
            | Pikachu       | Electric          | 3           |
            | Pikachu       | Fairy             | 2           |
        """)

        agg = self.t.aggregate(
            keys=('Pokemon', 'Attack Type'),
            aggregations=[
                ('Count', int, lambda t:len(t))
            ]
        )

        self.assertEquals(
            agg.column_names,
            ['Pokemon',
             'Attack Type',
             'Count'])

        self.assertEquals(
            agg.column_types,
            [str, str, int]
        )

        self.assertTablesEqualAnyOrder(
            agg,
            expected
        )

    def test_aggregate_indices_func(self):

        agg = self.t.aggregate(
            keys=('Pokemon', 'Attack Type'),
            aggregations=[
                ('Count', int, lambda t:len(t))
            ]
        )

        self.assertEquals(
            list(agg._indices_func()),
            [0, 1, 2]
        )

    def test_get_schema(self):
        t = self.t.aggregate(
            keys=('Pokemon', 'Attack Type'),
            aggregations=[
                ('Count', int, lambda t:len(t))
            ]
        )

        schema = t.schema

        self.assertEquals(
            schema,
            [
                ('Pokemon', str),
                ('Attack Type', str),
                ('Count', int)
            ])

    def test_get_row(self):
        agg = self.t.aggregate(
            keys=('Pokemon', 'Attack Type'),
            aggregations=[
                ('Count', int, lambda t:len(t))
            ]
        )

        self.assertTrue(
            ('Pikachu', 'Normal', 4) in list(agg)

        )

    def test_correct_row_type(self):
        agg = self.t.aggregate(
            keys=('Pokemon', 'Attack Type'),
            aggregations=[
                ('Count', int, lambda t:len(t))
            ]
        )
        self.assertIsInstance(agg[0], TableRow)

    def test_iter(self):
        agg = self.t.aggregate(
            keys=('Pokemon', 'Attack Type'),
            aggregations=[
                ('Count', int, lambda t:len(t))
            ]
        )
        self.assertEquals(
            set(agg),
            set([
                ('Pikachu', 'Normal', 4),
                ('Pikachu', 'Electric', 3),
                ('Pikachu', 'Fairy', 2)
                ])

        )

    def test_column_descriptions(self):
        agg = self.t.aggregate(
            keys=('Pokemon', 'Attack Type'),
            aggregations=[
                ('Count', int, lambda t:len(t)),
                ('Hello', str, lambda t:'hello'),
            ]
        )
        self.assertEquals(
            agg._column_descriptions,
            ['Pokemon (str)',
             'Attack Type (str)',
             'Count (int)',
             'Hello (str)'
             ])

    def test_repr(self):

        lines = [
            "| Pokemon (str) | Attack Type (str) | Count (int) |",
            "| Pikachu       | Normal            | 4           |",
            "| Pikachu       | Electric          | 3           |",
            "| Pikachu       | Fairy             | 2           |"
        ]

        agg = self.t.aggregate(
            keys=('Pokemon', 'Attack Type'),
            aggregations=[
                ('Count', int, lambda t:len(t))
            ]
        )

        self.assertEquals(
            set(repr(agg).split('\n')),
            set(lines)
        )

if __name__ == '__main__':
    unittest.main()

