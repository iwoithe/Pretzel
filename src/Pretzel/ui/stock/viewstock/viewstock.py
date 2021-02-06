import sys

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Pretzel.core.database import utils
from Pretzel.core.database.stock import load_stock
from Pretzel.core.models import StockModel, StockTableModel


class ViewStock(QDockWidget):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.stock_model = StockModel()
        self.table_model = StockTableModel(headers=["Name", "Quantity", "Unit", "Cost"])

        self.setup_ui()

    def setup_ui(self):
        # TODO: Add QStackedLayout for different filter options (not just name)
        uic.loadUi("Pretzel/ui/stock/viewstock/viewstock.ui", self)

        # Setup the table
        self.stock_view.setAlternatingRowColors(True)
        self.stock_view.setSortingEnabled(True)

        # Setup the sorting
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.table_model)
        self.proxy_model.setFilterKeyColumn(0)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # Setup the models
        self.stock_view.setModel(self.proxy_model)
        self.load_stock()

        self.bind_signals()

    def bind_signals(self):
        self.filter_entry.textEdited.connect(self.filter_items)

    def load_stock(self):
        stock = []
        for s in load_stock(database=utils.get_database_path()):
            stock.append(list(s.values()))

        self.stock_model.stock = stock
        self.stock_model.update()
        self.table_model.layoutAboutToBeChanged.emit()
        self.table_model.mirror_model(self.stock_model)

    @pyqtSlot(str)
    def filter_items(self, text: str):
        # Filter the packages
        self.proxy_model.setFilterFixedString(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    viewstock = ViewStock()
    viewstock.show()
    sys.exit(app.exec())
