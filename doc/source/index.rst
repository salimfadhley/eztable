
Welcome to toytable's documentation!
====================================

Toytable is a toy table package. It is suitable for lightweight data analysis tasks. It provides a class
which is suitable for representing one-dimensional tables (e.g. time-sequences).

Toytable is built with an emphasis on simplicity, both in interface and internal design
rather than performance or scalability. Toytable is intended to have as few dependancies
as possible, and is therefore suitable for casual development tasks.

Toytable is not intended for high performance or scalability. Toytable is not complete. For these reasons,
please consider evaluating other more mature packages (e.g. Pandas).

About this project
------------------

* Documentation: https://pythonhosted.org/toytable/
* Released version: https://pypi.python.org/pypi/toytable/
* Source code: https://bitbucket.org/salimfadhley/toytable
* Problems, Suggestions & Bugs: sal@stodge.org

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

It's easy to make a Table::
    >>> from toytable import Table
    >>> p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
    >>> p.extend([
    ...     [1, 'Pikachu', 18],
    ... ])

Table objects can be printed::
    >>> print p
    | Owner Id (int) | Pokemon | Level (int) |
    | 1              | Pikachu | 18          |

You can add data to tables one row at a time. It has the same effect as using the extend function::
    >>> o = Table([('Owner Id', int), ('Name', str)])
    >>> o.append([1, 'Ash Ketchum'])
    >>> o.append([2, 'Brock'])
    >>> o.append([3, 'Misty'])
    >>> print o
    | Owner Id (int) | Name (str)  |
    | 1              | Ash Ketchum |
    | 2              | Brock       |
    | 3              | Misty       |

Tables can be joined to other tables::
    >>> j = p.left_join(
    ...     keys=('Owner Id',),
    ...     other = o
    ... )
    >>> print j
    | Owner Id (int) | Pokemon | Level (int) | Name (str)  |
    | 1              | Pikachu | 18          | Ash Ketchum |

The project method allows you to re-order and remove columns::
    >>> j2 = j.project('Pokemon', 'Level', 'Name')
    >>> print j2
    | Pokemon | Level (int) | Name (str)  |
    | Pikachu | 18          | Ash Ketchum |

The Table Class
---------------

.. automethod:: toytable.Table.__init__

.. automodule:: toytable
    :members: Table, DerivedTable
    :undoc-members:
    :show-inheritance:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

