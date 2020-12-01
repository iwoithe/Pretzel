from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QAction


class StockToolbar(QToolBar):
    def __init__(self, *args, parent=None, view_stock_dock=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.view_stock_dock = view_stock_dock
        self.setup_ui()

    def setup_ui(self):
        # Reload the Stock View dock
        self.action_reload_stock_view = QAction(QIcon("data/icons/reload_stock_view.svg"), "Reload Stock View", self)
        self.action_reload_stock_view.triggered.connect(self.reload_stock_view)
        self.addAction(self.action_reload_stock_view)

    def reload_stock_view(self):
        if self.view_stock_dock:
            self.view_stock_dock.load_stock()

