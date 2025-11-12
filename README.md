# MMS-Calculator
@Author Ryan Yuncza

A program which uses a brute force technique to determine whether or not MMS exists for a given allocation problem

Dependences:
- Numpy
- Pandas

Included files:
- CostMatrixGenerator.py
- MMS.py
- Parser.py
- SharingParser.py

MMS:
- Where the actual computations are done to calculate MMS and test if it exists

CostMatrixGenerator:
- Randomly generates a bunch of CSV files with a given specfication

How to run Pasers:
Choose your parser that you wish to use
- Parser.py will just check if MMS exists
- SharingParser.py will first check if MMS exists, then will check if MMS exists with sharing

Then run the script in the terminal with the following structure:
- The inputs for both parsers is a directory full of CSV files or a single CSV file that represents a cost matrix
- All resulting output will be printed to the terminal.

ex: python3 Parser.py CSVFiles/2x10