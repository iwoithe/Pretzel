#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  removeitemsdialog.py
#
#  Copyright 2020 iwoithe <iwoithe@just42.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License.
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
import logging

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Pretzel.constants import *
from Pretzel.core.models.items import ItemsModel
from Pretzel.core.models.stock import StockModel
from Pretzel.core.database.items import load_items
from Pretzel.core.database.stock import load_stock_names, load_stock


class AddItemsDialog(QDialog):
    def __init__(self, parent=None, type_=AddItemsDialogType.Item, stock_type_=StockType.Default, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.type_ = type_
        self.stock_type_ = stock_type_
        self.load_database_items()
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('Pretzel/ui/dialogs/additemsdialog/additemsdialog.ui', self)

        # Setup the items list
        self.items_list.setModel(self.proxy_model)

        self.bind_signals()

    def bind_signals(self):
        self.button_add_items.clicked.connect(self.add_items)

        self.filter_entry.textEdited.connect(self.filter_items)

    def load_database_items(self):
        if self.type_ == AddItemsDialogType.Item:
            items = load_items()
            self.items_model = ItemsModel(items=items)
        elif self.type_ == AddItemsDialogType.Stock:
            if self.stock_type_ == StockType.Default:
                stock = load_stock_names()
            elif self.stock_type_ == StockType.Edit:
                stock = load_stock()
            else:
                stock = []

            self.items_model = StockModel(stock=stock)

        else:
            logging.warning("The supplied add items type does not exist")

        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.items_model)
        self.proxy_model.setFilterKeyColumn(0)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

    @pyqtSlot()
    def add_items(self):
        if self.parent:
            for item_index in self.items_list.selectedIndexes():
                #current_item_index = self.parent.items_list.currentIndex()
                if self.type_ == AddItemsDialogType.Item:
                    # Temporary fix
                    try:
                        self.parent.item_model.items.append(self.items_model.items[item_index.row()])
                    except AttributeError:
                        self.parent.items_model.items.append(self.items_model.items[item_index.row()])
                elif self.type_ == AddItemsDialogType.Stock:
                    self.parent.stock_model.stock.append(self.items_model.stock[item_index.row()])
                else:
                    logging.warning("The supplied add items type does not exist")
                    return

                #item = self.parent.stock_model.stock[current_item_index.row()]
                #pictograms = item["Pictograms"]
                #pictograms.pictograms.append(self.items_model.items[item_index.row()])
                if self.type_ == AddItemsDialogType.Item:
                    # Temporary fix
                    try:
                        self.parent.item_model.update()
                    except AttributeError:
                        self.parent.items_model.update()
                elif self.type_ == AddItemsDialogType.Stock:
                    self.parent.stock_model.update()
                else:
                    logging.warning("The supplied add items type does not exist")
                    return

            self.close()

    @pyqtSlot(str)
    def filter_items(self, text: str):
        # Filter the packages
        self.proxy_model.setFilterFixedString(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    add_items_dialog = AddItemsDialog()
    add_items_dialog.show()
    sys.exit(app.exec())
