from Pretzel.api import PretzelWindow

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence


def register_plugin(classes):
    for cls in classes:
        PretzelWindow.add_dock_widget_plugin(cls, Qt.BottomDockWidgetArea, cls.shortcuts)