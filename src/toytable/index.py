"""An index is an ordered list-like object implemented using a btree.blist.
"""

import bintrees
import six.moves
from .exceptions import InvalidIndex


class Index(bintrees.RBTree):

    def __init__(self, table, cols):
        bintrees.RBTree.__init__(self)
        if not cols:
            raise InvalidIndex('Please provide at least one column to index.')

        try:
            self.cols = [table._get_column(c) for c in cols]
        except KeyError as ke:
            raise InvalidIndex(
                'Column %s does not exist. Valid columns are %s' % (
                    ke.args[0],
                    ', '.join(table.column_names)
                ))
        self.table = table

    def __hash__(self):
        return hash(c.name for c in self.cols)

    def notify(self, op, pos):
        if op == 'append':
            value = tuple(c[pos] for c in self.cols) + (pos,)
            self.setdefault(value, []).append(pos)

    def __getitem__(self, key):
        """If key is an integer this function returns that
        element from the index.

        If key is a tuple it finds the index of that item
        in the index and then returns the corresponding row
        from the table.
        """
        if isinstance(key, int):
            return bintrees.RBTree.__getitem__(self, key)
        elif isinstance(key, tuple):
            return (
                [self.table[i] for i in self.index(key)]
            )
        raise TypeError(
            'Index keys must be an integer or a tuple, got %r (%s)' % 
            (key, type(key))
        )

    def index(self, key):
        return bintrees.RBTree.__getitem__(self, key)

    def reindex(self):
        del self[:]
        for i, row in enumerate(six.moves.zip(*self.cols)):
            self.setdefault(row, []).append(i)
        return self

    def __str__(self):
        return ','.join(c.name for c in self.cols)

    def __repr__(self):
        return (
            '<%s.%s %s>' % (
                self.__class__.__module__,
                self.__class__.__name__,
                str(self))
        )

    def unique_values(self):
        return set(self)

    def _get_iterator_fn_for_value(self, value):
        """Get an iterator that gives the indeces of any value in the index
        """
        return bintrees.RBTree.__getitem__(self, value).__iter__
