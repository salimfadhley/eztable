Aggregations
============

Toytable allows the contents of a table to be grouped according to the values
of one or more column. 

Internally the aggregation function splits the main table into a number of
smaller sub-tables, according to the group-columns.

In this example we are grouping by two of the columns, and using the len
function to get the length of each resulting sub-table.

Aggregations are specified as a triple containing name, type and function.

The function must be a callable which takes a subtable as it's input
and returns a value of the type specfied in the 2nd column.

    >>> from toytable import table_literal
    >>> t = table_literal(\"\"\"
    ... | Attack(str)   | Pokemon(str) | Level Obtained(int) | Attack Type(str) |
    ... | Thunder Shock | Pikachu      | 1                   | Electric         |
    ... | Tackle        | Pikachu      | 1                   | Normal           |
    ... | Tail Whip     | Pikachu      | 1                   | Normal           |
    ... | Growl         | Pikachu      | 5                   | Normal           |
    ... | Quick Attack  | Pikachu      | 10                  | Normal           |
    ... | Thunder Wave  | Pikachu      | 13                  | Electric         |
    ... | Electro Ball  | Pikachu      | 18                  | Electric         |
    ... | Charm         | Pikachu      | 0                   | Fairy            |
    ... | Sweet Kiss    | Pikachu      | 0                   | Fairy            |
    ... \"\"\")
    >>>
    >>> agg = t.aggregate(
    ...     keys=('Pokemon', 'Attack Type'),
    ...     aggregations = [
    ...         ('Count', int, lambda t:len(t))
    ...     ]
    ... )
    >>>
    >>> print agg
    | Pokemon (str) | Attack Type (str) | Count (int) |
    | Pikachu       | Normal            | 4           |
    | Pikachu       | Electric          | 3           |
    | Pikachu       | Fairy             | 2           |
