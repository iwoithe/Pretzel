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
