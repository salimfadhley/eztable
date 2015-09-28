Aggregations
============

EZTable allows the contents of a table to be grouped according to the values
of one or more column. 

Internally the aggregation function splits the main table into a number of
smaller sub-tables, according to the group-columns.

In this example we are grouping by two of the columns, and using the len
function to get the length of each resulting sub-table.

Aggregations are specified as a triple containing name, type and function.

The function must be a callable which takes a subtable as it's input
and returns a value of the type specfied in the 2nd column.

    >>> from eztable import table_literal
    Warning: FastBinaryTree not available, using Python version BinaryTree.
    Warning: FastAVLTree not available, using Python version AVLTree.
    Warning: FastRBTree not available, using Python version RBTree.
    >>> t = table_literal("""
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
    ... """)
    >>>
    >>> agg = t.aggregate(
    ...     keys=('Pokemon', 'Attack Type'),
    ...     aggregations=[
    ...         ('Count', int, len)
    ...     ]
    ... )
    >>>
    >>> print(agg)
    | Pokemon (str) | Attack Type (str) | Count (int) |
    | Pikachu       | Electric          | 3           |
    | Pikachu       | Normal            | 4           |
    | Pikachu       | Fairy             | 2           |
    >>>
