import sys

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Pretzel.core.database.items import load_items
from Pretzel.core.models import ItemsModel, ItemsTableModel


class ViewItems(QDockWidget):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.items_model = ItemsModel()
        # TODO: Add the ability to (at least) copy the notes
        # TODO: Add the ability to view the pictograms in self.items_view
        self.table_model = ItemsTableModel(headers=["Name", "Chemical Formula", "Warning Label", "Danger Level"])#, "Notes", "Pictograms"])

        self.setup_ui()

    def setup_ui(self):
        # TODO: Add QStackedLayout for different filter options (not just name)
        uic.loadUi("Pretzel/ui/items/viewitems/viewitems.ui", self)

        # Setup the table
        self.items_view.setAlternatingRowColors(True)
        self.items_view.setSortingEnabled(True)

        # Setup the sorting
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.table_model)
        self.proxy_model.setFilterKeyColumn(0)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # Setup the models
        self.items_view.setModel(self.proxy_model)
        self.load_stock()

        self.bind_signals()

    def bind_signals(self):
        self.filter_entry.textEdited.connect(self.filter_items)

    def load_stock(self):
        items = []
        for i in load_items():
            items.append(list(i.values())[:-2])

        self.items_model.items = items
        self.items_model.update()
        self.table_model.layoutAboutToBeChanged.emit()
        self.table_model.mirror_model(self.items_model)

    @pyqtSlot(str)
    def filter_items(self, text: str):
        # Filter the packages
        self.proxy_model.setFilterFixedString(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    viewitems = ViewItems()
    viewitems.show()
    sys.exit(app.exec())