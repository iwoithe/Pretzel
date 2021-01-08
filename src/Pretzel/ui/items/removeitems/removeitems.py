#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  removeitems.py
#
#  Copyright 2021 iwoithe <iwoithe@just42.net>
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

from PyQt5 import uic

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Pretzel.ui.dialogs import AddItemsDialog

from Pretzel.core.models import ItemsModel
from Pretzel.core.database.items import remove_items


class RemoveItems(QDockWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('Pretzel/ui/items/removeitems/removeitems.ui', self)

        self.items_model = ItemsModel()
        self.items_list.setModel(self.items_model)

        self.bind_signals()

    def bind_signals(self):
        self.button_add_items.clicked.connect(self.add_items)
        self.button_remove_items.clicked.connect(self.remove_items)

        self.remove_items_button.clicked.connect(self.delete_items)

    @pyqtSlot()
    def add_items(self):
        """ Adds items to the items list """
        add_items_dialog = AddItemsDialog(self)
        add_items_dialog.exec()

    @pyqtSlot()
    def remove_items(self):
        """ Removes the selected items from the items list"""
        indexes = self.items_list.selectedIndexes()

        if indexes:
            first_index = True
            for index in indexes[::-1]:
                # TODO: See if the following is a shortcut way of removing items
                # self.items_model.removeRow(index)

                # Remove the item and refresh
                if first_index:
                    del self.items_model.items[index.row()]
                    first_index = False
                else:
                    del self.items_model.items[index.row() - 1]

            self.items_model.update()

            # Clear the selection (as it is no longer valid)
            self.items_list.clearSelection()

    @pyqtSlot()
    def delete_items(self):
        """ Deletes the items from the database"""

        items = []

        for item_index in range(self.items_model.rowCount()):
            name = self.items_model.items[item_index]["Name"]
            items.append((name))

        remove_items(items)

        self.items_model.items.clear()
        self.items_model.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    removeitems = RemoveItems()
    removeitems.show()
    sys.exit(app.exec())
