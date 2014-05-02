Array Columns
=============

Ordinarily the columns in toytable.Table objects are lists, however the class also supports columns which are arrays.

These behave virtually identically to the normal kind of column, but ofer greater memory efficiency. They may be used alongside other kinds of column. 

An array column can be specified by using the single-char type code instead of a type name. The full list of type-codes are given Python's `array documentation`_.

.. _array documentation: https://docs.python.org/3.3/library/array.html?highlight=array#module-array

    >>> from toytable import table_literal, Table
    Warning: FastBinaryTree not available, using Python version BinaryTree.
    Warning: FastAVLTree not available, using Python version AVLTree.
    Warning: FastRBTree not available, using Python version RBTree.
    >>> 
    >>> types = Table([('Type Id', 'i'), ('Type', str)])
    >>> types.append([1, 'water'])
    >>> types.append([2, 'bug'])
    >>> 
    >>> t = table_literal("""
    ... | Pokedex Number (i) | Pokemon (str) | Type Id (i) |
    ... | 7                  | Squirtle      | 1           |
    ... | 8                  | Wartortle     | 1           |
    ... | 9                  | Blastoise     | 1           |
    ... | 10                 | Caterpie      | 2           |
    ... | 11                 | Metapod       | 2           |
    ... | 12                 | Butterfree    | 2           |
    ... """)
    >>> 
    >>> pokedex = t.left_join(
    ...     keys=('Type Id', ),
    ...     other=types
    ... )
    >>> print pokedex
    | Pokedex Number (i) | Pokemon (str) | Type Id (i) | Type (str) |
    | 7                  | Squirtle      | 1           | water      |
    | 8                  | Wartortle     | 1           | water      |
    | 9                  | Blastoise     | 1           | water      |
    | 10                 | Caterpie      | 2           | bug        |
    | 11                 | Metapod       | 2           | bug        |
    | 12                 | Butterfree    | 2           | bug        |
