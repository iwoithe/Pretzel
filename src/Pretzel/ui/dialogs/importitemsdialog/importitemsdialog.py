#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  importitemsdialog.py
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
from PyQt5.QtWidgets import *

from Pretzel.core.database.import_ import *


class ImportItemsDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = "None"

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pretzel/ui/dialogs/importitemsdialog/importitemsdialog.ui", self)

        self.bind_signals()

    def bind_signals(self):
        self.file_path_button.clicked.connect(self.set_file_path)
        self.import_button.clicked.connect(self.import_items)

    @pyqtSlot()
    def set_file_path(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file, type_ = QFileDialog.getOpenFileName(self,
                                                "Open File",
                                                "C:/",
                                                "Microsoft Excel (*.xlsx)",
                                                options=options)

        if file:
            # self.openFilesPath = files[0]
            self.file_path_entry.setText(file)
            if type_ == "Microsoft Excel (*.xlsx)":
                self.type = "Excel"
            elif type_ == "Open Document Spreadsheet (*.ods)":
                self.type = "ODS"
            elif type_ == "Comma Separated Values (*.csv)":
                self.type = "CSV"
            else:
                self.type = "None"

    @pyqtSlot()
    def import_items(self):
        file = self.file_path_entry.text()
        columns = {
                    "Name": self.name_spin.value(),
                    "Chemical Formula": self.chem_formula_spin.value(),
                    "Warning Label": self.warning_label_spin.value(),
                    "Danger Level": self.danger_level_spin.value(),
                    "Notes": self.notes_spin.value()}

        if self.type == "Excel":
            import_excel(file=file, columns_dict=columns)
        elif self.type == "ODS":
            # TODO: Add Open Document Spreadsheet file support
            pass
        elif self.type == "CSV":
            # TODO: Add CSV file support
            pass
        else:
            print("This file type is not supported")

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    import_items_dialog = ImportItemsDialog()
    import_items_dialog.show()
    sys.exit(app.exec())
