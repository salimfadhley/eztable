toytable: Lightweight python tables 
===================================

.. image:: toy_table.png

Toytable is a lightweight python table library. It provides a class called Table  which is suitable for representing one-dimensional tables (e.g. time-sequences).

Toytable is built with an emphasis on simplicity, both in interface and internal design
rather than performance or scalability. Toytable is intended to have as few dependancies
as possible, and is therefore suitable for casual development tasks.

Toytable is not complete. If you require a higher performance, more feature-rich table class, please
consider `Pandas`_, a very mature project which was a significant inspiration for this project. 

.. _Pandas: http://pandas.pydata.org/

About this project
------------------

* Documentation: http://toytable.readthedocs.org/
* Released version: https://pypi.python.org/pypi/toytable/
* Source code: https://bitbucket.org/salimfadhley/toytable
* Problems, Suggestions & Bugs: https://bitbucket.org/salimfadhley/toytable/issues

Installation
------------

Egg-files for this project are hosted on PyPi. Most Python users should be able to use pip or setuptools to automatically install this project.

Most users can do the following:
::
    pip install toytable

Or..
::
    easy_install toytable

You can also install this project from source. Check ou the code from mercurial
and then build the project.

Examples    
--------

Making a table is very easy::
    >>> from toytable import Table
    >>> p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
    >>> p.extend([
    ...     [1, 'Pikachu', 18],
    ...     [1, 'Bulbasaur', 22],
    ...     [1, 'Charmander', 12],
    ...     [3, 'Togepi', 5],
    ...     [1, 'Starmie', 44],
    ...     [9, 'Mew', 99],
    ... ])


Table objects can be printed::
    >>> print p
    | Owner Id (int) | Pokemon    | Level (int) |
    | 1              | Pikachu    | 18          |
    | 1              | Bulbasaur  | 22          |
    | 1              | Charmander | 12          |
    | 3              | Togepi     | 5           |
    | 1              | Starmie    | 44          |
    | 9              | Mew        | 99          |

You can add data to Tables one row at a time. It has the same effect as using the Table.extend(iter) function::
    >>> o = Table([('Owner Id', int), ('Name', str)])
    >>> o.append([1, 'Ash Ketchum'])
    >>> o.append([2, 'Brock'])
    >>> o.append([3, 'Misty'])
    >>> print o
    | Owner Id (int) | Name (str)  |
    | 1              | Ash Ketchum |
    | 2              | Brock       |
    | 3              | Misty       |


Tables can be joined to other Tables::
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


The project method allows you to re-order and remove columns from a Table::
    >>> j2 = j.project('Pokemon', 'Level', 'Name')
    >>> print j2
    | Pokemon    | Level (int) | Name (str)  |
    | Pikachu    | 18          | Ash Ketchum |
    | Bulbasaur  | 22          | Ash Ketchum |
    | Charmander | 12          | Ash Ketchum |
    | Togepi     | 5           | Misty       |
    | Starmie    | 44          | Ash Ketchum |
    | Mew        | 99          | None        |

The restrict method allows basic filtering of a Table::
    >>> restricted = j2.restrict(['Name'], lambda n: n == 'Ash Ketchum')
    >>> print restricted
    | Pokemon    | Level (int) | Name (str)  |
    | Pikachu    | 18          | Ash Ketchum |
    | Bulbasaur  | 22          | Ash Ketchum |
    | Charmander | 12          | Ash Ketchum |
    | Starmie    | 44          | Ash Ketchum |

Tables can also be sliced - and do exactly what you'd expect:
    >>> sliced = j2[1:-1]
    >>> print sliced
    | Pokemon    | Level (int) | Name (str)  |
    | Bulbasaur  | 22          | Ash Ketchum |
    | Charmander | 12          | Ash Ketchum |
    | Togepi     | 5           | Misty       |
    | Starmie    | 44          | Ash Ketchum |

Tables can be copied - that flattens their internal structure and can result
in improved performance::

    >>> j3 = j2.copy()

Flattened Tables (but currently not DerivedTables) can be indexed. Indexes
can be used to quickly look up rows by part of their value. Indexes
eliminate the need for time-consuming search operations::

    >>> i = j3.add_index(('Pokemon',)).reindex()
    >>> print i[('Pikachu', )]
    ('Pikachu', 18, 'Ash Ketchum')


The Table Class
---------------

The Table class (toytable.Table) is the most important component of this package.
It is intended to represent a 'normal' table - that is one which has no 
special colums or has not undergone any transformations (e.g. project, expand).

.. automethod:: toytable.Table.__init__

.. automodule:: toytable
    :members: Table, DerivedTable
    :undoc-members:
    :show-inheritance:

Table Literals
--------------

.. autofunction:: toytable.table_literal

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

