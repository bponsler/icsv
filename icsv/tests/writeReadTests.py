from os import unlink
from os.path import exists

from unittest import TestCase

from icsv import icsv, Row


class WriteReadTests(TestCase):
    def setUp(self):
        pass

    def test_filter(self):
        filename = "/tmp/testCsv.csv"

        headers = ["one", "two", "three"]
        csv = icsv(headers)
        self.assertTrue(csv is not None)
        self.assertEqual(csv.headers(), headers)
        self.assertEqual(csv.delimiter(), ',')

        rows = [
            [0, 1, 2],
            [3, 4, 5],
            ["hello", 1, True],
            [1, False, "world"],
            ]

        # Write all of the data to the file
        for row in rows:
            csv.addRow(row)
        self.assertEqual(csv.numRows(), 4)

        # Save the file
        writer = csv.write(filename)
        self.assertTrue(writer is not None)

        # Read the same CSV
        reader = csv.fromFile(filename, headers)
        self.assertTrue(reader is not None)

        # Compare the read data to the original
        self.assertEqual(reader.numRows(), csv.numRows())
        self.assertEqual(reader.numCols(), csv.numCols())
        self.assertEqual(reader.headers(), csv.headers())

        for index in range(len(rows)):
            read = reader.getRow(index)

            # Read data will be all strings
            original = list(map(str, csv.getRow(index).list()))
            expected = list(map(str, rows[index]))

        for index in range(len(original)):
            self.assertEqual(original[index], expected[index])
        self.assertEqual(read.list(), expected)
