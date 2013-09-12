from copy import deepcopy
from os.path import exists

from icsv.instantCsv import icsv


class Writer:
    '''The Writer class provides an interface for writing a CSV file.

    This class can be used to write a pre-existing :class:`icsv.icsv` object
    to a file, or be used to write data to a filename in real time.

    The Writer class provides a wrapper to the :class:`icsv.icsv` class which
    will immediately write new rows to the CSV file.

    '''

    def __init__(self, filename, headers, delimiter=',',
                 useHeaders=True, overwrite=True):
        '''
        :param filename: The filename for the CSV file to write
        :type filename: string
        :param headers: The list of column headers for this CSV file
        :type headers: list of string
        :param delimiter: The CSV delimiter to use
        :type delimiter: string
        :param useHeaders: True will write the headers to the first line of the
                           created CSV file, False will not
        :type useHeaders: bool
        :param overwrite: True will overwrite existing files, False will not
        :type overwrite: bool

        :raises Exception: If ``overwrite`` is False, and the file already
                           exists

        '''
        self.__filename = filename
        self.__csv = icsv(headers, delimiter)
        self.__useHeaders = useHeaders
        self.__overwrite = overwrite

        if not self.__overwrite and exists(filename):
            raise Exception("Filename %s exists, and overwrite is disabled" %
                            filename)

        self.__firstWrite = True

    @classmethod
    def fromCsv(cls, filename, csv, useHeaders=True, overwrite=True):
        '''Write the data to the given CSV file.

        :param filename: The path to the CSV filename
        :type filename: string
        :param useHeaders: True to write the CSV headers as the first
                           line the file, False does not do this
        :type useHeaders: bool
        :param overwrite: True to overwrite existing files, False will
                          result in an Exception
        :type overwrite: bool

        :raises Exception: If ``overwrite`` is False, and the file already
                           exists

        '''
        writer = Writer(filename, csv.headers(), csv.delimiter(), useHeaders,
                        overwrite)
        writer.__csv = csv

        # Write the current CSV rows to the file
        for index in range(csv.numRows()):
            writer.__writeRow(index)

        return writer

    def headers(self):
        '''Get the list of headers for this CSV file.

        :rtype: list of strings

        '''
        return self.__csv.headers()

    def delimiter(self):
        '''Get the delimiter used for this CSV file.

        :rtype: string

        '''
        return self.__csv.delimiter()

    def getHeaders(self):
        '''Get the list of headers for this CSV file as a CSV string.

        :rtype: list of strings

        '''
        return self.__csv.getHeaders()

    def writeRow(self, items):
        '''Write a new row of data to the CSV.

        ``items`` can be a list of values, or a dictionary of values.

        * items -- The list, or dictionary of row items

        :raises Exception: If ``items`` is a list and is not equal to the
                           number of headers
        :raises Exception: If ``items`` is a dictionary and contains entries
                           for unknown headers
        :raises Exception: If ``items`` is not a list or a dictionary

        '''
        self.__csv.addRow(items)
        self.__writeRow()

    ##### Private functions

    def __writeRow(self, index=-1):
        '''Write the given row to the CSV file.

        :param index: The row index
        :type index: int

        '''
        # Write the headers if this is the first time
        if self.__firstWrite and self.__useHeaders:
            headers = self.__csv.getHeaders()
            self.__writeRowToFile(headers)

        # Write the most recent row to the file
        row = self.__csv.getRow(index)
        self.__writeRowToFile(row)

    def __writeRowToFile(self, row):
        '''Write the given :class:`icsv.Row` to the CSV file.

        :param row: The row
        :type row: A :class:`icsv.Row` object

        '''
        mode = 'w' if self.__firstWrite and self.__overwrite else 'a'        
        fd = open(self.__filename, mode)
        fd.write("%s\n" % str(row))
        fd.close()

        # The file has been writen to at least once
        self.__firstWrite = False

    def __str__(self):
        '''Convert the CSV data to a string.'''
        return str(self.__csv)
