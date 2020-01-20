import sqlite3
import persistence


def main():
    conn = sqlite3.connect('moncafe.db')
    repo = persistence.startRepo(conn)
    list = repo.activitys.find_all()
    print("Activities")
    for item in list:
        print(item)
    list = repo.coffee_stands.find_all()
    print("Coffee stands")
    for item in list:
        print(item)
    list = repo.employees.find_all()
    print("Employees")
    for item in list:
        print(item)
    list = repo.products.find_all()
    print("Products")
    for item in list:
        print(item)
    list = repo.suppliers.find_all()
    print("Suppliers")
    for item in list:
        print(item)
    print("")
    print("Employees Report")
    list = repo.employeesReport.find_all(repo)
    for item in list:
        print(item)
    list = repo.activitys.find_all()
    if len(list) != 0:
        print("")
        print("Activities")
        list = repo.activitiesReport.find_all()
        for item in list:
            print(item)
    repo._close()


if __name__ == '__main__':
    main()
