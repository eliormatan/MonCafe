import sqlite3
import atexit


# Data Transfer Objects:
class Employee(object):
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand= coffee_stand


class Product(object):
    def __init__(self, id, description, price,quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


class Coffee_stand(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

class Activity(object):
    def __init__(self, product_id, quantity, activator_id,date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date


# Data Access Objects:
# All of these are meant to be singletons
class _Employee:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, employee):
        self._conn.execute("""
               INSERT INTO Employees (id, name,salary,coffee_stand) VALUES (?, ?, ?, ?)
           """, [employee.id, employee.name,employee.salary,employee.coffee_stand])

    def find(self, employee):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name,salary,coffee_stand FROM Employees WHERE id = ?
        """, [employee.id])

        return Employee(*c.fetchone())

class _Supplier:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
               INSERT INTO Employees (id, name,contact_information) VALUES (?, ?, ?)
           """, [supplier.id, supplier.name,supplier.contact_information])

    def find(self, employee):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name,salary,coffee_stand FROM Employees WHERE id = ?
        """, [employee.id])

        return Employee(*c.fetchone())


class _Product:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, product):
        self._conn.execute("""
                INSERT INTO Products (id, description,price,quantity) VALUES (?, ?, ?, ?)
        """, [product.id, product.description, product.price, product.quantity])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM assignments WHERE num = ?
            """, [id])

        return Product(*c.fetchone())


class _Coffee_stand:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("""
            INSERT INTO Coffee_stands (id, location, number_of_employees) VALUES (?, ?, ?)
        """, [coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT student_id, assignment_num, grade FROM grades
        """).fetchall()

        return Coffee_stand(*c.fetchone())

class _Activity:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, activity):
        self._conn.execute("""
            INSERT INTO Activitys (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)
        """, [activity.product_id, activity.quantity, activity.activator_id, activity.date])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT * grade FROM Activitys
        """).fetchall()

        return Activity(*c.fetchone())


# The Repository
class _Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('grades.db')
        self.employee = _Employee(self._conn)
        self.supplier = _Supplier(self._conn)
        self.product = _Product(self._conn)
        self.activity = _Activity(self._conn)
        self._Coffee_stand = _Coffee_stand(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE students (
                id      INT         PRIMARY KEY,
                name    TEXT        NOT NULL
            );

            CREATE TABLE assignments (
                num                 INT     PRIMARY KEY,
                expected_output     TEXT    NOT NULL
            );

            CREATE TABLE grades (
                student_id      INT     NOT NULL,
                assignment_num  INT     NOT NULL,
                grade           INT     NOT NULL,

                FOREIGN KEY(student_id)     REFERENCES students(id),
                FOREIGN KEY(assignment_num) REFERENCES assignments(num),

                PRIMARY KEY (student_id, assignment_num)
            );
        """)


# see code in previous version...

# the repository singleton
repo = _Repository()
atexit.register(repo._close)
