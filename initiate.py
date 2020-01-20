import printdb
import persistence
import sqlite3
import os
import sys
import atexit


def parse_file(filename, repo):
    with open(filename) as inputFile:
        for line in inputFile:
            line = line.strip(' \t\n\r')
            content = line.split(',')
            if line.startswith('E'):
                _id = content[1].strip(' \t\n\r')
                _name = content[2].strip(' \t\n\r')
                _salary = content[3].strip(' \t\n\r')
                _stand = content[4].strip(' \t\n\r')
                repo.employees.insert(persistence.Employee(_id, _name, _salary, _stand))
            elif line.startswith('S'):
                _id = content[1].strip(' \t\n\r')
                _name = content[2].strip(' \t\n\r')
                _information = content[3].strip(' \t\n\r')
                repo.suppliers.insert(persistence.Supplier(_id, _name, _information))
            elif line.startswith('P'):
                _id = content[1].strip(' \t\n\r')
                _description = content[2].strip(' \t\n\r')
                _price = content[3].strip(' \t\n\r')
                _quantity = 0
                repo.products.insert(persistence.Product(_id, _description, _price, _quantity))
            elif line.startswith('C'):
                _id = content[1].strip(' \t\n\r')
                _location = content[2].strip(' \t\n\r')
                _emp = content[3].strip(' \t\n\r')
                repo.coffee_stands.insert(persistence.Coffee_stand(_id, _location, _emp))


def create_tables(repo):
    repo.create_tables()


def main(args):
    if os.path.isfile('moncafe.db'):
        os.remove('moncafe.db')
    _conn = sqlite3.connect('moncafe.db')
    _repo = persistence.startRepo(_conn)
    filename = os.path.abspath(os.path.realpath(sys.argv[1]))
    create_tables(_repo)
    parse_file(filename, _repo)
    _repo._close()


if __name__ == '__main__':
    main(sys.argv)
