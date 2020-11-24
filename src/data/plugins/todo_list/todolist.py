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

import os

from PyQt5 import uic
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSlot
from PyQt5.QtGui import QKeySequence

from PyQt5.QtWidgets import *

from Pretzel.api import types


class TodoModel(QAbstractListModel):
    def __init__(self, *args, tasks=[], **kwargs):
        super().__init__(*args, **kwargs)

        self.tasks = tasks or None

    def data(self, index, role):
        if role == Qt.DisplayRole:
            data = self.tasks[index.row()]
            return data["Name"]
        else:
            pass

    def rowCount(self, parent=None):
        return len(self.tasks)

    def update(self):
        self.layoutChanged.emit()


class TodoListPlugin(QDockWidget, types.Plugin):
    name = "Todo List"
    version = (0, 0, 1)
    author = "iwoithe"
    description = "A simple todo list plugin"
    shortcuts = [QKeySequence("Ctrl+T")]
    README = "./README.md"

    file_path = __file__

    def __init__(self):
        super().__init__()

        self.setup()

    def setup(self):
        uic.loadUi("{}/todolist.ui".format(os.path.dirname(self.file_path)), self)

        # Setup the model
        self.todo_model = TodoModel()
        self.tasks_list.setModel(self.todo_model)

        self.bind_signals()

    def bind_signals(self):
        self.button_add_task.clicked.connect(self.add_task)

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
                    else:
                        pass

    def save_item_settings(self, task_index):
        """ Save an item's settings
            :item_index: The index of the item to save the settings to """

        row = task_index.row()
        try:
            settings = self.todo_model.tasks[row]
            settings["Name"] = self.entry_name.text()
            settings["Description"] = self.description_text.toMarkdown()
        except:
            pass

    def update_item_display(self, task_index):
        """ Update an item's display
            :item_index: The index of the item to update the display to """
        # TODO: Get live preview of markdown working

        row = task_index.row()
        try:
            settings = self.todo_model.tasks[row]
            self.entry_name.setText(settings["Name"])
            self.description_text.setMarkdown(settings["Description"])
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
    def add_task(self):
        self.todo_model.tasks.append({
            "Name": "New task",
            "Description": ""})

        self.todo_model.update()
        self.entry_name.setText(self.todo_model.tasks[-1]["Name"])
        self.description_text.setMarkdown(self.todo_model.tasks[-1]["Description"])

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
