from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QAction

from Pretzel.ui.workspaces import set_workspace


class WorkspaceAction(QAction):
    def __init__(self, *args, **kwargs):
        super(WorkspaceAction, self).__init__(kwargs["name"], kwargs["parent"])

        # if hasattr(kwargs, "workspaceFile"):
        #     self._workspaceFile = kwargs["workspaceFile"]
        # else:
        #     self._workspaceFile = "data/workspaces/default.xml"

        self._workspaceFile = kwargs["workspaceFile"]

        self.triggered.connect(self.setWorkspace)

    def workspaceFile(self):
        return self._workspaceFile

    def setWorkspaceFile(self, file):
        self._workspaceFile = file

    @pyqtSlot()
    def setWorkspace(self):
        set_workspace(self.parent(), self.workspaceFile())


