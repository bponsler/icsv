================================================================================
Introduction
================================================================================

The icsv project was designed to make dealing with typical CSV files much
easier and straight forward.

The typical structure of a CSV file (with m rows and n columns) is as follows::

    Header 1,Header 2,Header 3,...,Header n-1,Header n
    value 1x1,value 1x2,value 1x3,...,value 1xn-1,value 1xn
    ...
    value mx1,value mx2,value mx3,...,value mxn-1,value mxn

This file format defines the column headers on the first line of the file and
defines the data in each row as a subsequent line in the file.

icsv provides an interface for storing CSV data as well as writing this data
to CSV files, and reading the data from CSV files.
