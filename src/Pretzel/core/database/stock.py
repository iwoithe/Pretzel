import sqlite3


def load_stock(database: str = "data/databases/data.db") -> list:
    con = sqlite3.connect(database)
    items_tuple = con.execute("SELECT * FROM stock;").fetchall()

    # No changes made, don't need to save the database
    con.close()

    items = []
    for item in items_tuple:
        item_dict = {
            "Name": item[0],
            "Quantity": item[1],
            "Unit": item[2],
            "Cost": item[3],
        }
        items.append(item_dict)

    return items


def load_stock_names(database: str = "data/databases/data.db") -> list:
    con = sqlite3.connect(database)
    items_tuple = con.execute("SELECT * FROM stock;").fetchall()

    # No changes made, don't need to save the database
    con.close()

    items = []
    for item in items_tuple:
        item_dict = {
            "Name": item[0],
            "Quantity": 0.0,
            "Unit": item[2],
            "Cost": 0.0,
        }
        items.append(item_dict)

    return items


def add_stock(items: list, database: str = "data/databases/data.db"):
    # Open the database
    con = sqlite3.connect(database)

    # Update the quantity
    new_quantity = []
    for item in items:
        new_quantity.append([item[1], item[0]])

    old_quantity = []

    for q in new_quantity.copy():
        new_total = con.execute("SELECT quantity FROM stock WHERE name = (?)", (q[1],)).fetchall()[0]
        old_quantity.append([new_total, q[1]])

    quantity = []
    for q in old_quantity:
        new_quan = float(q[0][0] + new_quantity[old_quantity.index(q)][0])
        quantity.append([new_quan, q[1]])

    con.executemany("UPDATE stock SET quantity = ? WHERE name = ?", quantity)

    # Update the units
    units = []
    for item in items:
        units.append((item[2], item[0]))

    con.executemany("UPDATE stock SET unit = ? WHERE name = ?", units)

    # Update the cost
    new_cost = []
    for item in items:
        new_cost.append([item[3], item[0]])

    old_cost = []

    for c in new_cost.copy():
        new_total = con.execute("SELECT cost FROM stock WHERE name = (?)", (c[1],)).fetchall()[0]
        old_cost.append([new_total, c[1]])

    cost = []
    for c in old_cost:
        new_c = float(c[0][0] + new_cost[old_cost.index(c)][0])
        cost.append([new_c, c[1]])

    con.executemany("UPDATE stock SET cost = ? WHERE name = ?", cost)

    # Save changes to the database and close
    con.commit()
    con.close()


def remove_stock(items: list, database: str = "data/databases/data.db"):
    # Open the database
    con = sqlite3.connect(database)

    # Update the quantity
    new_quantity = []
    for item in items:
        new_quantity.append([item[1], item[0]])

    old_quantity = []

    for q in new_quantity.copy():
        new_total = con.execute("SELECT quantity FROM stock WHERE name = (?)", (q[1],)).fetchall()[0]
        old_quantity.append([new_total, q[1]])

    quantity = []
    for q in old_quantity:
        new_quan = float(q[0][0] - new_quantity[old_quantity.index(q)][0])
        quantity.append([new_quan, q[1]])

    con.executemany("UPDATE stock SET quantity = ? WHERE name = ?", quantity)

    # Don't need to update the unit or cost

    # Save changes to the database and close
    con.commit()
    con.close()