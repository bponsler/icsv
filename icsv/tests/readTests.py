from os import unlink
from os.path import exists

from unittest import TestCase

from icsv import icsv, Writer, Row


class ReadTests(TestCase):
    CsvFile = "/tmp/testCsv.csv"
    Headers = [
        "Header 1",
        "Header 2",
        "Header 3",
        ]

    def setUp(self):
        pass

    def test_basicRead(self):
        lines = []
        self.__writeFile(lines)

        csv = icsv.fromFile(self.CsvFile, self.Headers)
        self.assertTrue(csv is not None)
        self.assertEqual(csv.numRows(), 0)

    def test_simpleRead(self):
        lines = [
            "0,1,2",
            ]
        self.__writeFile(lines)

        csv = icsv.fromFile(self.CsvFile, self.Headers)
        self.assertTrue(csv is not None)
        self.assertEqual(csv.numRows(), 1)

        data = csv.data()
        self.assertEqual(len(data), 1)

        row0 = {
            "Header 1": '0',
            "Header 2": '1',
            "Header 3": '2',
            }
        data0 = data[0]
        self.assertEqual(data0.dict(), row0)
        self.assertEqual(data0["Header 1"], "0")
        self.assertEqual(data0["Header 2"], "1")
        self.assertEqual(data0["Header 3"], "2")

    def __writeFile(self, lines, includeHeaders=True, delimiter=','):
        fd = open(self.CsvFile, 'w')

        if includeHeaders:
            fd.write("%s\n" % delimiter.join(self.Headers))

        for line in lines:
            fd.write("%s\n" % line)
        fd.close()
