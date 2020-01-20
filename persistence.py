import sqlite3
import atexit


# Data Transfer Objects:
class Employee(object):
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand

    def __str__(self):
        str = "({}, '{}', {}, {})".format(self.id, self.name, self.salary, self.coffee_stand)
        return str


class Product(object):
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        str = "({}, '{}', {}, {})".format(self.id, self.description, self.price, self.quantity)
        return str


class Supplier(object):
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

    def __str__(self):
        str = "({}, '{}', '{}')".format(self.id, self.name, self.contact_information)
        return str


class Coffee_stand(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

    def __str__(self):
        str = "({}, '{}', {})".format(self.id, self.location, self.number_of_employees)
        return str


class Activity(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date

    def __str__(self):
        str = '({}, {}, {}, {})'.format(self.product_id, self.quantity, self.activator_id, self.date)
        return str


# Data Access Objects:
# All of these are meant to be singletons
class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, employee):
        self._conn.execute("""
               INSERT INTO Employees (id, name,salary,coffee_stand) VALUES (?, ?, ?, ?)
           """, [employee.id, employee.name, employee.salary, employee.coffee_stand])

    def find(self, employee):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name,salary,coffee_stand FROM Employees WHERE id = (?)
        """, [employee.id])

        return Employee(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT id, name, salary, coffee_stand FROM Employees
            ORDER BY id
        """).fetchall()

        return [Employee(*row) for row in all]

    def findWorker(self, workID):
        c = self._conn.cursor()
        c.execute("""
                SELECT name FROM Employees
                WHERE id=(?)
            """, [workID])
        ans = c.fetchone()
        if ans is None:
            return "None"
        return ans[0]


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
               INSERT INTO Suppliers (id, name,contact_information) VALUES (?, ?, ?)
           """, [supplier.id, supplier.name, supplier.contact_information])

    def find(self, supplier):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Suppliers WHERE id = ?
        """, [supplier.id])

        return Employee(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT * FROM Suppliers
            ORDER BY id
        """).fetchall()

        return [Supplier(*row) for row in all]

    def findSupplier(self, supID):
        c = self._conn.cursor()
        c.execute("""
                SELECT name FROM Suppliers
                WHERE id=(?)
            """, [supID])
        ans = c.fetchone()
        if ans is None:
            return "None"
        return ans[0]


class _Products:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, product):
        self._conn.execute("""
                INSERT INTO Products (id, description, price, quantity) VALUES (?, ?, ?, ?)
        """, [product.id, product.description, product.price, product.quantity])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM Products WHERE id = ?
            """, [id])

        return Product(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT * FROM Products
            ORDER BY id
        """).fetchall()

        return [Product(*row) for row in all]

    def checkIfLeagl(self, idToCheck, quantityToCheck):
        ans = self.find(idToCheck)
        if ans.quantity >= int(quantityToCheck):
            return 1
        return 0

    def updateQuantity(self, idToUpdate, amountToUpdate):
        c = self._conn.cursor()
        ans = self.find(idToUpdate)
        newQuan = ans.quantity + int(amountToUpdate)
        c.execute("""
                UPDATE Products SET quantity=(?) WHERE id=(?)
            """, [newQuan, idToUpdate])

    def getProductPrice(self, proID):
        c = self._conn.cursor()
        c.execute("""
                SELECT price FROM Products WHERE id = (?)
            """, [proID])

        return c.fetchone()[0]

    def getProductName(self, proID):
        c = self._conn.cursor()
        c.execute("""
                SELECT description FROM Products WHERE id = (?)
            """, [proID])

        return c.fetchone()[0]


class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("""
            INSERT INTO Coffee_stands (id, location, number_of_employees) VALUES (?, ?, ?)
        """, [coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT id, location, number_of_employees FROM Coffee_stands
            ORDER BY id
        """).fetchall()

        return [Coffee_stand(*row) for row in all]

    def findLocationByID(self, standID):
        c = self._conn.cursor()
        ans = c.execute("""
                    SELECT location FROM Coffee_stands
                    WHERE id=(?)
                """, [standID]).fetchone()
        return ans[0]


class _Activitys:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, activity):
        self._conn.execute("""
            INSERT INTO Activities (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)
        """, [activity.product_id, activity.quantity, activity.activator_id, activity.date])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT * FROM Activities
            ORDER BY date
        """).fetchall()

        return [Activity(*row) for row in all]

    def findProfitByID(self, actId, repo):
        total = 0
        c = self._conn.cursor()
        all = c.execute("""
                    SELECT product_id,quantity FROM Activities
                    WHERE activator_id=(?)
                """, [actId]).fetchall()
        for quan in all:
            proID = quan[0]
            quantity = quan[1]
            price = repo.products.getProductPrice(proID)
            total += abs(quantity * price)
        return total

    # The Repository


class _Repository(object):
    def __init__(self, _conn):
        self.conn = _conn
        self.employees = _Employees(self.conn)
        self.suppliers = _Suppliers(self.conn)
        self.products = _Products(self.conn)
        self.activitys = _Activitys(self.conn)
        self.coffee_stands = _Coffee_stands(self.conn)

    def _close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.executescript("""
            CREATE TABLE Employees (
                id      INTEGER        PRIMARY KEY,
                name    TEXT        NOT NULL,
                salary  REAL    NOT NULL,
                coffee_stand    INTEGER REFERENCES  Coffee_stand(id)
            );

            CREATE TABLE Suppliers (
                id                 INTEGER     PRIMARY KEY,
                name     TEXT    NOT NULL,
                contact_information  REAL
            );

            CREATE TABLE Products (
                id      INTEGER     PRIMARY KEY,
                description  TEXT     NOT NULL,
                price           REAL     NOT NULL,
                quantity    INTEGER NOT NULL
            );
            
            CREATE TABLE Coffee_stands (
                id  INTEGER PRIMARY KEY,
                location TEXT    NOT NULL,
                number_of_employees INTEGER
            );
            CREATE TABLE Activities (
                product_id INTEGER  INTEGER REFERENCES  Product(id),
                quantity INTEGER    NOT NULL,
                activator_id INTEGER NOT NULL,
                date    DATE    NOT NULL
                
            );
            """)


def startRepo(_conn):
    repo = _Repository(_conn)
    return repo
