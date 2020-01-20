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
    list = repo.activitys.find_all()
    if len(list) != 0:
        print("")
        print("Employees Report")
        list = repo.employees.find_all()
        for item in list:
            str = '({} {} {} {})'.format(item.name, item.salary, repo.coffee_stands.findLocationByID(item.coffee_stand),
                                         repo.activitys.findProfitByID(item.id, repo))
            print(str)
        print("")
        list = repo.activitys.find_all()
        print("Activities")
        for item in list:
            emp = repo.employees.findWorker(item.activator_id)
            sup = repo.suppliers.findSupplier(item.activator_id)
            modEmp = emp
            if emp != "None":
                modEmp = ("'{}'").format(emp)
            modSup = sup
            if sup != "None":
                modSup = ("'{}'").format(sup)
            str = '({}, {}, {}, {}, {})'.format(item.date, ("'{}'").format(repo.products.getProductName(item.product_id)), item.quantity,
                                                modEmp,
                                                modSup)
            print(str)
    repo._close()


if __name__ == '__main__':
    main()
