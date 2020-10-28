import sqlite3


from core.models.items import PictogramModel


def load_items(database: str = "data/databases/data.db"):
    con = sqlite3.connect(database)
    items_tuple = con.execute("SELECT * FROM items;").fetchall()

    # No changes made, don't need to save the database
    con.close()

    items = []
    for item in items_tuple:
        pictogram_list = []
        for pictogram_path in item[-1].split(","):
            pictogram_list.append(pictogram_path)

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

    con.commit()
    con.close()