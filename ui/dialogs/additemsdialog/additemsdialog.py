#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  additemsdialog.py
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

from PyQt5 import uic

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class AddItemsDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('ui/dialogs/additemsdialog/additemsdialog.ui', self)

    def add_database_items(self):
        for database_item in self.items_database_view.selectedItems():
            item = QListWidgetItem(database_item.text(), self.added_items_view)

    def remove_items(self):
        sender = self.sender()
        if sender:
            if sender.objectName() == "button_remove_items_database":
                selected_items = self.added_items_view.selectedItems()
            else:
                selected_items = []

            for item in selected_items:
                self.added_items_view.takeItem(self.added_items_view.row(item))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    add_items_dialog = AddItemsDialog()
    add_items_dialog.show()
    sys.exit(app.exec())
