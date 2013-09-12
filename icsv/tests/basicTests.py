from unittest import TestCase

from icsv import icsv, Row


class BasicTests(TestCase):
    def setUp(self):
        pass

    def test_emptyConstructor(self):
        csv = icsv([])
        self.assertTrue(csv is not None)

        # Test default argument values
        self.assertEqual(csv.getHeaders(), "")
        self.assertEqual(csv.delimiter(), ",")
        self.assertEqual(csv.numRows(), 0)
        self.assertEqual(csv.numCols(), 0)

    def test_constructor(self):
        csv = icsv(["one", "two", "three"])
        self.assertTrue(csv is not None)

        # Test default argument values
        self.assertEqual(csv.getHeaders(), "one,two,three")
        self.assertEqual(csv.delimiter(), ",")
        self.assertEqual(csv.numRows(), 0)
        self.assertEqual(csv.numCols(), 3)

    def test_customDelimiter(self):
        csv = icsv(["three", "two", "one"], "/")
        self.assertTrue(csv is not None)

        # Test default argument values
        self.assertEqual(csv.getHeaders(), "three/two/one")
        self.assertEqual(csv.delimiter(), "/")
        self.assertEqual(csv.numRows(), 0)
        self.assertEqual(csv.numCols(), 3)

    def test_addInvalidRow(self):
        csv = icsv([])
        self.assertEqual(csv.numCols(), 0)

        # Adding an invalid rows
        self.assertRaises(Exception, csv.addRow, True)
        self.assertRaises(Exception, csv.addRow, 'a')
        self.assertRaises(Exception, csv.addRow, 1)

        # Adding valid row -- but no headers
        self.assertRaises(Exception, csv.addRow, [0, 0, 0])
        self.assertRaises(Exception, csv.addRow, {"a": 0})

    def test_addRowList(self):
        csv = icsv(["a", "b", "c"])

        # Adding incorrect amount of data
        self.assertRaises(Exception, csv.addRow, [])
        self.assertRaises(Exception, csv.addRow, [1, 2])
        self.assertRaises(Exception, csv.addRow, [1, 2, 3, 4])

        row1 = [1, 2, 3]
        row1Str = ','.join(map(str, row1))

        # Valid additions
        csv.addRow(row1)
        self.assertEqual(csv.numRows(), 1)
        self.assertEqual(str(csv.getRow()), row1Str)
        self.assertEqual(str(csv.getRow(0)), row1Str)
        self.assertEqual(str(csv.getRow(-1)), row1Str)
        self.assertEqual(csv.getRow().list(), row1)
        self.assertEqual(csv.getRow(0).list(), row1)
        self.assertEqual(csv.getRow(-1).list(), row1)

        row2 = [3, 2, 1]
        row2Str = ','.join(map(str, row2))

        csv.addRow(row2)
        self.assertEqual(csv.numRows(), 2)
        self.assertEqual(str(csv.getRow(0)), row1Str)
        self.assertEqual(str(csv.getRow(1)), row2Str)
        self.assertEqual(str(csv.getRow(-1)), row2Str)
        self.assertEqual(csv.getRow().list(), row2)
        self.assertEqual(csv.getRow(0).list(), row2)
        self.assertEqual(csv.getRow(-1).list(), row2)

    def test_addRowList(self):
        csv = icsv(["a", "b", "c"])

        # Adding incorrect amount of data
        self.assertRaises(Exception, csv.addRow, [])
        self.assertRaises(Exception, csv.addRow, [1, 2])
        self.assertRaises(Exception, csv.addRow, [1, 2, 3, 4])

        row1 = {"a": 1, "b": 2, "c": 3}
        row1List = [row1["a"], row1["b"], row1["c"]]
        row1Str = "1,2,3"

        # Valid additions
        csv.addRow(row1)
        self.assertEqual(csv.numRows(), 1)
        self.assertEqual(str(csv.getRow()), row1Str)
        self.assertEqual(str(csv.getRow(0)), row1Str)
        self.assertEqual(str(csv.getRow(-1)), row1Str)
        self.assertEqual(csv.getRow().list(), row1List)
        self.assertEqual(csv.getRow(0).list(), row1List)
        self.assertEqual(csv.getRow(-1).list(), row1List)

        row2 = {"a": 3, "b": 2, "c": 1}
        row2List = [row2["a"], row2["b"], row2["c"]]
        row2Str = "3,2,1"

        csv.addRow(row2)
        self.assertEqual(csv.numRows(), 2)
        self.assertEqual(str(csv.getRow(0)), row1Str)
        self.assertEqual(str(csv.getRow(1)), row2Str)
        self.assertEqual(str(csv.getRow(-1)), row2Str)
        self.assertEqual(csv.getRow(0).list(), row1List)
        self.assertEqual(csv.getRow().list(), row2List)
        self.assertEqual(csv.getRow(-1).list(), row2List)

    def test_removeInvalidRow(self):
        csv = icsv([])

        # No rows to remove
        self.assertRaises(Exception, csv.removeRow)
        self.assertRaises(Exception, csv.removeRow, 1)
        self.assertRaises(Exception, csv.removeRow, 0)

    def test_removeRow(self):
        csv = icsv(["a", "b", "c"])
        self.assertEqual(csv.numRows(), 0)

        row1 = [1, 2, 3]
        row2 = [3, 2, 1]

        csv.addRow(row1)
        self.assertEqual(csv.numRows(), 1)

        csv.addRow(row2)
        self.assertEqual(csv.numRows(), 2)
        self.assertEqual(str(csv.getRow()), "3,2,1")
        self.assertEqual(csv.getRow().list(), row2)

        csv.removeRow()
        self.assertEqual(csv.numRows(), 1)
        self.assertEqual(str(csv.getRow()), "1,2,3")
        self.assertEqual(csv.getRow().list(), row1)

        csv.removeRow()
        self.assertEqual(csv.numRows(), 0)

    def test_getRow(self):
        csv = icsv(["a", "b", "c"])
        csv.addRow([1, 2, 3])

        row = csv.getRow()
        self.assertEqual(str(row), "1,2,3")
        self.assertEqual(row.list(), [1, 2, 3])
        self.assertTrue(isinstance(row, Row))
