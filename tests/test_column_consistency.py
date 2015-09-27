import unittest
from eztable.columns import Column, StaticColumn, DerivedColumn, DerivedTableColumn, NormalizedColumn, \
    StandardizedColumn, ArrayColumn


class BaseTest():

    def test_that_we_can_repr(self):
        repr(self.col)

    def test_that_we_can_unpack(self):
        self.assertEqual(len(list(self.col)), 3)

    def test_that_we_can_get_a_type(self):
        expected_type = getattr(self, "expected_type", str)
        self.assertEqual(self.col.column_type, expected_type)

    def test_that_we_can_get_a_name(self):
        self.assertEqual(self.col.name, self.expected_name)

    def test_that_we_can_get_a_description(self):
        desc = self.col.description
        self.assertIsInstance(desc, str)


class TestColumn(BaseTest, unittest.TestCase):
    expected_name = "StrCol"

    def setUp(self):
        self.col = Column(self.expected_name, ["A", "B", "C"], column_type=str)


class TestStaticColumn(BaseTest, unittest.TestCase):
    expected_name = "StaticCol"

    def setUp(self):
        self.col = StaticColumn(self.expected_name, "X", lambda: 3, column_type=str)


class TestDerivedColumn(BaseTest, unittest.TestCase):
    expected_name = "DerivedCol"

    def setUp(self):
        input_col = Column("xxx", ["A", "B", "C"], column_type=str)
        self.col = DerivedColumn(name=self.expected_name, inputs=[input_col], column_type=str,
                                 func=lambda *c: "X" + "".join(c))


class TestDerivedTableColumn(BaseTest, unittest.TestCase):
    expected_name = "DerivedTableCol"

    def setUp(self):
        input_col = Column(self.expected_name, ["A", "B", "C"], column_type=str)
        self.col = DerivedTableColumn(column=input_col, indices_func=lambda: range(3))


class TestNormalizeColumn(BaseTest, unittest.TestCase):
    expected_type = float
    expected_name = "NormalCol"

    def setUp(self):
        input_col = Column(self.expected_name, [0, 0.5, 1], column_type=float)
        self.col = NormalizedColumn(column=input_col, normal=1.0)

class TestStandardizedColumn(BaseTest, unittest.TestCase):
    expected_type = float
    expected_name = "StandardCol"

    def setUp(self):
        input_col = Column(self.expected_name, [-1, 0, 1], column_type=float)
        self.col = StandardizedColumn(column=input_col, deviation=1.0)


class TestArrayColumn(BaseTest, unittest.TestCase):
    expected_type = "i"
    expected_name = "ArrayIntCol"

    def setUp(self):
        self.col = ArrayColumn(self.expected_name, values=[1,2,3], column_type="i")

if __name__ == '__main__':
    unittest.main()
