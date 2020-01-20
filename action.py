import os
import sys
import persistence
import printdb
import sqlite3


def action(filename):
    with open(filename) as inputFile:
        _conn = sqlite3.connect('moncafe.db')
        repo = persistence.startRepo(_conn)
        for line in inputFile:
            seperate = line.split(',')
            productID = seperate[0].strip(' \t\n\r')
            quantity = seperate[1].strip(' \t\n\r')
            activatorID = seperate[2].strip(' \t\n\r')
            date = seperate[3].strip(' \t\n\r')
            if int(quantity) < 0:
                ans = repo.products.checkIfLeagl(productID, abs(int(quantity)))
                if ans == 1:
                    repo.activitys.insert(persistence.Activity(productID, quantity, activatorID, date))
                    repo.products.updateQuantity(productID, quantity)
            else:
                repo.activitys.insert(persistence.Activity(productID, quantity, activatorID, date))
                repo.products.updateQuantity(productID, quantity)
        repo._close()


def main(args):
    DBExist = os.path.isfile('moncafe.db')
    if DBExist:
        filename = os.path.abspath(os.path.realpath(sys.argv[1]))
        action(filename)
        printdb.main()


if __name__ == '__main__':
    main(sys.argv)
