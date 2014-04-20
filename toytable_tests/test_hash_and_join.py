import unittest
from toytable import Table


class TestHashAndJoin(unittest.TestCase):

    def setUp(self):
        self.s = [
            ('A', int),
            ('B', float),
            ('C', str),
            ('D', tuple),
        ]

        self.t = Table(self.s)
        self.t.extend([
            [1, 1.1, 'a', (1, 2)],
            [2, 1.2, 'b', (2, 3)],
            [3, 1.3, 'c', (3, 4)],
        ])

    # def test_simple_hash(self):
    #     t = self.t.hash('H', ['C'])

    #     self.assertEquals(
    #         t.H.to_list(),
    #         [hash(('a')), hash(('b')), hash(('c'))]

    #     )
