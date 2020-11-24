#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  menu.py
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

# TODO: Move utils functions to the utils.py file in the ui directory
try:
    import utils
except ModuleNotFoundError:
    from . import utils

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Menu(QDockWidget):

    toggleDock = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__("Menu", *args, **kwargs)

        self.setup_menu()
        self.setup_ui()

    def setup_menu(self):
        self.menu = {"Items": {
                        "Add Items",
                        "Remove Items",
                    },
                    "Stock": {
                        "Add Stock",
                        "Remove Stock"
                    },
                    "Reports": {
                        "Generate Reports",
                        "Update Reports"
                    },
                    "Tools": {
                        "Calculators": {
                            "Molecular Mass",
                            "Scientific Calculator"
                        }
                    }
        }

    def setup_ui(self):
        # Menu items
        self.menu_view = QTreeWidget()
        self.menu_view.setHeaderHidden(True)
        self.menu_view.setAlternatingRowColors(False)
        self.menu_view.setColumnCount(1)
        self.menu_view.setExpandsOnDoubleClick(True)

        utils.fill_widget(self.menu_view, self.menu)

        self.menu_view.itemClicked.connect(self.toggle_dock)

        # Main Layout
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.menu_view)

        widget.setLayout(layout)
        self.setWidget(widget)

    def toggle_dock(self, current_item):
        dock_item = self.sender()
        if dock_item:
            self.toggleDock.emit(current_item.text(0))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Temporarily set the style, until I've written my own styles
    app.setStyle("fusion")
    menu = Menu()
    menu.show()
    sys.exit(app.exec_())
