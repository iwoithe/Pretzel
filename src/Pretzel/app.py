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

import os
import glob
import importlib
import easysettings

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Pretzel.ui.utils

from Pretzel.ui.menu import *
from Pretzel.ui.items import AddItems, EditItems, RemoveItems, ViewItems

from Pretzel.ui.stock import AddStock, RemoveStock, EditStock, ViewStock
from Pretzel.ui.dialogs import (ImportItemsDialog, AboutDialog, PreferencesDialog,
                                ActionSearchDialog)
from Pretzel.ui.toolbars import TableToolbar
from Pretzel.ui.tools.calculators import MolecularMass, ScientificCalculator

from Pretzel.core.paths import settings_file

# TODO: Move to Pretzel.core?
from Pretzel.ui.workspaces import WorkspaceAction, set_workspace


class PretzelWindow(QMainWindow):

    settings = easysettings.load_json_settings(settings_file)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.workspaces = []
        self.load_available_workspaces()

        self.setup_ui()

        self.load_plugins()

    def setup_ui(self):
        self.create_actions()
        self.create_docks()
        self.create_toolbars()
        self.setup_window()

    def create_actions(self):
        # Quit
        self.action_quit = QAction("Quit", self)
        self.action_quit.setStatusTip("Quit the application")
        self.action_quit.setShortcuts(QKeySequence("Ctrl+Q"))
        self.action_quit.triggered.connect(self.quit)

        # Import Items
        self.action_import = QAction("Import", self)
        self.action_import.setShortcuts(QKeySequence("Ctrl+I"))
        self.action_import.triggered.connect(self.show_import_items_dialog)

        # Preferences
        self.action_preferences = QAction("Preferences", self)
        self.action_preferences.setStatusTip("Open the preferences")
        self.action_preferences.setShortcuts(QKeySequence("Ctrl+Shift+P"))
        self.action_preferences.triggered.connect(self.show_preferences)

        # Action Search
        self.action_action_search = QAction("Action Search", self)
        self.action_action_search.setShortcuts(QKeySequence("F3"))
        self.action_action_search.triggered.connect(self.show_action_search_dialog)

        # About
        self.action_about = QAction("About", self)
        self.action_about.setStatusTip("About Pretzel")
        self.action_about.triggered.connect(self.show_about_dialog)

        # About Qt
        self.action_about_qt = QAction("About Qt", self)
        self.action_about_qt.setStatusTip("About Qt")
        self.action_about_qt.triggered.connect(QApplication.instance().aboutQt)

    def create_docks(self):
        # Create and setup the dock widgets
        self.menu = Menu(self)
        # Or QKeySequence(Qt.CTRL + Qt.Key_M)
        self.menu.toggleViewAction().setShortcuts(QKeySequence("Ctrl+M"))
        self.menu.toggleDock.connect(self.toggle_dock)

        # Items
        self.add_items = AddItems(self)
        self.add_items.toggleViewAction().setShortcuts(QKeySequence("Shift+A"))
        self.remove_items = RemoveItems(self)
        self.remove_items.toggleViewAction().setShortcuts(QKeySequence("Shift+R"))
        self.edit_items = EditItems(self)
        self.edit_items.toggleViewAction().setShortcuts(QKeySequence("Shift+E"))
        self.view_items = ViewItems(self)
        self.view_items.toggleViewAction().setShortcuts(QKeySequence("Shift+I"))

        # Stock
        self.add_stock = AddStock(self)
        self.add_stock.toggleViewAction().setShortcuts(QKeySequence("Ctrl+A"))
        self.remove_stock = RemoveStock(self)
        self.remove_stock.toggleViewAction().setShortcuts(QKeySequence("Ctrl+R"))
        self.edit_stock = EditStock(self)
        self.edit_stock.toggleViewAction().setShortcuts(QKeySequence("Ctrl+E"))
        self.view_stock = ViewStock(self)
        self.view_stock.toggleViewAction().setShortcuts(QKeySequence("Shift+V"))

        self.scientific_calculator = ScientificCalculator(self)
        self.scientific_calculator.toggleViewAction().setShortcuts(QKeySequence("Alt+C"))

        self.molecular_mass = MolecularMass(self)
        self.molecular_mass.toggleViewAction().setShortcuts(QKeySequence("Shift+M"))

        set_workspace(self, "data/workspaces/default.xml")

    def create_toolbars(self):
        self.table_toolbar = TableToolbar("Table Toolbar", parent=self, view_items_dock=self.view_items, view_stock_dock=self.view_stock)
        self.addToolBar(self.table_toolbar)

    def setup_window(self):
        ''' Sets up the title, icon, menu bar etc. '''
        self.setWindowTitle("Pretzel")
        self.setWindowIcon(QIcon("data/pretzel/icon.svg"))
        self.menu_bar = self.create_menu_bar()
        self.setMenuBar(self.menu_bar)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Set the style
        style = Pretzel.ui.utils.load_style_from_file(os.path.join("data/styles/", self.settings.get("Style") + ".qss"))
        Pretzel.ui.utils.apply_style(style)

        # Configure docks
        self.setTabPosition(Qt.AllDockWidgetAreas, QTabWidget.North)
        self.setDockOptions(self.AnimatedDocks | self.AllowNestedDocks | self.AllowTabbedDocks | self.GroupedDragging)

    def create_menu_bar(self):
        self.menu_bar = QMenuBar()

        # File
        file_menu = self.menu_bar.addMenu("&File")
        file_menu.addAction(self.action_import)
        file_menu.addSeparator()
        file_menu.addAction(self.action_quit)

        # Edit
        edit_menu = self.menu_bar.addMenu("&Edit")
        edit_menu.addAction(self.action_preferences)

        # View
        view_menu = self.menu_bar.addMenu("&View")
        dock_menu = view_menu.addMenu("Docks")
        # Items
        item_menu = dock_menu.addMenu("Item")
        item_menu.addAction(self.add_items.toggleViewAction())
        item_menu.addAction(self.remove_items.toggleViewAction())
        item_menu.addAction(self.edit_items.toggleViewAction())
        item_menu.addAction(self.view_items.toggleViewAction())
        # Stock
        stock_menu = dock_menu.addMenu("Stock")
        stock_menu.addAction(self.add_stock.toggleViewAction())
        stock_menu.addAction(self.remove_stock.toggleViewAction())
        stock_menu.addAction(self.edit_stock.toggleViewAction())
        stock_menu.addAction(self.view_stock.toggleViewAction())
        # Tools
        tools_menu = dock_menu.addMenu("Tools")
        tools_menu.addAction(self.scientific_calculator.toggleViewAction())
        tools_menu.addAction(self.molecular_mass.toggleViewAction())

        dock_menu.addAction(self.menu.toggleViewAction())

        # Toolbars
        toolbar_menu = view_menu.addMenu("Toolbars")
        toolbar_menu.addAction(self.table_toolbar.toggleViewAction())

        # Workspaces
        workspace_menu = view_menu.addMenu("Workspaces")
        for workspace_action in self.workspaces:
            workspace_menu.addAction(workspace_action)

        # Help
        help_menu = self.menu_bar.addMenu("&Help")
        help_menu.addAction(self.action_action_search)
        help_menu.addSeparator()
        help_menu.addAction(self.action_about)
        help_menu.addAction(self.action_about_qt)

        return self.menu_bar

    def load_available_workspaces(self):
        # TODO: Search the user data folder for custom workspaces (not just the bundled ones)
        # TODO: Create submenus from workspace subdirectories (e.g. instead of View > Workspaces > Add Items,
        #  use View > Workspaces > Items > Add Items)
        for workspace_file in glob.glob("data/workspaces/**/*.xml", recursive=True):
            workspace_name = os.path.splitext(os.path.basename(workspace_file))[0].replace("_", " ").title()
            workspace_action = WorkspaceAction(name=workspace_name, parent=self, workspaceFile=workspace_file)
            self.workspaces.append(workspace_action)

    def load_plugins(self):
        # TODO: This is a very basic plugin system. Will need to be improved in future
        for plugin in self.settings.get("Plugins"):
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

    @pyqtSlot(str)
    def toggle_dock(self, dock_name):
        if dock_name == "Add Items":
            self.add_items.toggleViewAction().trigger()
        elif dock_name == "Edit Items":
            self.edit_items.toggleViewAction().trigger()
        elif dock_name == "Remove Items":
            self.remove_items.toggleViewAction().trigger()
        elif dock_name == "View Items":
            self.view_items.toggleViewAction().trigger()
        elif dock_name == "Add Stock":
            self.add_items.toggleViewAction().trigger()
        elif dock_name == "Edit Stock":
            self.edit_items.toggleViewAction().trigger()
        elif dock_name == "Remove Stock":
            self.remove_items.toggleViewAction().trigger()
        elif dock_name == "View Stock":
            self.view_items.toggleViewAction().trigger()
        elif dock_name == "Molecular Mass":
            self.molecular_mass.toggleViewAction().trigger()
        elif dock_name == "Scientific Calculator":
            self.scientific_calculator.toggleViewAction().trigger()
        else:
            pass

    @pyqtSlot()
    def show_preferences(self):
        preferences_dialog = PreferencesDialog(self)
        preferences_dialog.exec()

    @pyqtSlot()
    def show_about_dialog(self):
        about_dialog = AboutDialog(parent=self)
        about_dialog.exec()

    @pyqtSlot()
    def show_action_search_dialog(self):
        action_search_dialog = ActionSearchDialog(parent=self)
        action_search_dialog.exec()

    @pyqtSlot()
    def show_import_items_dialog(self):
        import_items_dialog = ImportItemsDialog(parent=self)
        import_items_dialog.exec()

    @pyqtSlot()
    def quit(self):
        # Unregister all plugins

        # Quit Pretzel
        QCoreApplication.quit()
