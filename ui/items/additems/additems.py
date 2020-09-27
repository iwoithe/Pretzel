#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  additems.py
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


class GeneralTab(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('ui/items/additems/tabs/generaltab.ui', self)
        self.bind_signals()

    def bind_signals(self):
        pass


class AddItemsProperties(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.general_tab = GeneralTab()

        properties = QTabWidget()
        properties.addTab(self.general_tab, "General")

        main_layout = QVBoxLayout()

        main_layout.addWidget(properties)

        self.setLayout(main_layout)

        self.bind_signals()

    def bind_signals(self):
        pass


class AddItems(QDockWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('ui/items/additems/additems.ui', self)

        self.add_items_properties = AddItemsProperties()

        self.combo_add_items_type.addItems(["Add Items", "Import from Database"])

        self.items_properties = QStackedLayout(self.add_items_type_widget)
        self.items_properties.addWidget(self.add_items_properties)

        self.bind_signals()

    def bind_signals(self):
        self.button_add_items.clicked.connect(self.add_items)
        self.button_remove_items.clicked.connect(self.remove_items)

        self.combo_add_items_type.currentIndexChanged.connect(self.update_properties_view)

        self.items_view.currentItemChanged.connect(self.update_item_properties)

        # Cycle through a layouts line edits
        for widget_num in range(self.add_items_properties.general_tab.layout().count()):
            widget = self.add_items_properties.general_tab.layout().itemAt(widget_num)
            if type(widget) == QHBoxLayout:
                for w_num in range(widget.count()):
                    w = widget.itemAt(w_num).widget()
                    if type(w) == QLineEdit:
                        # Use textEdited instead of textChanged!
                        w.textEdited.connect(self.update_item_properties_lineedit)

    def save_item_settings(self, item):
        """ Save an item's settings
            :item: The QListWidgetItem to save the settings to """
        item.settings["Name"] = self.add_items_properties.general_tab.entry_name.text()
        item.settings["Chemical Formula"] = self.add_items_properties.general_tab.entry_chem_formula.text()

    def update_item_display(self, item):
        """ Update an item's display
            :item: The QListWidgetItem to update the display to """
        item.setText(item.settings["Name"])
        self.add_items_properties.general_tab.entry_name.setText(item.settings["Name"])
        self.add_items_properties.general_tab.entry_chem_formula.setText(item.settings["Chemical Formula"])

    @pyqtSlot()
    def update_properties_view(self):
        self.items_properties.setCurrentIndex(self.combo_add_items_type.currentIndex())

    @pyqtSlot()
    def add_items(self):
        item = QListWidgetItem("New Item", self.items_view)
        item.settings = {"Name": item.text(),
                         "Chemical Formula": ""}

        self.items_view.setCurrentItem(item)

        self.update_item_properties(current_item=item)

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def update_item_properties(self, current_item=None, previous_item=None):
        # Save the last item first, then update the display
        if previous_item:
            # Save the item settings
            self.save_item_settings(previous_item)

        if current_item:
            # Update the display
            self.update_item_display(current_item)

    @pyqtSlot()
    def update_item_properties_lineedit(self):
        current_item = self.items_view.currentItem()
        self.update_item_properties(current_item=current_item, previous_item=current_item)

    @pyqtSlot()
    def remove_items(self):
        selected_items = self.items_view.selectedItems()

        for item in selected_items:
            self.items_view.takeItem(self.items_view.row(item))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    add_items = AddItems()
    add_items.show()
    sys.exit(app.exec())
