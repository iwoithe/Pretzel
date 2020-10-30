#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  scientific_calculator.py
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

from PyQt5 import uic

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from sympy import init_printing, sympify, latex

try:
    import utils
except ModuleNotFoundError:
    from . import utils


class ScientificCalculator(QDockWidget):

    equation = ""

    def __init__(self, *args, **kwargs):
        super().__init__("Scientific Calculator", *args, **kwargs)

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pretzel/ui/tools/calculators/scientific_calculator/scientific_calculator.ui", self)
        self.bind_signals()

    def bind_signals(self):
        # Equation Display
        self.equation_display.textEdited.connect(self.set_equation)
        self.equation_display.textChanged.connect(self.calculate_result)

        # Buttons
        for button_num in range(self.keypad.count()):
            button = self.keypad.itemAt(button_num).widget()
            button.clicked.connect(self.add_to_equation)

    @pyqtSlot(str)
    def set_equation(self, text):
        self.equation = text

    def add_to_equation(self):
        button = self.sender()
        if button:
            text = button.text()
            if text == "C":
                self.equation = ""
            elif text == "->":
                self.equation = self.equation[:1]
            elif text == "<-":
                self.equation = self.equation[:-1]
            elif text == "^":
                self.equation += "**"
            elif text in ["sin", "cos", "tan", "sqrt"]:
                self.equation += button.text() + "("
            elif text == "Solve":
                self.equation += "solve("
            elif text == "Factorise":
                self.equation += "factor("
            elif text == "Expand":
                self.equation += "expand("
            elif text == "Plot":
                self.equation += "plot("
            else:
                self.equation += button.text()

        self.update_equation_display()

    def update_equation_display(self):
        self.equation_display.setText(self.equation)

    def calculate_result(self):
        result = ""
        #init_printing(pretty_print=True, use_unicode=True)
        init_printing()
        try:
            # Todo: Don't auto-calculate plots
            expr = sympify(self.equation)
            tex_string = latex(expr)
            tex_string = r'$' + tex_string + '$'
            pixmap = utils.mathTex_to_QPixmap(tex_string, 14)
            self.result.setPixmap(pixmap)
        except Exception as e:
            # For debugging
            #result = "Error: " + str(e)
            # Otherwise use live preview (like Caligator)
            result = ""

            self.result.setPixmap(QPixmap())
            self.result.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Temporarily set the style, until I've written my own styles
    app.setStyle("fusion")
    sc = ScientificCalculator()
    sc.show()
    sys.exit(app.exec_())
