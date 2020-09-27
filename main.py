#!/usr/bin/env python
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
import importlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ui.utils

from ui.menu import *
from ui.items import *
from ui.stock import *
from ui.reports import *

from ui.preferences import PreferencesDialog
from ui.tools.calculators import MolecularMass, ScientificCalculator

class Pretzel(QMainWindow):

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
        view_menu.addAction(self.menu.toggleViewAction())
        item_menu = view_menu.addMenu("Item")
        item_menu.addAction(self.add_items.toggleViewAction())
        item_menu.addAction(self.remove_items.toggleViewAction())
        stock_menu = view_menu.addMenu("Stock")

        # Tools
        tools_menu = self.menu_bar.addMenu("&Tools")
        # Calculators
        calculators_menu = tools_menu.addMenu("Calculators")
        calculators_menu.addAction(self.scientific_calculator.toggleViewAction())
        # Generation
        generation_menu = tools_menu.addMenu("Generation")
        generation_menu.addAction(self.generate_reports.toggleViewAction())
        #generation_menu.addAction(self.update_report.toggleViewAction())

        # Help
        help_menu = self.menu_bar.addMenu("&Help")
        help_menu.addAction(self.action_about_qt)

        return self.menu_bar

    def setup_ui(self):
        self.create_docks()
        self.setup_window()

    def create_docks(self):
        # Create and setup the dock widgets
        self.menu = Menu()
        # Or QKeySequence(Qt.CTRL + Qt.Key_M)
        self.menu.toggleViewAction().setShortcuts(QKeySequence("Ctrl+M"))
        self.menu.toggleDock.connect(self.toggle_dock)

        self.add_items = AddItems(self)
        self.add_items.toggleViewAction().setShortcuts(QKeySequence("Shift+A"))

        self.remove_items = RemoveItems(self)
        self.remove_items.toggleViewAction().setShortcuts(QKeySequence("Shift+R"))

        self.generate_reports = GenerateReports(self)
        self.generate_reports.toggleViewAction().setShortcuts(QKeySequence("Ctrl+G"))

        self.scientific_calculator = ScientificCalculator()
        self.scientific_calculator.toggleViewAction().setShortcuts(QKeySequence("Alt+C"))

        self.molecular_mass = MolecularMass()
        self.molecular_mass.toggleViewAction().setShortcuts(QKeySequence("Shift+M"))

        # Add docks

        self.addDockWidget(Qt.LeftDockWidgetArea, self.menu)

        self.addDockWidget(Qt.RightDockWidgetArea, self.add_items)
        self.addDockWidget(Qt.RightDockWidgetArea, self.remove_items)

        self.addDockWidget(Qt.RightDockWidgetArea, self.generate_reports)

        self.splitDockWidget(self.add_items, self.generate_reports, Qt.Horizontal)
        self.splitDockWidget(self.add_items, self.remove_items, Qt.Vertical)

        self.addDockWidget(Qt.BottomDockWidgetArea, self.scientific_calculator)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.molecular_mass)

        self.splitDockWidget(self.scientific_calculator, self.molecular_mass, Qt.Horizontal)

        # Hide some of the docks so that the UI is not overcrowded
        self.generate_reports.hide()
        self.remove_items.hide()

        self.scientific_calculator.hide()
        self.molecular_mass.hide()

    def setup_window(self):
        ''' Sets up the title, icon, menu bar etc. '''
        self.setWindowTitle("Pretzel")
        self.menu_bar = self.create_menu_bar()
        self.setMenuBar(self.menu_bar)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Set the style
        style = ui.utils.load_style_from_file(os.path.join("data/styles/", self.settings["Style"] + ".qss"))
        ui.utils.apply_style(style)

        # Configue docks
        self.setTabPosition(Qt.AllDockWidgetAreas, QTabWidget.North)
        self.setDockOptions(self.AnimatedDocks | self.AllowNestedDocks | self.AllowTabbedDocks | self.GroupedDragging)

    @pyqtSlot(str)
    def toggle_dock(self, dock_name):
        if dock_name == "Add Items":
            self.add_items.toggleViewAction().trigger()
        elif dock_name == "Remove Items":
            self.remove_items.toggleViewAction().trigger()
        elif dock_name == "Generate Reports":
            self.generate_reports.toggleViewAction().trigger()
        elif dock_name == "Scientific Calculator":
            self.scientific_calculator.toggleViewAction().trigger()
        else:
            pass

    def load_plugins(self):
        # TODO: This is a very basic plugin system. Will need to be improved
        #       in future
        for plugin_path in self.settings["Plugin Paths"]:
            valid_file_types = [os.path.join(plugin_path, "*.py")]
            for file_type in valid_file_types:
                plugins = glob.glob(file_type)
                for plugin in plugins:
                    plugin_name = os.path.splitext(os.path.basename(plugin))[0].replace("_", " ").title()
                    spec = importlib.util.spec_from_file_location(plugin_name, plugin)
                    p = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(p)
                    try:
                        p.register(self)
                    except NameError as e:
                        print("All plugins must have a register method!")
                        print(str(e))

    def show_preferences(self):
        preferences_dialog = PreferencesDialog(self)
        preferences_dialog.exec_()

    def quit(self):
        QCoreApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Temporarily set the style, until I've written my own styles
    app.setStyle("fusion")
    pretzel = Pretzel()
    pretzel.show()
    sys.exit(app.exec_())
