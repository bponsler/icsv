from os import unlink
from os.path import exists

from unittest import TestCase

from icsv import icsv, Writer, Row


class WriteTests(TestCase):
    def setUp(self):
        pass

    def test_constructor(self):
        writer = Writer("/tmp/test.csv", [])
        self.assertTrue(writer is not None)
        self.assertEqual(writer.headers(), [])
        self.assertEqual(writer.delimiter(), ',')

        writer = Writer("/tmp/test.csv", [])
        self.assertTrue(writer is not None)
        self.assertEqual(writer.headers(), [])
        self.assertEqual(writer.delimiter(), ',')

        headers = ["one", "two"]
        writer = Writer("/tmp/test.csv", headers)
        self.assertTrue(writer is not None)
        self.assertEqual(writer.headers(), headers)
        self.assertEqual(writer.delimiter(), ',')

        headers = ["two"]
        writer = Writer("/tmp/test.csv", headers)
        self.assertTrue(writer is not None)
        self.assertEqual(writer.headers(), headers)
        self.assertEqual(writer.delimiter(), ',')

        headers = ["three"]
        delimiter = '-'
        writer = Writer("/tmp/test.csv", headers, delimiter)
        self.assertTrue(writer is not None)
        self.assertEqual(writer.headers(), headers)
        self.assertEqual(writer.delimiter(), delimiter)

        headers = ["four"]
        delimiter = ' '
        writer = Writer("/tmp/test.csv", headers, delimiter, True)
        self.assertTrue(writer is not None)
        self.assertEqual(writer.headers(), headers)
        self.assertEqual(writer.delimiter(), delimiter)

        # File exists, and overwrite is disabled
        headers = ["five", "6", "onetwo"]
        delimiter = '/'
        self.assertRaises(Exception, Writer, "/tmp/test.csv", headers,
                          delimiter, True, False)

    def test_testWriteHeaders(self):
        filename = "/tmp/test.csv"
        headers = ["five", "6", "onetwo"]

        # Delete the file for better testing
        self.__deleteFile(filename)

        writer = Writer(filename, headers)

        # Writing an unknown key should throw an error
        self.assertRaises(Exception, writer.writeRow,
                          {"DoesNotExist": "empty"})

        # File should not exist yet
        self.assertRaises(Exception, self.__readFile, filename)

        writer.writeRow([0, 1, 2])

        expectedLines = [
            writer.getHeaders(),
            "0,1,2",
            ]
        self.__verifyFileLines(filename, expectedLines)

        # Test writing a second row
        writer.writeRow({"onetwo": "hello"})

        expectedLines = [
            writer.getHeaders(),
            "0,1,2",
            ",,hello",
            ]
        self.__verifyFileLines(filename, expectedLines)

        # Test writing a second row -- order does not matter
        writer.writeRow({"onetwo": "two", "6": "1", "five": "abcd"})

        expectedLines = [
            writer.getHeaders(),
            "0,1,2",
            ",,hello",
            ",1,",
            "abcd,1,two",
            ]
        self.__verifyFileLines(filename, expectedLines)

        # Test writing a second row
        writer.writeRow({"6": "1"})

        expectedLines = [
            writer.getHeaders(),
            "0,1,2",
            ",,hello",
            ",1,",
            ]
        self.__verifyFileLines(filename, expectedLines)

    ##### Private helper functions

    def __verifyFileLines(self, filename, expectedLines):
        content = self.__readFile(filename)

        for index in range(len(content)):
            self.assertEqual(content[0], expectedLines[0])

    def __readFile(self, filename):
        if not exists(filename):
            raise Exception("File does not exist: %s" % filename)

        fd = open(filename, 'r')
        content = fd.read()
        fd.close()

        return content.strip().split('\n')

    def __deleteFile(self, filename):
        if exists(filename):
            unlink(filename)
