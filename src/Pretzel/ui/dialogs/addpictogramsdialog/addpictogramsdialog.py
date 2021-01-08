#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
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


import sys
import glob

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Pretzel.core.models import PictogramModel

class AddPictogramsDialog(QDialog):
    def __init__(self, *args, parent=None, **kwargs):
        self.parent = parent

        if self.parent:
            super().__init__(self.parent, *args, **kwargs)
        else:
            super().__init__(*args, **kwargs)

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pretzel/ui/dialogs/addpictogramsdialog/addpictogramsdialog.ui", self)

        self.pictograms_model = PictogramModel()
        self.pictograms_list.setModel(self.pictograms_model)

        self.load_pictograms()

        self.bind_signals()

    def bind_signals(self):
        self.button_add_pictograms.clicked.connect(self.add_pictograms)

    def load_pictograms(self):
        pictogram_paths = ["data/pictograms/*.*"]
        for path in pictogram_paths:
            for pictogram in glob.glob(path, recursive=True):
                try:
                    self.pictograms_model.pictograms.append(pictogram)
                except:
                    print("Please put only image files into the pictogram directory")

        self.pictograms_model.update()

    @pyqtSlot()
    def add_pictograms(self):
        for pictogram_index in self.pictograms_list.selectedIndexes():
            # Temporary fix
            try:
                current_item_index = self.parent.item_list.currentIndex()
            except AttributeError:
                try:
                    current_item_index = self.parent.items_list.currentIndex()
                except AttributeError:
                    current_item_index = self.parent.pictograms_list.currentIndex()

            # Temporary fix
            try:
                item = self.parent.item_model.items[current_item_index.row()]
            except AttributeError:
                try:
                    item = self.parent.items_model.items[current_item_index.row()]
                except AttributeError:
                    item = self.parent.pictograms_model.pictograms[current_item_index.row()]

            pictograms = item["Pictograms"]
            pictograms.pictograms.append(self.pictograms_model.pictograms[pictogram_index.row()])

        try:
            self.parent.pictograms_list.model().update()
        except AttributeError:
            self.parent.add_items_properties.pictograms_list.model().update()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    apd = AddPictogramsDialog()
    apd.show()
    sys.exit(apd.exec())