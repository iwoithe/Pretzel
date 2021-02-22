from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Pretzel.core import converter
from Pretzel.core.database import items


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

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemIsEnabled

        return QAbstractItemModel.flags(self, index) | Qt.ItemIsEditable

    def data(self, index, role):
        if role == Qt.DisplayRole:
            data = self.items[index.row()][index.column()]
            return data
        if role == Qt.EditRole:
            data = self.items[index.row()][index.column()]
        if role == Qt.TextAlignmentRole:
            # Use following lines for specific types
            # value = self.items[index.row()][index.column()]
            # if isinstance(value, int) or isinstance(value, float):
            return Qt.AlignVCenter | Qt.AlignHCenter

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        if index.isValid() and (role == Qt.EditRole):
            # Get the required data before it changes
            old_name = self.items[index.row()][0]
            item = items.load_items()[index.row()]
            notes = item["Notes"]
            pictograms = converter.list_to_string(item["Pictograms"].pictograms)

            # Update the view
            self.items[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, {role})

            # Save to the database
            if index.column() == 0:
                new_name = value
                items.edit_items([(old_name,
                                   new_name,
                                   self.items[index.row()][1],
                                   self.items[index.row()][2],
                                   self.items[index.row()][3],
                                   notes,
                                   pictograms)])
            elif index.column() == 1:
                new_chem_formula = value
                items.edit_items([(old_name,
                                   self.items[index.row()][0],
                                   new_chem_formula,
                                   self.items[index.row()][2],
                                   self.items[index.row()][3],
                                   notes,
                                   pictograms)])
            elif index.column() == 2:
                new_warning_label = value
                items.edit_items([(old_name,
                                   self.items[index.row()][0],
                                   self.items[index.row()][1],
                                   new_warning_label,
                                   self.items[index.row()][3],
                                   notes,
                                   pictograms)])
            elif index.column() == 3:
                new_danger_level_label = value
                items.edit_items([(old_name,
                                   self.items[index.row()][0],
                                   self.items[index.row()][1],
                                   self.items[index.row()][2],
                                   new_danger_level_label,
                                   notes,
                                   pictograms)])
            else:
                pass

            return True

        return False

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
