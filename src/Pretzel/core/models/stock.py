from PyQt5.QtCore import *


class StockModel(QAbstractListModel):
    def __init__(self, *args, stock=None, **kwargs):
        super().__init__()

        self.stock = stock or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            data = self.stock[index.row()]
            return data["Name"]
        else:
            pass

    def rowCount(self, parent=None):
        return len(self.stock)

    def update(self):
        self.layoutChanged.emit()


class StockListModel(QAbstractListModel):
    """ This is the same as StockModel however it uses
    a list to store the stock instead of a dictionary """
    def __init__(self, *args, stock=None, **kwargs):
        super().__init__()

        self.stock = stock or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            data = self.stock[index.row()]
            return data[0]

    def rowCount(self, parent=None):
        return len(self.stock)

    def update(self):
        self.layoutChanged.emit()


class StockQuantityModel(QAbstractListModel):
    """ This is the same as StockModel however it uses
    a list to store the stock instead of a dictionary """
    def __init__(self, *args, stock=None, **kwargs):
        super().__init__()

        self.stock = stock or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            data = self.stock[index.row()]
            return data["Name"]

    def rowCount(self, parent=None):
        return len(self.stock)

    def update(self):
        self.layoutChanged.emit()