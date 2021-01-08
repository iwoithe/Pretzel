#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  molecular_mass_calculator.py
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

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from molmass import Formula
from molmass.molmass import FormulaError


class MolecularMass(QDockWidget):
    def __init__(self, *args, **kwargs):
        super().__init__("Molecular Mass Calculator", *args, **kwargs)

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pretzel/ui/tools/calculators/molecular_mass_calculator/molecular_mass_calculator.ui", self)

        types = ["Average", "Nominal", "Monoisotopic"]

        self.combo_type.addItems(types)

        self.bind_signals()

    def bind_signals(self):
        self.button_calculate.clicked.connect(self.calculate_molecular_mass)

    @pyqtSlot()
    def calculate_molecular_mass(self):
        chem_formula = self.entry_chem_formula.text()
        try:
            f = Formula(chem_formula)
        except FormulaError as e:
            print(e)
            return

        type = self.combo_type.currentText()
        if type == "Average":
            result = f.mass
        elif type == "Nominal":
            result = f.isotope.massnumber
        elif type == "Monoisotopic":
            result = f.isotope.mass
        else:
            pass

        self.result_display.setText(str(result))

def register(parent=None):
    """ This is a function which Pretzel looks for when installing add-ons """
    if parent:
        parent.molecular_mass = MolecularMass()
        parent.molecular_mass.toggleViewAction().setShortcuts(QKeySequence("Shift+M"))

        plugins_menu = parent.menu_bar.addMenu("&Plugins")
        plugins_menu.addAction(parent.molecular_mass.toggleViewAction())

        parent.addDockWidget(Qt.BottomDockWidgetArea, parent.molecular_mass)

def unregister(parent=None):
    """ This is a function which Pretzel looks for when uninstalling add-ons """
    if parent:
        parent.removeDockWidget(parent.molecular_mass)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Temporarily set the style, until I've written my own styles
    app.setStyle("fusion")
    molecular_mass = MolecularMass()
    molecular_mass.show()
    sys.exit(app.exec_())
