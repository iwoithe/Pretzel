import xml.etree.ElementTree as ET
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QMainWindow


def set_workspace(window: QMainWindow, file: str):
    tree = ET.parse(file)
    root = tree.getroot()

    if root.tag == "Workspace":
        # Hide all dock widgets
        for dock in window.findChildren(QDockWidget):
            dock.hide()

        for child in root.iter("Dock"):
            dock_name = child.attrib["name"]
            dock = window.findChild(QDockWidget, dock_name)
            if dock:
                # Change where the area which the dock widget is placed
                try:
                    dock_area = child.attrib["area"]
                    if dock_area:
                        try:
                            window.removeDockWidget(dock)
                        except:
                            pass

                        if dock_area == "Left":
                            window.addDockWidget(Qt.LeftDockWidgetArea, dock)
                        elif dock_area == "Right":
                            window.addDockWidget(Qt.RightDockWidgetArea, dock)
                        elif dock_area == "Top":
                            window.addDockWidget(Qt.TopDockWidgetArea, dock)
                        elif dock_area == "Bottom":
                            window.addDockWidget(Qt.BottomDockWidgetArea, dock)
                        else:
                            window.addDockWidget(Qt.LeftDockWidgetArea, dock)
                except KeyError:
                    pass

                # Show or hide the dock widget
                try:
                    dock_show = child.attrib["show"]
                    if dock_show == "True":
                        dock.show()
                    else:
                        dock.hide()
                except KeyError:
                    pass

        for child in root.iter("SplitDocks"):
            dock1_name = child.attrib["dock1"]
            dock2_name = child.attrib["dock2"]
            dock1 = window.findChild(QDockWidget, dock1_name)
            dock2 = window.findChild(QDockWidget, dock2_name)
            split_orientation = child.attrib["orientation"]
            if split_orientation == "Horizontal":
                window.splitDockWidget(dock1, dock2, Qt.Horizontal)
            elif split_orientation == "Vertical":
                window.splitDockWidget(dock1, dock2, Qt.Vertical)
            else:
                pass

        for child in root.iter("TabbifyDocks"):
            dock1_name = child.attrib["dock1"]
            dock2_name = child.attrib["dock2"]
            dock1 = window.findChild(QDockWidget, dock1_name)
            dock2 = window.findChild(QDockWidget, dock2_name)
            window.tabifyDockWidget(dock1, dock2)

        # Focus the dock widget
        for child in root.iter("Dock"):
            dock_name = child.attrib["name"]
            dock = window.findChild(QDockWidget, dock_name)
            try:
                dock_focus = child.attrib["focus"]
                if dock_focus == "True":
                    dock.raise_()
            except KeyError:
                pass
