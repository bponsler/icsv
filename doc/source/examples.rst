================================================================================
Examples
================================================================================

Examples of how to use icsv...

----------------
Basics
----------------

It is easy to create CSV objects::

    from icsv import icsv

    headers = ["Header 1", "Second Header", "Three"]
    i = icsv(headers)

Which can be used to add new rows of data::

    # The following are valid, and equivalent
    i.addRow([0, 1, 2])
    i.addRow({"Header 1": 0, "Second Header": 1, "Three": 2})  # Order does not matter

    # The following raise Exceptions
    i.addRow([0, 1])          # Not enough items
    i.addRow({"Unknown": 7})  # An unknown header value

It is also easy to set the value of specific cells::

    # These are equivalent
    i.setCell("Header 1", 5)                     # Default row is -1 (last row)
    i.setCell("Header 1", 5, -1)
    i.setCell("Header 1", 5, (i.numRows() - 1))

    # These are not valid
    i.setCell("Unknown", 11)                     # Unknown header
    i.setCell("Header 1", 100, i.numRows())      # Row index out of range
    i.setCell("Header 1", 100, -2)               # Invalid row index

Accessing CSV data is also easy::

    # Access specific rows
    row = i.getRow()                           # Default row is -1 (last row)
    row = i.getRow(-1)                         # Same as above
    row = i.getRow(i.numRows() - 1)            # Save as above
    row = i.getRow(0)

    # Access specific columns
    col = i.getCol("Header 1")
    col = i.getCol("Second Header")
    col = i.getCol("Three")

    # Access specific cells
    cell = i.getCell(0, "Header 1")
    cell = i.getCell((i.numRows() - 1), "Second Header")
    cell = i.getCell(1, "Third")

    # The following are invalid
    row = i.getRow(-2)                         # Invalid row index
    row = i.getRow(i.numRows())                # Row index out of range
    col = i.getCol("Unknown")                  # Unknown column header
    cell = i.getCell(-2, "Header 1")           # Invalid row index
    cell = i.getCell(i.numRows(), "Header 1")  # Row index out of range
    cell = i.getCell(0, "Unknown")             # Unknown column header

-------------------------
Writing a CSV file
-------------------------

There are two simple ways to write a CSV file.

The first is to create a :class:`icsv.Writer` object::

    from icsv import Writer

    headers = ["Header 1", "Second Header", "Third"]
    writer = Writer("/tmp/test.csv", headers)

    # Optional constructor aguments
    #    delimiter -- The CSV delimiter string (',' by default)
    #    useHeaders -- True (default) will write the headers as the
    #                  first line of the CSV file, False will not
    #    overwrite -- True (default) will overwrite existing CSV files
    #                 False will raise an Exception on existing files

Now you can write new rows to the CSV file::

    # The following lines are equivalent
    writer.writeRow([0, 1, 2])
    writer.writeRow({"Third": 2, "Second Header": 1, "Header 1": 0})  # Order does not matter

The :func:`icsv.Writer.writeRow` will write the data to the CSV file immediately.

The second way to write a CSV file is by using a pre-existing :class:`icsv.icsv` object as such::

    from icsv import icsv, Writer

    headers = ["Header 1", "Second Header", "Third"]
    i = icsv(headers)

    # Add a few rows to the CSV
    i.addRow([0, 1, 2])
    i.addRow(["Types", "do not", "matter"])
    i.addRow({"Third": True})

    # Write all of the CSV data to the file, and get a Writer
    writer = i.write("/tmp/test.csv")
    writer = Writer.fromCsv("/tmp/test.csv", i)  # Same as above

    # Optional constructor aguments
    #    useHeaders -- True (default) will write the headers as the
    #                  first line of the CSV file, False will not
    #    overwrite -- True (default) will overwrite existing CSV files
    #                 False will raise an Exception on existing files

    # Now the writer can be used to write additonal data
    writer.writeRow(["a", "b", "c"])


-------------------------
Reading a CSV file
-------------------------

Reading data from a CSV file is very easy::

    from icsv import icsv

    # Automatically read CSV headers from the first line of the CSV file
    i = icsv.fromFile("/tmp/test.csv")

    # Or, specify the headers and delimiter
    headers = ["Header 1", "Second Header", "Third"]
    i = icsv.fromFile("/tmp/test.csv", headers=headers, delimiter=',')

    # Now the data is accessible
    print i

-------------------------
Advanced
-------------------------

It is easy to filter CSV data::

    from icsv import icsv

    headers = ["Header 1", "Second Header", "Third"]
    i = icsv(headers)

    # Add some data
    i.addRow([0, 1, 2, 3])
    i.addRow([4, 5, 6, 7])
    i.addRow([8, 9, 10, 11])

    def evenCells(rowIndex, colHeader, cellValue):
        return (cellValue % 2) == 0

    # Get a list of the CSV cells with even values
    f = i.filter(evenCells)

    for c in f:
        print c.row(), c.header(), c.value()

It is also easy to transform the CSV data::

    from icsv import icsv

    headers = ["Header 1", "Second Header", "Third"]
    i = icsv(headers)

    # Add some data
    i.addRow([0, 1, 2, 3])
    i.addRow([4, 5, 6, 7])
    i.addRow([8, 9, 10, 11])

    def addValue(rowIndex, colHeader, cellValue):
        if rowIndex == 2:
            cellValue += 1

        return cellValue

    # Transform the data
    i2 = i.map(addValue)  # i remains unchanged

    # View the CSV data
    for rowIndex in range(i2.numRows()):
        row = i2.getRow(rowIndex)
        print "[%d]: %s" % (rowIndex, row)

    # Or, transform the CSV
    i.map(addValue, overwrite=True)  # i is changed

    # View the CSV data
    for rowIndex in range(i.numRows()):
        row = i.getRow(rowIndex)
        print "[%d]: %s" % (rowIndex, row)
