#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  generatereports.py
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
import time

from PyQt5 import uic

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ...dialogs import *


class SDSPropertiesWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pretzel/ui/reports/generatereports/properties/sdspropertieswidget.ui", self)

        # Setup the date edit
        date = time.strftime("%Y %m %d")
        year = int(date.split(" ")[0])
        month = int(date.split(" ")[1])
        day = int(date.split(" ")[2])
        self.date_edit.setDate(QDate(year, month, day))


class LabelPropertiesWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pretzel/ui/reports/generatereports/properties/labelpropertieswidget.ui", self)


class SummaryPropertiesWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pretzel/ui/reports/generatereports/properties/summarypropertieswidget.ui", self)


class GenerateReports(QDockWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('Pretzel/ui/reports/generatereports/generatereports.ui', self)

        # Setup the report type and report properties
        self.combo_report_type.addItems(["SDS", "Label", "Summary"])

        # Report properties
        self.report_properties = QStackedLayout(self.report_properties_container)

        sds_properties_widget = SDSPropertiesWidget()
        label_properties_widget = LabelPropertiesWidget()
        summary_properties_widget = SummaryPropertiesWidget()

        self.report_properties.addWidget(sds_properties_widget)
        self.report_properties.addWidget(label_properties_widget)
        self.report_properties.addWidget(summary_properties_widget)

        self.combo_report_type.currentIndexChanged.connect(self.update_report_properties)

        # Open folder
        self.button_open_folder.clicked.connect(self.open_folder)

        # Signals
        self.button_add_items.clicked.connect(self.add_items)

    @pyqtSlot()
    def open_folder(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self.parent, "Open Folder", "C:/", options=options)

        if folder:
            self.entry_folder_path.setText(folder)

    @pyqtSlot()
    def add_items(self):
        add_items_dialog = AddItemsDialog(self.parent)
        add_items_dialog.exec()

    def remove_items(self):
        sender = self.sender()
        if sender:
            if sender.objectName() == "button_remove_items":
                selected_items = self.items_view.selectedItems()
            else:
                selected_items = []

            for item in selected_items:
                self.plots_view.takeItem(self.plots_view.row(item))

    @pyqtSlot()
    def update_report_properties(self):
        self.report_properties.setCurrentIndex(self.combo_report_type.currentIndex())
