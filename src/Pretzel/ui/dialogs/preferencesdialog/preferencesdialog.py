#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  preferencesdialog.py
#
#  Copyright 2021 iwoithe <iwoithe@just42.net>
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
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

from Pretzel.ui import utils


class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.app = QApplication.instance()

        self.parent = parent

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pretzel/ui/dialogs/preferencesdialog/preferencesdialog.ui", self)

        # Interface
        # TODO: Add an option using QStyleFactory.keys()
        self.load_available_styles()
        # Paths
        # Database path
        self.get_database_path()

        self.bind_signals()

    def bind_signals(self):
        # Paths
        # Database path
        self.database_path_button.clicked.connect(self.open_database_path)
        # The button box
        self.button_box.accepted.connect(self.save_settings)
        self.button_box.clicked.connect(self.check_dialog_button)
        self.button_box.rejected.connect(self.reject)

    def load_available_styles(self):
        styles = utils.load_styles_list_from_directory()
        self.style_combo.addItems(styles)
        self.style_combo.setCurrentText(self.parent.settings.get("Style"))

    def get_database_path(self):
        self.database_path_edit.setText(self.parent.settings.get("Database Path"))

    @pyqtSlot()
    def open_database_path(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,
                                           "Open Database File",
                                           "",
                                           "All Files (*);;Database File (*.db *.DB *.database *.DATABASE)",
                                           options=options)
        if file:
            self.database_path_edit.setText(file)

    def save_settings(self):
        # Interface
        # Update the styles
        current_style = self.style_combo.currentText().replace(" ", "_")
        self.parent.settings.set("Style", current_style)

        # Paths
        self.parent.settings.set("Database Path", self.database_path_edit.text())

        # Save the changes
        self.parent.settings.save()
        self.close()

    def apply_settings(self):
        # Apply the style
        new_style_name = self.style_combo.currentText().replace(" ", "_")
        new_style = utils.load_style_from_file(os.path.join("data/styles/", new_style_name + ".qss"))
        utils.apply_style(new_style)

        # Paths
        # TODO: Reload the view table when the settings are applied

    @pyqtSlot(QAbstractButton)
    def check_dialog_button(self, button: QAbstractButton):
        if button.text().title() == "Apply":
            self.apply_settings()
