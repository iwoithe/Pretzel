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

# TODO: Work out why this crashes Pretzel
# import matplotlib
# matplotlib.use("Qt5Agg")

from PyQt5.QtCore import *
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Pretzel
# import Pretzel.core
from Pretzel.app import PretzelWindow

try:
    # For Windows
    from PyQt5.QtWinExtras import QtWin
    pretzel_id = 'iwoithe.pretzel.app.0.0.1'
    QtWin.setCurrentProcessExplicitAppUserModelID(pretzel_id)
except ImportError:
    pass


if __name__ == '__main__':
    # TODO: Store the path to the database file in the settings
    # TODO: when using uic.loadUi(), see if using relative paths will work (e.g. "./test.ui" instead of "Pretzel/ui/test/test.ui etc.")
    # Setup the application
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    # TODO: Start switching the UI over to QML
    # TODO: As QML doesn't support QSS style sheets, find a different way of styling
    engine = QQmlApplicationEngine()

    # Show the splash screen
    splash_img = QPixmap("data/pretzel/logo.svg")
    splash_screen = QSplashScreen(splash_img)
    splash_screen.show()

    # Init logs
    splash_screen.showMessage("Initializing Logging...", alignment=Qt.AlignRight | Qt.AlignBottom)
    app.processEvents()
    Pretzel.core.init.init_logging()
    # Time?
    # logging.basicConfig(filename='data/debug.log', level=logging.INFO, format='%(levelname)s:%(asctime)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.basicConfig(filename='data/debug.log', level=logging.INFO, format='%(levelname)s:%(name)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.debug("Initialized logging")

    # Init databases
    splash_screen.showMessage("Initializing Databases...", alignment=Qt.AlignRight | Qt.AlignBottom)
    app.processEvents()
    Pretzel.core.database.init.initialize_databases()
    logging.debug("Initialized the databases")

    # Loading
    splash_screen.showMessage("Loading...", alignment=Qt.AlignRight | Qt.AlignBottom)
    app.processEvents()

    # Run Pretzel
    pretzel = PretzelWindow()

    pretzel.show()
    splash_screen.finish(pretzel)
    logging.info("Pretzel loaded successfully")
    sys.exit(app.exec())

