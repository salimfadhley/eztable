import unittest

from zqtable.table import Table, Schema, InvalidSchema, InvalidData

class TestExtendTable(unittest.TestCase):

    def setUp(self):
        self.s = Schema(
                ('A', int),
                ('B', float),
                ('C', str),
            )
        self.t = Table(self.s)

