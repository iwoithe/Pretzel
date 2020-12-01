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
import sys
import glob
import json
import logging
import importlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


import Pretzel.core

import Pretzel.ui.utils

from Pretzel.ui.menu import *
from Pretzel.ui.items import *

from Pretzel.ui.stock import AddStock, RemoveStock, EditStock, ViewStock, StockToolbar
from Pretzel.ui.preferences import PreferencesDialog
from Pretzel.ui.tools.calculators import MolecularMass, ScientificCalculator


#logging.basicConfig(filename='data/debug.log', level=logging.DEBUG)

try:
    # For Windows
    from PyQt5.QtWinExtras import QtWin
    pretzel_id = 'iwoithe.pretzel.app.0.0.1'
    QtWin.setCurrentProcessExplicitAppUserModelID(pretzel_id)
except ImportError:
    pass


class PretzelWindow(QMainWindow):

    settings_file = "data/settings.json"
    with open(settings_file) as f:
        settings = json.loads(f.read())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_actions()
        self.setup_ui()

        self.load_plugins()

    def create_actions(self):
        # Quit
        self.action_quit = QAction("Quit", self)
        self.action_quit.setStatusTip("Quit the application")
        self.action_quit.setShortcuts(QKeySequence("Ctrl+Q"))
        self.action_quit.triggered.connect(self.quit)

        # Preferences
        self.action_preferences = QAction("Preferences", self)
        self.action_preferences.setStatusTip("Open the preferences")
        self.action_preferences.setShortcuts(QKeySequence("Ctrl+Shift+P"))
        self.action_preferences.triggered.connect(self.show_preferences)

        # About

        # About Qt
        self.action_about_qt = QAction("About Qt", self)
        self.action_about_qt.setStatusTip("About Qt")
        self.action_about_qt.triggered.connect(QApplication.instance().aboutQt)

    def create_menu_bar(self):
        self.menu_bar = QMenuBar()

        # File
        file_menu = self.menu_bar.addMenu("&File")
        file_menu.addAction(self.action_quit)

        # Edit
        edit_menu = self.menu_bar.addMenu("&Edit")
        edit_menu.addAction(self.action_preferences)

        # View
        view_menu = self.menu_bar.addMenu("&View")
        # Items
        item_menu = view_menu.addMenu("Item")
        item_menu.addAction(self.add_items.toggleViewAction())
        item_menu.addAction(self.remove_items.toggleViewAction())
        # Stock
        stock_menu = view_menu.addMenu("Stock")
        stock_menu.addAction(self.add_stock.toggleViewAction())
        stock_menu.addAction(self.remove_stock.toggleViewAction())
        stock_menu.addAction(self.edit_stock.toggleViewAction())
        stock_menu.addAction(self.view_stock.toggleViewAction())
        stock_menu.addAction(self.stock_toolbar.toggleViewAction())

        view_menu.addAction(self.menu.toggleViewAction())

        # Tools
        tools_menu = self.menu_bar.addMenu("&Tools")
        # Calculators
        calculators_menu = tools_menu.addMenu("Calculators")
        calculators_menu.addAction(self.scientific_calculator.toggleViewAction())
        calculators_menu.addAction(self.molecular_mass.toggleViewAction())
        # Generation
        generation_menu = tools_menu.addMenu("Generation")

        # Help
        help_menu = self.menu_bar.addMenu("&Help")
        help_menu.addAction(self.action_about_qt)

        return self.menu_bar

    def setup_ui(self):
        self.create_docks()
        self.create_toolbars()
        self.setup_window()

    def create_docks(self):
        # Create and setup the dock widgets
        self.menu = Menu()
        # Or QKeySequence(Qt.CTRL + Qt.Key_M)
        self.menu.toggleViewAction().setShortcuts(QKeySequence("Ctrl+M"))
        self.menu.toggleDock.connect(self.toggle_dock)

        # Items
        self.add_items = AddItems(self)
        self.add_items.toggleViewAction().setShortcuts(QKeySequence("Shift+A"))
        self.remove_items = RemoveItems(self)
        self.remove_items.toggleViewAction().setShortcuts(QKeySequence("Shift+R"))

        # Stock
        self.add_stock = AddStock(parent=self)
        self.add_stock.toggleViewAction().setShortcuts(QKeySequence("Ctrl+A"))
        self.remove_stock = RemoveStock(parent=self)
        self.remove_stock.toggleViewAction().setShortcuts(QKeySequence("Ctrl+R"))
        self.edit_stock = EditStock(parent=self)
        self.edit_stock.toggleViewAction().setShortcuts(QKeySequence("Ctrl+E"))
        self.view_stock = ViewStock(parent=self)
        self.view_stock.toggleViewAction().setShortcuts(QKeySequence("Shift+V"))

        self.scientific_calculator = ScientificCalculator()
        self.scientific_calculator.toggleViewAction().setShortcuts(QKeySequence("Alt+C"))

        self.molecular_mass = MolecularMass()
        self.molecular_mass.toggleViewAction().setShortcuts(QKeySequence("Shift+M"))

        # Add docks

        self.addDockWidget(Qt.LeftDockWidgetArea, self.menu)

        self.addDockWidget(Qt.RightDockWidgetArea, self.add_items)
        self.addDockWidget(Qt.RightDockWidgetArea, self.remove_items)

        self.addDockWidget(Qt.RightDockWidgetArea, self.add_stock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.remove_stock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.edit_stock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.view_stock)

        self.splitDockWidget(self.add_items, self.add_stock, Qt.Horizontal)
        self.splitDockWidget(self.add_items, self.remove_items, Qt.Vertical)
        self.splitDockWidget(self.add_stock, self.remove_stock, Qt.Vertical)

        self.splitDockWidget(self.menu, self.edit_stock, Qt.Vertical)

        self.addDockWidget(Qt.BottomDockWidgetArea, self.scientific_calculator)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.molecular_mass)

        self.splitDockWidget(self.scientific_calculator, self.molecular_mass, Qt.Horizontal)

        # Hide some of the docks so that the UI is not overcrowded
        self.remove_items.hide()
        self.remove_stock.hide()
        self.edit_stock.hide()

        self.scientific_calculator.hide()
        self.molecular_mass.hide()

    def create_toolbars(self):
        self.stock_toolbar = StockToolbar("Stock Toolbar", parent=self, view_stock_dock=self.view_stock)
        self.addToolBar(self.stock_toolbar)

    def setup_window(self):
        ''' Sets up the title, icon, menu bar etc. '''
        self.setWindowTitle("Pretzel")
        self.setWindowIcon(QIcon("data/pretzel/icon.svg"))
        self.menu_bar = self.create_menu_bar()
        self.setMenuBar(self.menu_bar)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Set the style
        style = Pretzel.ui.utils.load_style_from_file(os.path.join("data/styles/", self.settings["Style"] + ".qss"))
        Pretzel.ui.utils.apply_style(style)

        # Configure docks
        self.setTabPosition(Qt.AllDockWidgetAreas, QTabWidget.North)
        self.setDockOptions(self.AnimatedDocks | self.AllowNestedDocks | self.AllowTabbedDocks | self.GroupedDragging)

    @pyqtSlot(str)
    def toggle_dock(self, dock_name):
        if dock_name == "Add Items":
            self.add_items.toggleViewAction().trigger()
        elif dock_name == "Remove Items":
            self.remove_items.toggleViewAction().trigger()
        elif dock_name == "Scientific Calculator":
            self.scientific_calculator.toggleViewAction().trigger()
        else:
            pass

    def load_plugins(self):
        # TODO: This is a very basic plugin system. Will need to be improved
        #       in future
        for plugin in self.settings["Plugins"]:
            plugin_name = os.path.splitext(os.path.basename(plugin))[0].replace("_", " ").title()
            spec = importlib.util.spec_from_file_location(plugin_name, plugin)
            p = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(p)
            try:
                p.register(self)
            except NameError as e:
                print("All plugins must have a register method!")
                print(str(e))

    def add_dock_widget_plugin(self, plugin_class, dock_widget_area, shortcuts=[]):
        self.addDockWidget(dock_widget_area, plugin_class)
        plugin_class.toggleViewAction().setShortcuts(*shortcuts)

    def show_preferences(self):
        preferences_dialog = PreferencesDialog(self)
        preferences_dialog.exec_()

    def quit(self):
        # Unregister all plugins

        # Quit Pretzel
        QCoreApplication.quit()


if __name__ == '__main__':
    # TODO: Move PretzelWindow to separate file (application.py?)
    # TODO: Find a better loading/saving settings system (EasySettings)
    # TODO: when using uic.loadUi(), see if using relative paths will work (instead of "Pretzel/ui/test/test.ui etc.")
    # Setup the application
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    # Show the splash screen
    splash_img = QPixmap("data/pretzel/logo.svg")
    splash_screen = QSplashScreen(splash_img)
    splash_screen.show()

    # Init databases
    splash_screen.showMessage("Initializing Databases...", alignment=Qt.AlignRight | Qt.AlignBottom)
    app.processEvents()
    Pretzel.core.database.init.initialize_databases()
    logging.info("Initialized the databases")

    # Loading
    splash_screen.showMessage("Loading...", alignment=Qt.AlignRight | Qt.AlignBottom)
    app.processEvents()

    # Run Pretzel
    pretzel = PretzelWindow()

    # Add todolist plugin (only for testing)
    #from data.plugins.todo_list import todolist
    #todolistplugin = todolist.TodoListPlugin()
    #pretzel.add_dock_widget_plugin(todolistplugin, Qt.BottomDockWidgetArea, [QKeySequence("Ctrl+T")])

    pretzel.show()
    splash_screen.finish(pretzel)
    logging.info("Pretzel loaded successfully")
    sys.exit(app.exec_())
