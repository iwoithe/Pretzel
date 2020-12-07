from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QAction


class TableToolbar(QToolBar):
    def __init__(self, *args, parent=None, view_items_dock=None, view_stock_dock=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.view_items_dock = view_items_dock
        self.view_stock_dock = view_stock_dock
        self.setup_ui()

    def setup_ui(self):
        # Reload the Stock View dock
        self.action_reload_tables = QAction(QIcon("data/icons/reload_tables.svg"), "Reload Tables", self)
        self.action_reload_tables.triggered.connect(self.reload_tables)
        self.addAction(self.action_reload_tables)

    def reload_tables(self):
        if self.view_items_dock and self.view_stock_dock:
            self.view_items_dock.load_items()
            self.view_stock_dock.load_stock()

