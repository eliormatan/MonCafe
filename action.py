import os
import sys
import printdb
import sqlite3


def main(args):
    DBExist = os.path.isfile('moncafe.db')
    if DBExist:
        action(sys.args[0])

if __name__ == '__main__':
    main(sys.argv)

def action(filename):
    with open(filename) as inputFile:
        for line in inputFile:
            seperate = line.split(',')
            productID = seperate[0]
            quantity = seperate[1]
            activatorID = seperate[2]
            date = seperate[3]



