Examples    
========

Building a table
----------------

Making a table is trivial:
    >>> from eztable import Table
    >>> p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
    >>> p.extend([
    ...     [1, 'Pikachu', 18],
    ...     [1, 'Bulbasaur', 22],
    ...     [1, 'Charmander', 12],
    ...     [3, 'Togepi', 5],
    ...     [1, 'Starmie', 44],
    ...     [9, 'Mew', 99],
    ... ])


Printing tables
---------------

Table objects can be printed:
    >>> print(p)
    | Owner Id (int) | Pokemon    | Level (int) |
    | 1              | Pikachu    | 18          |
    | 1              | Bulbasaur  | 22          |
    | 1              | Charmander | 12          |
    | 3              | Togepi     | 5           |
    | 1              | Starmie    | 44          |
    | 9              | Mew        | 99          |

The "repr-string" you get when you print a table can be used to define the table. In other words, anything you can print
you can load into an eztable.Table. This behavior helps you define tables very quickly. It's useful in testing and agile
development.

    >>> from eztable import table_literal
    Warning: FastBinaryTree not available, using Python version BinaryTree.
    Warning: FastAVLTree not available, using Python version AVLTree.
    Warning: FastRBTree not available, using Python version RBTree.
    >>> pokedex = table_literal("""
    ...     | Owner Id (int) | Pokemon    | Level (int) |
    ...     | 1              | Pikachu    | 18          |
    ...     | 1              | Bulbasaur  | 22          |
    ...     | 1              | Charmander | 12          |
    ...     | 3              | Togepi     | 5           |
    ...     | 1              | Starmie    | 44          |
    ...     | 9              | Mew        | 99          |
    ...     """)
    >>> print(pokedex)
    | Owner Id (int) | Pokemon (str) | Level (int) |
    | 1              | Pikachu       | 18          |
    | 1              | Bulbasaur     | 22          |
    | 1              | Charmander    | 12          |
    | 3              | Togepi        | 5           |
    | 1              | Starmie       | 44          |
    | 9              | Mew           | 99          |


Adding rows  to tables
----------------------

You can add data to Tables one row at a time:

    >>> o = Table([('Owner Id', int), ('Name', str)])
    >>> o.append([1, 'Ash Ketchum'])
    >>> o.append([2, 'Brock'])
    >>> o.append([3, 'Misty'])
    >>> print(o)
    | Owner Id (int) | Name (str)  |
    | 1              | Ash Ketchum |
    | 2              | Brock       |
    | 3              | Misty       |

You can aso add many rows to a table in a single operation using the 'extend' function:

    >>> o = Table([('Owner Id', int), ('Name', str)])
    >>> o.extend([[1, 'Ash Ketchum'],
    ...           [2, 'Brock'],
    ...           [3, 'Misty']])
    >>> print(o)
    | Owner Id (int) | Name (str)  |
    | 1              | Ash Ketchum |
    | 2              | Brock       |
    | 3              | Misty       |

Append and extend have behaviors that are intentionally constent with Python's lists.

Joins on tables
---------------

Tables can be joined to other Tables:
    >>> j = p.left_join(
    ...     keys=('Owner Id',),
    ...     other = o
    ... )
    >>> print j
    | Owner Id (int) | Pokemon    | Level (int) | Name (str)  |
    | 1              | Pikachu    | 18          | Ash Ketchum |
    | 1              | Bulbasaur  | 22          | Ash Ketchum |
    | 1              | Charmander | 12          | Ash Ketchum |
    | 3              | Togepi     | 5           | Misty       |
    | 1              | Starmie    | 44          | Ash Ketchum |
    | 9              | Mew        | 99          | None        |


Re-ordering columns
-------------------

The project method allows you to re-order and remove columns from a Table:
    >>> j2 = j.project('Pokemon', 'Level', 'Name')
    >>> print(j2)
    | Pokemon    | Level (int) | Name (str)  |
    | Pikachu    | 18          | Ash Ketchum |
    | Bulbasaur  | 22          | Ash Ketchum |
    | Charmander | 12          | Ash Ketchum |
    | Togepi     | 5           | Misty       |
    | Starmie    | 44          | Ash Ketchum |
    | Mew        | 99          | None        |

You can use the project method to throw away columns you no longer need. Simply omit the columns you no longer require.

Discarding columns
------------------

There's an even easier way to throw-away columns you don't need anymore. You can use anti_project to tell the Table to
forget about a column. The order of arguments in the anti_project function does not matter - you just give it a list of
arguments you want it to not include in the table:

    >>> from eztable import table_literal
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
    >>> t = t.anti_project(["Attack", "Level Obtained"])
    >>> print(t)
    | Pokemon (str) | Attack Type (str) |
    | Pikachu       | Electric          |
    | Pikachu       | Normal            |
    | Pikachu       | Normal            |
    | Pikachu       | Normal            |
    | Pikachu       | Normal            |
    | Pikachu       | Electric          |
    | Pikachu       | Electric          |
    | Pikachu       | Fairy             |
    | Pikachu       | Fairy             |

Filtering rows of a table
-------------------------

The restrict method allows basic filtering of a Table:
    >>> restricted = j2.restrict(['Name'], lambda n: n == 'Ash Ketchum')
    >>> print(restricted)
    | Pokemon    | Level (int) | Name (str)  |
    | Pikachu    | 18          | Ash Ketchum |
    | Bulbasaur  | 22          | Ash Ketchum |
    | Charmander | 12          | Ash Ketchum |
    | Starmie    | 44          | Ash Ketchum |

Slicing Operations
------------------

Tables can also be sliced - and do exactly what you'd expect:
    >>> sliced = j2[1:-1]
    >>> print(sliced)
    | Pokemon    | Level (int) | Name (str)  |
    | Bulbasaur  | 22          | Ash Ketchum |
    | Charmander | 12          | Ash Ketchum |
    | Togepi     | 5           | Misty       |
    | Starmie    | 44          | Ash Ketchum |

Copying tables
--------------

Tables can be copied - that flattens their internal structure and can result
in improved performance::

    >>> j3 = j2.copy()

Indexing tables
---------------

Flattened Tables (but currently not DerivedTables) can be indexed. Indexes
can be used to quickly look up rows by part of their value. Indexes
eliminate the need for time-consuming search operations::

    >>> i = j3.add_index(('Pokemon',)).reindex()
    >>> print(i[('Pikachu', )])
    ('Pikachu', 18, 'Ash Ketchum')