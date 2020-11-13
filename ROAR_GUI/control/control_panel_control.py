
from control.utilities import BaseWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from view.control_panel import Ui_ControlPanelWindow


class ControlPanelWindow(BaseWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__(app, Ui_ControlPanelWindow)

    def set_listener(self):
        super(ControlPanelWindow, self).set_listener()
