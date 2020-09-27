from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Thanks to Pavel Strakhov
# https://stackoverflow.com/questions/21805047/qtreewidget-to-mirror-python-dictionary
def fill_item(item, value, expanded=True):
    if expanded:
        item.setExpanded(True)

    if type(value) is dict:
        for key, val in iter(value.items()):
            child = QTreeWidgetItem()
            child.setText(0, key)
            item.addChild(child)
            fill_item(child, val)
    elif type(value) is list:
        for val in value:
            child = QTreeWidgetItem()
            item.addChild(child)
            if type(val) is dict:
                child.setText(0, '[dict]')
                fill_item(child, val)
            elif type(val) is list:
                child.setText(0, '[list]')
                fill_item(child, val)
            else:
                child.setText(0, val)

            if expanded:
                child.setExpanded(True)
    else:
        value = list(value)
        for c in value:
            child = QTreeWidgetItem()
            child.setText(0, value[value.index(c)])
            item.addChild(child)


def fill_widget(widget, value):
    widget.clear()
    fill_item(widget.invisibleRootItem(), value)
