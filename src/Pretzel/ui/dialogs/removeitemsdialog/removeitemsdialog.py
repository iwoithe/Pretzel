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

from PyQt5 import uic

from PyQt5.QtWidgets import *

from Pretzel.core.models import ItemsModel
from Pretzel.core.database.items import load_items


class RemoveItemsDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('Pretzel/ui/dialogs/removeitemsdialog/removeitemsdialog.ui', self)

        self.load_database_items()

        self.bind_signals()

    def bind_signals(self):
        self.button_remove_items.clicked.connect(self.add_items)

    def load_database_items(self):
        items = load_items()
        self.items_model = ItemsModel(items=items)
        self.items_list.setModel(self.items_model)

    def add_items(self):
        for item_index in self.items_list.selectedIndexes():
            self.parent.items_list.model().items.append(self.items_model.items[item_index.row()])

        self.parent.items_list.model().update()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    add_items_dialog = RemoveItemsDialog()
    add_items_dialog.show()
    sys.exit(app.exec())
