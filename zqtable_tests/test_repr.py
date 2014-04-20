import unittest
from zqtable import Table


class TestRepr(unittest.TestCase):

    def test_repr_headers(self):
        t = Table([('A', int), 'B', ('C', float)])
        self.assertEquals(
            repr(t),
            "| A (int) | B | C (float) |"
        )

    def test_repr(self):
        t = Table([('A', int), 'B', ('C', float)])
        t.extend([
            [1, "hello", 1.1],
            [2, "goodbye", 2.2],
        ])
        print repr(t)

if __name__ == '__main__':
    unittest.main()
