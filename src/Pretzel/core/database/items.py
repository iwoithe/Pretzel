import sqlite3


from Pretzel.core.models import PictogramModel


def load_items(database: str = "data/databases/data.db") -> list:
    con = sqlite3.connect(database)
    items_tuple = con.execute("SELECT * FROM items;").fetchall()

    # No changes made, don't need to save the database
    con.close()

    items = []
    for item in items_tuple:
        pictogram_list = []
        for pictogram_path in item[-1].split(","):
            pictogram_list.append(pictogram_path)

        pictogram_list.pop(-1)

        pictogram_model = PictogramModel(pictograms=pictogram_list)

        item_dict = {
            "Name": item[0],
            "Chemical Formula": item[1],
            "Warning Label": item[2],
            "Danger Level": item[3],
            "Notes": item[4],
            "Pictograms": pictogram_model
        }

        items.append(item_dict)

    return items


def add_items(items: list, database: str = "data/databases/data.db"):
    con = sqlite3.connect(database)
    con.executemany("INSERT INTO items(name, chemical_formula, warning_label, danger_level, notes, pictograms) values (?, ?, ?, ?, ?, ?)", items)

    item_names = []
    for item in items:
        item_names.append([item[0]])

    con.executemany("INSERT INTO stock(name, quantity, unit, cost) values (?, 0, 'None', 0)", item_names)

    con.commit()
    con.close()


def remove_items(items: list, database: str = "data/databases/data.db"):
    """
    :param items: The items to remove from the database
    :type items: list
    :param database: The database to remove the items from
    :type database: str
    """
    con = sqlite3.connect(database)

    con.executemany("DELETE FROM items WHERE name = ?;", (items,))
    con.executemany("DELETE FROM stock WHERE name = ?;", (items,))

    con.commit()
    con.close()


def edit_items(items: list, database: str = "data/databases/data.db"):
    con = sqlite3.connect(database)

    # Update the names
    # item[0] = Old Name, item[1] = New Name
    names = []
    for item in items:
        names.append([item[1], item[0]])

    con.executemany("UPDATE items SET name = ? WHERE name = ?", names)
    con.executemany("UPDATE stock SET name = ? WHERE name = ?", names)

    # Update the chemical formulas
    chem_formulas = []
    for item in items:
        chem_formulas.append([item[2], item[1]])

    con.executemany("UPDATE items SET chemical_formula = ? WHERE name = ?", chem_formulas)

    # Update the warning labels
    warning_labels = []
    for item in items:
        warning_labels.append([item[3], item[1]])

    con.executemany("UPDATE items SET warning_label = ? WHERE name = ?", warning_labels)

    # Update the danger levels
    danger_levels = []
    for item in items:
        danger_levels.append([item[4], item[1]])

    con.executemany("UPDATE items SET danger_level = ? WHERE name = ?", danger_levels)

    # Update the notes
    notes = []
    for item in items:
        notes.append([item[5], item[1]])

    con.executemany("UPDATE items SET notes = ? WHERE name = ?", notes)

    # Update the notes
    pictograms = []
    for item in items:
        pictograms.append([item[6], item[1]])

    con.executemany("UPDATE items SET pictograms = ? WHERE name = ?", pictograms)

    con.commit()
    con.close()
