#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  addremoveitemswidget.py
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


class AddRemoveItemsWidget(QWidget):

    add_items_button_clicked = pyqtSignal()

    def __init__(self, parent=None, title="Items", suffix=":", *args, **kwargs):
        if parent is not None:
            super().__init__(parent, *args, **kwargs)
        else:
            super().__init__(*args, **kwargs)

        self.title = title
        self.suffix = suffix

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('ui/widgets/addremoveitemswidget/addremoveitemswidget.ui', self)

        self.label_items.setText(self.title + self.suffix)

        self.bind_signals()

    def bind_signals(self):
        self.button_add_items.clicked.connect(self.add_items_button_clicked.emit)
        self.button_remove_items.clicked.connect(self.remove_items)

    @pyqtSlot()
    def remove_items(self):
        selected_items = self.items_view.selectedItems()

        for item in selected_items:
            self.items_view.takeItem(self.items_view.row(item))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    addremoveitemswidget = AddRemoveItemsWidget()
    addremoveitemswidget.show()
    sys.exit(app.exec())
