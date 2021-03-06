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
import logging

# FIXME: Pretzel crashes when the plotting window comes up (from the scientific calculator)
# FIXME: This crashes when run from PyCharm. I think it's related to above
# import matplotlib
# try:
#     matplotlib.use("Qt5Agg")
# except:
#     matplotlib.use("TkAgg")

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Pretzel
from Pretzel.app import PretzelWindow

try:
    # For Windows
    from PyQt5.QtWinExtras import QtWin
    pretzel_id = 'iwoithe.pretzel.app.0.0.1'
    QtWin.setCurrentProcessExplicitAppUserModelID(pretzel_id)
except ImportError:
    pass


if __name__ == '__main__':
    # TODO: Customise properties so users can add/remove columns of data (properties)
    # TODO: when using uic.loadUi(), see if using relative paths will work (e.g. "./test.ui" instead of "Pretzel/ui/test/test.ui etc.")
    # Setup the application
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    # Show the splash screen
    splash_img = QPixmap("data/pretzel/logo.svg")
    splash_screen = QSplashScreen(splash_img)
    splash_screen.show()

    # Init directories
    splash_screen.showMessage("Initializing Directories...", alignment=Qt.AlignRight | Qt.AlignBottom)
    app.processEvents()
    Pretzel.core.init.init_dirs()

    # Init files
    splash_screen.showMessage("Initializing Files...", alignment=Qt.AlignRight | Qt.AlignBottom)
    app.processEvents()
    Pretzel.core.init.init_files()
    # Time?
    logging.basicConfig(filename=Pretzel.core.paths.log_file, level=logging.INFO, format='%(levelname)s:%(name)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.debug("Initialized files")

    # Loading
    splash_screen.showMessage("Loading...", alignment=Qt.AlignRight | Qt.AlignBottom)
    app.processEvents()

    # Run Pretzel
    pretzel = PretzelWindow()

    pretzel.show()
    splash_screen.finish(pretzel)
    logging.info("Pretzel loaded successfully")
    sys.exit(app.exec())

