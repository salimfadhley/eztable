"""An index is an ordered list-like object implemented using a btree.blist.
"""

import blist
import itertools
from .exceptions import InvalidIndex


class Index(blist.blist):

    def __init__(self, table, cols):
        if not cols:
            raise InvalidIndex('Please provide at least one column to index.')

        try:
            self.cols = [getattr(table, c) for c in cols]
        except AttributeError as ae:

            raise InvalidIndex(
                'Column %s does not exist. Valid columns are %s' % (
                    ae[0],
                    ', '.join(table.column_names)
                ))

        table._listeners.add(self)
        self.table = table

    def __hash__(self):
        return hash(c.name for c in self.cols)

    def notify(self, op, pos):
        if op == 'append':
            value = tuple(c[pos] for c in self.cols) + (pos,)
            self.append(value)

    def __getitem__(self, key):
        """If key is an integer this function returns that
        element from the index.

        If key is a tuple it finds the index of that item
        in the index and then returns the corresponding row
        from the table.
        """
        if isinstance(key, int):
            return blist.blist.__getitem__(self, key)
        elif isinstance(key, tuple):
            return self.table[self.index(key)]
        raise TypeError(
            'Index keys must be an integer or a tuple, got %r (%s)' %
            (key, type(key))
        )

    def reindex(self):
        del self[:]
        self.extend(itertools.izip(*self.cols))
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
        def fn_iter():
            for i, v in enumerate(self):
                if v == value:
                    yield i
        return fn_iter
