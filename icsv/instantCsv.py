from copy import deepcopy
from os.path import exists

from icsv.base import Row, Col, Cell


class icsv:
    '''The icsv class encapsulates the data contained in a single CSV
    file.

    A CSV consists of zero or more rows of information where each row
    has one or more named columns. The names of the columns are referred to
    as headers.

    The icsv class provides an interface for easily adding new data to a
    CSV, writing the data to a CSV file, and creating an icsv from a file.

    '''
    def __init__(self, headers, delimiter=','):
        '''
        :param headers: The list of column headers
        :type headers: list of strings
        :param delimiter: The CSV delimiter
        :type delimiter: string

        '''
        self.__headers = headers
        self.__delimiter = delimiter

        # List of dictionaries mapping headers to values for each
        # row in the CSV
        self.__data = []

    @classmethod
    def fromFile(cls, filename, headers=None, delimiter=',',
                 containsHeaders=True):
        '''Create an icsv from a given CSV file.

        :param filename: The path to the CSV file
        :type filename: string
        :param headers: The list of CSV headers. If this is None they will be
                        automatically read from the file
        :type headers: list of strings
        :param delimiter: The CSV delimiter
        :type delimiter: string
        :param containsHeaders: True if the file list the headers as the first
                                line, False if it does not
        :type containsHeaders: bool

        :raises Exception: If the file does not exist
        :raises Exception: If ``headers`` is None and ``containsHeaders``
                           is False

        '''
        # CSV file must actually exist
        if not exists(filename):
            raise Exception("File does not exist: %s" % filename)

        # Must be able to determine the headers
        if headers is None and not containsHeaders:
            raise Exception("Could not determine headers. If 'headers' is " \
                                "None, then 'containsHeaders' must be True")

        fd = open(filename, 'r')
        content = fd.read()
        fd.close()

        # Split the content into separate rows
        rows = content.strip().split('\n')

        # Split each row into separate columns
        splitRows = [row.strip().split(delimiter) for row in rows]

        data = []

        # Grab the headers from the first line in the file
        if headers is None:
            headers = splitRows[0].split(delimiter)

        # Create row dictionaries for all the other data
        startIndex = 1 if containsHeaders else 0
        for splitRow in splitRows[startIndex:]:
            dataMap = dict(zip(headers, splitRow))
            data.append(dataMap)

        # Create the CSV file
        csv = icsv(headers, delimiter)
        csv.__data = data

        return csv

    def write(self, filename, useHeaders=True, overwrite=True):
        '''Write the data to the given CSV file.

        This is the same as calling::

            import icsv
            aCsv = icsv.icsv()
            writer = icsv.Writer.fromCsv(filename, aCsv, useHeaders, overwrite)

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
        # Import writer here, to avoid cyclical dependencies
        from icsv.writer import Writer
        return Writer.fromCsv(filename, self, useHeaders, overwrite)

    def numRows(self):
        '''Get the number of rows in the CSV.

        :rtype: int

        '''
        return len(self.__data)

    def numCols(self):
        '''Get the number of columns in the CSV.

        :rtype: int

        '''
        return len(self.__headers)

    def delimiter(self):
        '''Get the delimiter value for this CSV.

        :rtype: string

        '''
        return self.__delimiter

    def headers(self):
        '''Get the list of column headers for this CSV.

        :rtype: list of strings

        '''
        return self.__headers

    def data(self):
        '''Get the list of :class:`icsv.Row` objects pertaining to the rows
        of this CSV.

        :rtype: list of :class:`icsv.Row` objects

        '''
        # Convert all rows into actual Row objects
        return [Row(self.__headers, r, self.__delimiter) for r in self.__data]

    def setCell(self, header, value, row=-1):
        '''Set the value of a cell.

        :param header: The header for the cell
        :type header: string
        :param value: The cell value
        :param row: The row index (last row by default)
        :type row: int

        :raises Exception: If an invalid row index is given
        :raises Exception: If an invalid header is given

        '''
        self.__validateRow(row)
        self.__validateHeader(header)

        row = self.__data[row]
        row[header] = value

    def addRow(self, items):
        '''Add a row of data to the CSV.

        ``items`` can be a list of values, or a dictionary of values.

        * items -- The list, or dictionary of row items

        :raises Exception: If ``items`` is a list and is not equal to the
                           number of headers
        :raises Exception: If ``items`` is a dictionary and contains entries
                           for unknown headers
        :raises Exception: If ``items`` is not a list or a dictionary

        '''
        if type(items) == type(list()):
            self.__addRowList(items)
        elif type(items) == type(dict()):
            self.__addRowMap(items)
        else:
            raise Exception("Unknown row type. Expected list or dictionary.")

    def removeRow(self, row=-1):
        '''Remove the given row.

        :param row: The index of the row to remove (last row by default)
        :type row: int

        :raises Exception: If row is not a valid index

        '''
        self.__validateRow(row)
        del self.__data[row]

    def getRow(self, row=-1):
        '''Get the given row.

        :param row: The row index (last row be default)
        :type row: int

        :raises Exception: If row is not a valid index

        '''
        self.__validateRow(row)
        return Row(self.__headers, self.__data[row], self.__delimiter)

    def getCol(self, header):
        '''Get the :class:`icsv.Col` object for the given column header.

        :param header: The column header
        :type header: string

        :rtype: A :class:`icsv.Col` object

        :raises Exception: If an unknown header is given

        '''
        self.__validateHeader(header)
        data = [row.get(header, '') for row in self.__data]
        return Col(header, data)

    def getCell(self, row, header):
        '''Get the :class:`icsv.Cell` object contained at the given
        row index and column header.

        :param row: The row index
        :type row: int
        :param header: The column header
        :type header: string

        :rtype: A :class:`icsv.Cell` object

        :raises Exception: If an invalid row index is given
        :raises Exception: If an unknown header is given

        '''
        self.__validateRow(row)
        self.__validateHeader(header)

        value = self.__data[row].get(header, '')
        return Cell(row, header, value)

    def getHeaderIndex(self, header):
        '''Get the column index for the given column header.

        :param header: The column header
        :type header: string

        :rtype: int

        :raises Exception: If an unknown header is given

        '''
        self.__validateHeader(header)
        return self.__headers.index(header)

    def getHeader(self, index):
        '''Get the column header for the given column index.

        :param index: The column index
        :type index: int

        :rtype: string

        :raises Exception: If an invalid column index is given

        '''
        if index not in range(len(self.__headers)):
            raise Exception("Header index out of range: %s" % index)

        return self.__headers[index]

    def getHeaders(self):
        '''Get the list of headers for this CSV file as a CSV string.

        :rtype: list of strings

        '''
        return self.__delimiter.join(self.__headers)

    # TODO: ability to add new columns
    # TODO: ability to remove columns

    # TODO: ability to re-arrange rows
    # TODO: ability to re-arrange columns

    # TODO: ability to search for data

    def filter(self, fn):
        '''Apply a filter function to the CSV data.

        The filter function must have the following signature::

            filterFn(rowIndex, columnHeader, cellValue)

        :param fn: The filter function
        :type fn: function(rowIndex, colHeader, cellValue)

        :returns: A list of Cells for which ``fn`` returned True
        :rtype: List of :class:`icsv.Cell` objects

        '''
        allCells = []

        for rowIdx in range(len(self.__data)):
            row = self.__data[rowIdx]

            for header in self.__headers:
                cellValue = row.get(header, '')

                if fn(rowIdx, header, cellValue):
                    cell = Cell(rowIdx, header, cellValue)
                    allCells.append(cell)

        return allCells

    def map(self, fn, overwrite=False):
        '''Map all of the values of the CSV.

        The map function must have the following signature::

            mapFn(rowIndex, columnHeader, cellValue)

        :param fn: The map function
        :type fn: function(rowIndex, columnHeader, cellValue)
        :param overwrite: True to replace the current icsv data with
                          the mapped data
        :type overwrite: bool

        :returns: An :class:`icsv.icsv` object containing the mapped data
        :rtype: An :class:`icsv.icsv` object

        '''
        if overwrite:
            csv = self  # Update this CSV data
        else:
            # Create a copy of the current CSV file
            csv = icsv(self.__headers, self.__delimiter)
            csv.__data = deepcopy(self.__data)

        for rowIdx in range(len(self.__data)):
            row = self.__data[rowIdx]

            for header in self.__headers:
                cell = row.get(header, '')
                newValue = fn(rowIdx, header, cell)

                # Store the new value
                csv.__data[rowIdx][header] = newValue

        return csv

    # TODO: ability to merge two icsvs into one -- not sure how this works

    ##### Private headers

    def __addRowList(self, items):
        '''Add a new row consisting of a list of values.

        :param items: The list of values
        :type items: list of values

        :raises Exception: If the number of items given does not match the
                           number of headers in the CSV

        '''
        # Must provide values for each header
        if len(items) != self.numCols():
            raise Exception("Expected %s items, but got %s" % (self.numCols(),
                                                               len(items)))

        itemMap = dict(zip(self.__headers, items))
        self.__addRowMap(itemMap)

    def __addRowMap(self, itemMap):
        '''Add a new row consisting of a dictionary mapping column headers
        to values.

        :param itemMap: The dictionary mapping column headers to values
        :type itemMap: dict

        :raises Exception: If the dictionary contains an entry
                           for an unknown header

        '''
        # Do not allow invalid headers to be added
        invalid = [h for h in itemMap if h not in self.__headers]
        if len(invalid) > 0:
            raise Exception("Attempting to add unknown headers: %s" % invalid)
            
        self.__data.append(itemMap)

    def __validateRow(self, row):
        '''Validate the given row index.

        :param row: The row index
        :type row: int

        :raises Exception: If an invalid row index is given

        '''
        if (row != -1 or self.numRows() == 0) and \
                row not in range(self.numRows()):
            raise Exception("Invalid row: %s" % row)

    def __validateHeader(self, header):
        '''Validate the given header value.

        :param header: The header
        :type header: string

        :raises Exception: If an unknown header is given

        '''
        if header not in self.__headers:
            raise Exception("Invalid header: %s" % header)

    def __str__(self):
        '''Convert the CSV to a string.'''
        lines = [
            self.__delimiter.join(self.__headers),
            ]

        s = [self.getRow(i) for i in range(self.numRows())]
        lines.extend(s)

        return '\n'.join(map(str, lines))
