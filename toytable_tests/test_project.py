import unittest
from toytable import Table


class TestProject(unittest.TestCase):

    def setUp(self):
        self.s = [
            ('A', int),
            ('B', float),
            ('C', str),
        ]
        self.t = Table(self.s)

        self.t.extend([
            [1, 1.1, 'hello'],
            [2, 2.2, 'yello'],
        ])

    def test_simple_project(self):
        t = self.t.project(['A', 'C'])
        self.assertEqual(t.schema, [('A', int), ('C', str)])
        self.assertEqual(t[0], (1, 'hello'))

    def test_anti_project(self):
        t = self.t.anti_project(['B'])
        self.assertEqual(t.schema, [('A', int), ('C', str)])
        self.assertEqual(t[0], (1, 'hello'))

    def test_anti_project_multiple_arguments(self):
        t = self.t.anti_project('A', 'B')
        self.assertEqual(t.schema, [('C', str)])
        self.assertEqual(t[0], ('hello',))

    def test_expand_const_on_project(self):
        t0 = self.t.project(['C'])
        t1 = t0.expand_const('D', 0)
        self.assertEqual(
            list(t1.D),
            [0] * len(self.t)
        )


if __name__ == '__main__':
    unittest.main()
