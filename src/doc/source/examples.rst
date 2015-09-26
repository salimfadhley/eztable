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
    >>> print p
    | Owner Id (int) | Pokemon    | Level (int) |
    | 1              | Pikachu    | 18          |
    | 1              | Bulbasaur  | 22          |
    | 1              | Charmander | 12          |
    | 3              | Togepi     | 5           |
    | 1              | Starmie    | 44          |
    | 9              | Mew        | 99          |

Appending to tables
-------------------

You can add data to Tables one row at a time. It has the same effect as using the Table.extend(iter) function:
    >>> o = Table([('Owner Id', int), ('Name', str)])
    >>> o.append([1, 'Ash Ketchum'])
    >>> o.append([2, 'Brock'])
    >>> o.append([3, 'Misty'])
    >>> print o
    | Owner Id (int) | Name (str)  |
    | 1              | Ash Ketchum |
    | 2              | Brock       |
    | 3              | Misty       |


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
    >>> print j2
    | Pokemon    | Level (int) | Name (str)  |
    | Pikachu    | 18          | Ash Ketchum |
    | Bulbasaur  | 22          | Ash Ketchum |
    | Charmander | 12          | Ash Ketchum |
    | Togepi     | 5           | Misty       |
    | Starmie    | 44          | Ash Ketchum |
    | Mew        | 99          | None        |

Filtering rows of a table
-------------------------

The restrict method allows basic filtering of a Table:
    >>> restricted = j2.restrict(['Name'], lambda n: n == 'Ash Ketchum')
    >>> print restricted
    | Pokemon    | Level (int) | Name (str)  |
    | Pikachu    | 18          | Ash Ketchum |
    | Bulbasaur  | 22          | Ash Ketchum |
    | Charmander | 12          | Ash Ketchum |
    | Starmie    | 44          | Ash Ketchum |

Slicing Operations
------------------

Tables can also be sliced - and do exactly what you'd expect:
    >>> sliced = j2[1:-1]
    >>> print sliced
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

Flattened Tables (but currently not DerivedTables) can be indexed. Indexes
can be used to quickly look up rows by part of their value. Indexes
eliminate the need for time-consuming search operations::

    >>> i = j3.add_index(('Pokemon',)).reindex()
    >>> print i[('Pikachu', )]
    ('Pikachu', 18, 'Ash Ketchum')