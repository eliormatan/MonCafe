from persistence import repo
import persistence
import sqlite3
import os
import sys
import atexit


def parse_file(filename, cursor):
    file = open(filename)
    for line in file:
        line = line.strip(' \t\n\r')
        content = line.split(',')
    if line.startswith('E'):
        _id = content[1].strip(' \t\n\r')
        _name = content[2].strip(' \t\n\r')
        _salary = content[3].strip(' \t\n\r')
        _stand = content[4].strip(' \t\n\r')
        repo.employee.insert(persistence.Employee(_id, _name, _salary, _stand))
    elif line.startswith('S'):
        _id = content[1].strip(' \t\n\r')
        _name = content[2].strip(' \t\n\r')
        _information = content[3].strip(' \t\n\r')
        repo.supplier.insert(persistence.Supplier(_id, _name, _information))
    elif line.startswith('P'):
        _id = content[1].strip(' \t\n\r')
        _description = content[2].strip(' \t\n\r')
        _price = content[3].strip(' \t\n\r')
        _quantity = content[4].strip(' \t\n\r')
        repo.product.insert(persistence.Product(_id, _description, _price, _quantity))
    elif line.startswith('C'):
        _id = content[1].strip(' \t\n\r')
        _location = content[2].strip(' \t\n\r')
        _emp = content[3].strip(' \t\n\r')
        repo.coffee_stand(persistence.Coffee_stand(_id, _location, _emp))


def create_tables(cursor):
    repo.create_tables()


def close_db(dbcon):
    dbcon.commit()
    dbcon.close()
    os.remove('moncafe.db')

atexit.register(close_db)


def main(args):
    DBExist = os.path.isfile('moncafe.db')
    dbcon = sqlite3.connect('moncafe.db')
    with dbcon:
        cursor = dbcon.cursor()
        filename = os.path.abspath(os.path.realpath(sys.argv[0]))
    if DBExist:
        os.remove('moncafe.db')
    if not DBExist:
        create_tables(cursor)
        parse_file(filename, cursor)


if __name__ == '__main__':
    main(sys.argv)
