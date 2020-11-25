#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2020 iwoithe <iwoithe@just42.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import sys

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Pretzel.constants import *
from Pretzel.ui.dialogs import AddItemsDialog
from Pretzel.core.models import StockQuantityModel
from Pretzel.core.database.stock import remove_stock


class RemoveStock(QDockWidget):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Create the model
        self.stock_model = StockQuantityModel()

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pretzel/ui/stock/removestock/removestock.ui", self)

        self.previous_index = None

        # Setup up the items list
        self.items_list.setModel(self.stock_model)

        self.bind_signals()

    def bind_signals(self):
        self.button_add_items.clicked.connect(self.add_stock)
        self.button_remove_items.clicked.connect(self.remove_items)

        self.button_save_stock.clicked.connect(self.save_stock)

        """self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.stock_model)
        self.mapper.addMapping(self.spin_quantity, 1)
        self.mapper.addMapping(self.combo_unit, 2, b"currentIndex")
        self.mapper.addMapping(self.spin_cost, 3)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)

        self.mapper.toFirst()"""

        self.items_list.clicked.connect(self.update_item_properties_index)

        # Cycle through layouts
        for widget_num in range(self.general_tab.layout().count()):
            widget = self.general_tab.layout().itemAt(widget_num)
            if (type(widget) == QHBoxLayout) or (type(widget) == QVBoxLayout):
                for w_num in range(widget.count()):
                    w = widget.itemAt(w_num).widget()
                    if type(w) == QLineEdit:
                        # Use textEdited instead of textChanged!
                        w.textEdited.connect(self.update_item_properties_widget)
                    elif type(w) == QTextEdit:
                        w.textChanged.connect(self.update_item_properties_widget)
                    elif type(w) == QComboBox:
                        w.activated.connect(self.update_item_properties_widget)
                    elif type(w) == QSpinBox:
                        w.editingFinished.connect(self.update_item_properties_widget)
                    elif type(w) == QDoubleSpinBox:
                        w.editingFinished.connect(self.update_item_properties_widget)
                    else:
                        pass

    def save_stock_settings(self, item_index):
        """ Save an item's settings

            :param item_index: The index of the item to save the settings to """

        row = item_index.row()
        try:
            settings = self.stock_model.stock[row]
            settings["Quantity"] = self.spin_quantity.value()
            self.stock_model.dataChanged.emit(item_index, item_index)
        except:
            pass

    def update_stock_display(self, item_index):
        """ Update an item's display

            :param item_index: The index of the item to update the display to """

        row = item_index.row()

        try:
            settings = self.stock_model.stock[row]
            self.spin_quantity.setValue(settings["Quantity"])
        except:
            pass

    def update_item_properties(self, current_index=None, previous_index=None):
        # Save the last item first, then update the display
        if previous_index:
            # Save the stock settings
            self.save_stock_settings(previous_index)

        if current_index:
            # Update the display
            self.update_stock_display(current_index)

    @pyqtSlot()
    def add_stock(self):
        add_items_dialog = AddItemsDialog(parent=self, type_=AddItemsDialogType.Stock)
        add_items_dialog.exec()

        new_stock_index = self.stock_model.index(-1)
        self.items_list.setCurrentIndex(new_stock_index)

        self.update_item_properties_index(new_stock_index)

    @pyqtSlot(QModelIndex)
    def update_item_properties_index(self, current_index: QModelIndex):
        """ Upates item properties based on a QModelIndex

            :param current_index: The current index of a QListView's model
            :type current_index: QModelIndex

        """

        # Don't use the previous index (creates a bug)
        self.update_item_properties(current_index=current_index)

        self.previous_index = current_index

    @pyqtSlot()
    def update_item_properties_widget(self):
        current_index = self.items_list.currentIndex()
        self.update_item_properties(previous_index=current_index)

    @pyqtSlot()
    def remove_items(self):
        indexes = self.items_list.selectedIndexes()

        if indexes:
            first_index = True
            for index in indexes[::-1]:
                # Remove the item and refresh
                if first_index:
                    del self.stock_model.stock[index.row()]
                    first_index = False
                else:
                    del self.stock_model.stock[index.row() - 1]

            self.stock_model.update()

            # Clear the selection (as it is no longer valid)
            self.items_list.clearSelection()

            self.previous_index = None
            current_index = self.items_list.currentIndex()
            self.update_item_properties_index(current_index=current_index)

    @pyqtSlot()
    def save_stock(self):
        items = []
        for item_index in range(self.stock_model.rowCount()):
            name = self.stock_model.stock[item_index]["Name"]
            quantity = self.stock_model.stock[item_index]["Quantity"]

            items.append((name, quantity))

        remove_stock(items)

        # Clear the items list
        self.stock_model.stock.clear()
        self.stock_model.update()
        # TODO: Update the data display when items are removed


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    removestock = RemoveStock()
    removestock.show()
    sys.exit(app.exec())
