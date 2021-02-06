#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  aboutdialog.py
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


from PyQt5 import uic
from PyQt5.QtWidgets import *


class AboutDialog(QDialog):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(parent)

        self.parent = parent

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pretzel/ui/dialogs/aboutdialog/aboutdialog.ui", self)
        self.bind_signals()

        self.load_license()

    def bind_signals(self):
        self.button_box.clicked.connect(self.close)

    def load_license(self):
        license_file = "data/pretzel/LICENSE"
        with open(license_file) as f:
            license_text = f.read()

        self.license_text.setPlainText(license_text)
