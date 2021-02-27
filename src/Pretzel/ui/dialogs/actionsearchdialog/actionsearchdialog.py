from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (QWidget, QDialog, QVBoxLayout, QListWidget,
                             QListWidgetItem, QAction)

from Pretzel.ui.widgets import ActionSearchEdit


class ActionSearchDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.parent = parent
        self.actions = self.get_actions()
        self.setup_ui()

    def get_actions(self):
        actions = []
        try:
            for action in self.parent.findChildren(QAction):
                if not (action.isSeparator() or action.menu()):
                    # Don't include the menu bar actions
                    actions.append(action)
        except:
            for action in self.findChildren(QAction):
                actions.append(action)

        return actions

    def setup_ui(self):
        # Setup the dialog
        self.setObjectName("ActionSearchDialog")
        self.resize(self.parent.width() / 3, self.parent.height() / 3)
        self.setWindowFlags(Qt.Popup)

        # The content
        layout = QVBoxLayout()

        self.action_search_edit = ActionSearchEdit()
        self.action_search_edit.setObjectName("action_search_edit")
        self.action_search_edit.setPlaceholderText("Search for action...")

        layout.addWidget(self.action_search_edit)

        self.actions_list = QListWidget()
        self.actions_list.setObjectName("actions_list")
        # Sorting
        # TODO: Add an option in the preferences to set how to sort the actions
        self.actions_list.setSortingEnabled(True)
        self.actions_list.sortItems(Qt.AscendingOrder)
        # TODO: Add option in preferences to set the number of actions displayed
        # Actions
        for action in self.actions:
            action_widget = QListWidgetItem(action.iconText())
            action_widget.action = action
            self.actions_list.addItem(action_widget)

        # Select the first item
        self.actions_list.item(0).setSelected(True)

        layout.addWidget(self.actions_list)

        self.setLayout(layout)

        self.action_search_edit.setFocus()

        # Bind the signals
        self.bind_signals()


    def bind_signals(self):
        self.action_search_edit.textEdited.connect(self.filter_actions)
        self.action_search_edit.moveSelectionUp.connect(self.move_selection_up)
        self.action_search_edit.moveSelectionDown.connect(self.move_selection_down)
        self.action_search_edit.returnPressed.connect(self.run_action)
        self.actions_list.itemDoubleClicked.connect(self.run_action_double_clicked)

    def move_selection_up(self):
        lim = self.actions_list.count()
        for i in range(lim):
            if self.actions_list.item(i).isSelected():
                if (i - 1) < 0:
                    # Select the bottom item
                    self.actions_list.item(lim - 1).setSelected(True)
                else:
                    # Select the item above the current one
                    self.actions_list.item(i - 1).setSelected(True)

                break

    def move_selection_down(self):
        lim = self.actions_list.count()
        for i in range(lim):
            if self.actions_list.item(i).isSelected():
                if (i + 1) > (lim - 1):
                    self.actions_list.item(0).setSelected(True)
                else:
                    self.actions_list.item(i + 1).setSelected(True)

                break

    @pyqtSlot(str)
    def filter_actions(self, text: str):
        """ Filters the action lists actions """
        self.actions_list.clear()
        for action in self.actions:
            if text.lower() in action.iconText().lower():
                action_widget = QListWidgetItem(action.iconText())
                action_widget.action = action
                self.actions_list.addItem(action_widget)

        # Select the first item
        self.actions_list.item(0).setSelected(True)

    @pyqtSlot()
    def run_action(self):
        selected_item = self.actions_list.selectedItems()[0]
        selected_item.action.trigger()
        self.close()

    @pyqtSlot(QListWidgetItem)
    def run_action_double_clicked(self, item: QListWidgetItem):
        """ Triggers the items action """
        item.action.trigger()
        self.close()
