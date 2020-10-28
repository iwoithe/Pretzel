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

from ui.dialogs import AddPictogramsDialog
from core.models.items import ItemsModel, PictogramModel
import core.database
import core.converter

class AddItemsProperties(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.items_model = ItemsModel()

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("ui/items/additems/additemsproperties.ui", self)

        self.items_list.setModel(self.items_model)
        self.previous_index = None

        # Setup the warning label combobox
        self.warning_labels = ["None", "Warning", "Danger"]
        self.combo_warning_label.addItems(self.warning_labels)
        self.combo_warning_label.setCurrentIndex(0)

        # Setup the danger level combobox
        self.danger_levels = ["None", "Low", "Moderate", "High", "Extreme"]
        self.combo_danger_level.addItems(self.danger_levels)
        self.combo_danger_level.setCurrentIndex(0)

        self.bind_signals()

    def bind_signals(self):
        self.button_add_items.clicked.connect(self.add_item)
        self.button_remove_items.clicked.connect(self.remove_items)

        self.items_list.clicked.connect(self.update_item_properties_index)

        # Cycle through a layouts line edits
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
                    else:
                        pass

        self.button_add_pictograms.clicked.connect(self.add_pictograms)
        self.button_remove_pictograms.clicked.connect(self.remove_pictograms)

    def save_item_settings(self, item_index):
        """ Save an item's settings
            :item_index: The index of the item to save the settings to """

        row = item_index.row()
        try:
            settings = self.items_model.items[row]
            settings["Name"] = self.entry_name.text()
            settings["Chemical Formula"] = self.entry_chem_formula.text()
            settings["Warning Label"] = self.warning_labels[self.combo_warning_label.currentIndex()]
            settings["Danger Level"] = self.danger_levels[self.combo_danger_level.currentIndex()]
            settings["Notes"] = self.notes_text.toMarkdown()
            self.items_model.dataChanged.emit(item_index, item_index)
        except:
            pass

    def update_item_display(self, item_index):
        """ Update an item's display
            :item_index: The index of the item to update the display to """
        # TODO: Get live preview of markdown working

        row = item_index.row()
        try:
            settings = self.items_model.items[row]
            self.entry_name.setText(settings["Name"])
            self.entry_chem_formula.setText(settings["Chemical Formula"])
            self.combo_warning_label.setCurrentIndex(self.warning_labels.index(settings["Warning Label"]))
            self.combo_danger_level.setCurrentIndex(self.danger_levels.index(settings["Danger Level"]))
            self.notes_text.setMarkdown(settings["Notes"])
            self.pictograms_list.setModel(settings["Pictograms"])
        except:
            pass

    def update_item_properties(self, current_index=None, previous_index=None):
        # Save the last item first, then update the display
        if previous_index:
            # Save the item settings
            self.save_item_settings(previous_index)

        if current_index:
            # Update the display
            self.update_item_display(current_index)

    @pyqtSlot()
    def add_item(self):
        self.items_model.items.append({"Name": "New Item",
                                       "Chemical Formula": "",
                                       "Warning Label": "None",
                                       "Danger Level": "None",
                                       "Notes": "",
                                       "Pictograms": PictogramModel()})

        self.items_model.update()
        self.pictograms_list.setModel(self.items_model.items[-1]["Pictograms"])

        self.entry_name.setText(self.items_model.items[-1]["Name"])

        new_item_index = self.items_model.index(-1)
        self.items_list.setCurrentIndex(new_item_index)

        self.update_item_properties_index(new_item_index)

    @pyqtSlot(QModelIndex)
    def update_item_properties_index(self, current_index: QModelIndex):
        """ Upates item properties based on a QModelIndex

            :param current_index: The current index of a QListView's model
            :type current_index: QModelIndex

        """

        # Don't use self.previous_index (creates a bug)
        self.update_item_properties(current_index=current_index)

        self.previous_index = current_index

    @pyqtSlot()
    def update_item_properties_widget(self):
        current_index = self.items_list.currentIndex()
        # For some reason, self.notes_text does not like the current_index parameter
        self.update_item_properties(previous_index=current_index)

    @pyqtSlot()
    def remove_items(self):
        indexes = self.items_list.selectedIndexes()

        if indexes:
            first_index = True
            for index in indexes[::-1]:
                # Remove the item and refresh
                if first_index:
                    del self.items_model.items[index.row()]
                    first_index = False
                else:
                    del self.items_model.items[index.row() - 1]

            self.items_model.update()

            # Clear the selection (as it is no longer valid)
            self.items_list.clearSelection()

            self.previous_index = None
            current_index = self.items_list.currentIndex()
            self.update_item_properties_index(current_index=current_index)

    @pyqtSlot()
    def add_pictograms(self):
        # shorten add_pictograms_dialg to apd
        apd = AddPictogramsDialog(parent=self.parent)
        apd.exec()

    @pyqtSlot()
    def remove_pictograms(self):
        indexes = self.pictograms_list.selectedIndexes()

        if indexes:
            first_index = True
            for index in indexes[::-1]:
                # Remove the item and refresh
                item = self.items_model.items[self.items_list.currentIndex().row()]
                if first_index:
                    item["Pictograms"].pictograms.pop(index.row())
                    first_index = False
                else:
                    item["Pictograms"].pictograms.pop(index.row() - 1)

            item["Pictograms"].update()

            # Clear the selection (as it is no longer valid)
            self.items_list.clearSelection()

            self.previous_index = None
            current_index = self.items_list.currentIndex()
            self.update_item_properties_index(current_index=current_index)


class ImportItemsProperties(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if parent:
            self.parent = parent

        # Setup the interface
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("ui/items/additems/importitemsproperties.ui", self)

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

        self.add_items_properties = AddItemsProperties(parent=self)
        self.import_items_properties = ImportItemsProperties()

        self.combo_items_type.addItems(["Add Items", "Import from Database"])

        self.items_type_layout = QStackedLayout(self.items_widget)
        self.items_type_layout.addWidget(self.add_items_properties)
        self.items_type_layout.addWidget(self.import_items_properties)

        self.bind_signals()

    def bind_signals(self):
        self.combo_items_type.currentIndexChanged.connect(self.update_properties_view)

        self.button_save_items.clicked.connect(self.save_items)

    @pyqtSlot()
    def update_properties_view(self):
        current_index = self.combo_items_type.currentIndex()
        self.items_type_layout.setCurrentIndex(current_index)

    @pyqtSlot()
    def save_items(self):
        """ Save the items to the item's database """
        items = []
        items_model = self.add_items_properties.items_list.model()
        for item_index in range(items_model.rowCount()):
            name = items_model.items[item_index]["Name"]
            chem_formula = items_model.items[item_index]["Chemical Formula"]
            warning_label = items_model.items[item_index]["Warning Label"]
            danger_level = items_model.items[item_index]["Danger Level"]
            notes = items_model.items[item_index]["Notes"]
            pictos = items_model.items[item_index]["Pictograms"].pictograms
            pictograms = []
            for picto in pictos:
                # Append the pictograms image path
                pictograms.append(picto)

            pictograms = core.converter.list_to_string(pictograms)

            items.append((name, chem_formula, warning_label, danger_level, notes, pictograms))

        core.database.items.add_items(items)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    add_items = AddItems()
    add_items.show()
    sys.exit(app.exec())
