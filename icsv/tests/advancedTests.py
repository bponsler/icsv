from os import unlink
from os.path import exists

from unittest import TestCase

from icsv import icsv, Row


class AdvancedTests(TestCase):
    def setUp(self):
        pass

    def test_filter(self):
        headers = ["one", "two", "three"]
        csv = icsv(headers)
        self.assertTrue(csv is not None)
        self.assertEqual(csv.headers(), headers)
        self.assertEqual(csv.delimiter(), ',')

        # Write some data to the file
        csv.addRow([0, 0, 0])
        csv.addRow([1, 0, 0])
        csv.addRow([1, 1, 0])
        csv.addRow([1, 1, 1])
        self.assertEqual(csv.numRows(), 4)

        cells = csv.filter(lambda r, h, v: v == 2)
        self.assertEqual(len(cells), 0)

        cells = csv.filter(lambda r, h, v: v == 1)
        self.assertEqual(len(cells), 6)
        self.assertEqual(cells[0].row(), 1)
        self.assertEqual(cells[0].header(), "one")

        items = [
            (1, "one"),
            (2, "one"),
            (2, "two"),
            (3, "one"),
            (3, "two"),
            (3, "three"),
            ]

        for index in range(len(cells)):
            row, header = items[index]
            self.assertEqual(cells[index].row(), row)
            self.assertEqual(cells[index].header(), header)

            # All returned cells should have a value of 1
            self.assertEqual(cells[index].value(), 1)
