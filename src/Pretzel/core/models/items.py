import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ItemsModel(QAbstractListModel):
    def __init__(self, *args, items=None, pictograms=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.items = items or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            data = self.items[index.row()]
            return data["Name"]
        else:
            pass

    def rowCount(self, parent=None):
        return len(self.items)

    def update(self):
        self.layoutChanged.emit()


class PictogramModel(QAbstractListModel):
    def __init__(self, *args, pictograms=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.pictograms = pictograms or []

    def data(self, index, role):
        if role == Qt.DecorationRole:
            data = QPixmap(self.pictograms[index.row()])
            return data

    def rowCount(self, parent=None):
        return len(self.pictograms)

    def update(self):
        self.layoutChanged.emit()


class ItemsTableModel(QAbstractTableModel):
    def __init__(self, *args, headers=None, items=None, **kwargs):
        super().__init__()

        self.headers = headers or []
        self.items = items or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            data = self.items[index.row()][index.column()]
            return data
        if role == Qt.TextAlignmentRole:
            # Use following lines for specific types
            # value = self.items[index.row()][index.column()]
            # if isinstance(value, int) or isinstance(value, float):
            return Qt.AlignVCenter | Qt.AlignHCenter

    def rowCount(self, parent=None):
        return len(self.items)

    def columnCount(self, parent=None):
        if self.items:
            return len(self.items[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def update(self):
        self.layoutChanged.emit()

    def mirror_model(self, model: ItemsModel):
        """ Mirrors this model with another model

        :param model: The model to mirror
        :type model: ItemsModel """

        self.items = model.items
        self.update()

