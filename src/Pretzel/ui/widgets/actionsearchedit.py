from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QLineEdit


class ActionSearchEdit(QLineEdit):
    moveSelectionUp = pyqtSignal()
    moveSelectionDown = pyqtSignal()

    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Up:
            self.moveSelectionUp.emit()
        elif event.key() == Qt.Key_Left:
            self.moveSelectionUp.emit()
        elif event.key() == Qt.Key_Down:
            self.moveSelectionDown.emit()
        elif event.key() == Qt.Key_Right:
            self.moveSelectionDown.emit()
        else:
            QLineEdit.keyPressEvent(self, event)
