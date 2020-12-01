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
    a list to store the stock instead of a dictionary.
     If needed, will use it with the QDataWidgetMapper
     class """
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

    def mirror_model(self, model: StockModel):
        """ Mirrors this model with another model

        :param model: The model to mirror
        :type model: StockModel """

        self.stock = list([model.stock[0], model.stock[1], model.stock[2], model.stock[3]])
        self.update()


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


class StockTableModel(QAbstractTableModel):
    def __init__(self, *args, headers=None, stock=None, **kwargs):
        super().__init__()

        self.headers = headers or []
        self.stock = stock or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            data = self.stock[index.row()][index.column()]
            return data
        if role == Qt.TextAlignmentRole:
            # Use following lines for specific types
            # value = self.stock[index.row()][index.column()]
            # if isinstance(value, int) or isinstance(value, float):
            return Qt.AlignVCenter | Qt.AlignHCenter

    def rowCount(self, parent=None):
        return len(self.stock)

    def columnCount(self, parent=None):
        if self.stock:
            return len(self.stock[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def update(self):
        self.layoutChanged.emit()

    def mirror_model(self, model: StockModel):
        """ Mirrors this model with another model

        :param model: The model to mirror
        :type model: StockModel """

        self.stock = model.stock
        self.update()
