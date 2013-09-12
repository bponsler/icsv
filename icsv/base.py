from copy import deepcopy


class Cell:
    '''The Cell class encapsulates the data pertaining to a single cell entry
    within a CSV.

    '''

    def __init__(self, row, header, value):
        '''
        :param row: The row index where this cell is located
        :type row: int
        :param header: The column header where this cell is located
        :type header: string
        :param value: The cell value

        '''
        self.__row = row
        self.__header = header
        self.__value = value

    def row(self):
        '''Get the index of the row for this cell.

        :rtype: int

        '''
        return self.__row

    def header(self):
        '''Get the column header for this cell.

        :rtype: string

        '''
        return self.__header

    def value(self):
        '''Get the value for this cell.'''
        return self.__value


class Row:
    '''The Row class encapsulates the data pertaining to a single row of a
    CSV file.

    '''

    def __init__(self, headers, dataMap, delimiter=','):
        '''
        :param headers: The list of column headers
        :type headers: list of strings
        :param dataMap: A dictionary mapping headers to corresponding values
        :type dataMap: dict
        :param delimiter: The CSV delimiter
        :type delimiter: string

        '''
        self.__headers = headers
        self.__dataMap = dataMap
        self.__delimiter = delimiter

    def getCell(self, header):
        '''Get the cell value for the given column header.

        :param header: The column header value
        :type header: string

        :raises Exception: Due to an unknown header value

        '''
        return self[header]

    def dict(self):
        '''Return the row as a dictionary mapping column header values to
        cell values.

        :rtype: dict

        '''
        return deepcopy(self.__dataMap)

    def list(self):
        '''Return the row as a list of cell values in order of the
        column headers.

        :rtype: list

        '''
        return [self.__dataMap.get(header, '') for header in self.__headers]

    def numCols(self):
        '''Get the number of columns in this row.

        :rtype: int

        '''
        return len(self.__headers)

    def __str__(self):
        '''Convert the row to a CSV string.'''
        return self.__delimiter.join(map(str, self.list()))

    def __getitem__(self, header):
        '''Get the cell value for the given column header.

        :param header: The column header value
        :type header: string

        :raises Exception: Due to an unknown header value

        '''
        if header not in self.__headers:
            raise Exception("Invalid header: %s" % header)
        return self.__dataMap.get(header, '')


class Col:
    '''The Col class encapsulates the data pertaining to a single
    column of a CSV file.

    '''

    def __init__(self, header, data):
        '''
        :param header: The column header
        :type header: string
        :param data: The list of row values in this column
        :type data: list

        '''
        self.__header = header
        self.__data = data

    def header(self):
        '''Get the header for this column.

        :rtype: string

        '''
        return self.__header

    def data(self):
        '''Get the list of data values in this column.

        :rtype: list

        '''
        return self.__data

    def numRows(self):
        '''Get the number of rows in this column.

        :rtype: int

        '''
        return len(self.__data)

    def getCell(self, row):
        '''Get a cell value for a specific row in this column.

        :param row: The index of the row where the cell is located
        :type row: int

        :raises Exception: If row is not a valid index

        '''
        return self[row]

    def __getitem__(self, row):
        '''Get a cell value for a specific row in this column.

        :param row: The index of the row where the cell is located
        :type row: int

        :raises Exception: If row is not a valid index

        '''        
        if (row != -1 or self.numRows() == 0) and \
                row not in range(self.numRows()):
            raise Exception("Invalid row: %s" % row)
        return self.__data[row]
