from view.main_menu_panel import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from control.utilities import BaseWindow
from control.jetson_config_panel_control import JetsonConfigWindow
from control.simulation_config_panel_control import SimConfigWindow


class MainMenuWindow(BaseWindow):
    def __init__(
        self,
        app: QtWidgets.QApplication,
        **kwargs,
    ):
        super().__init__(
            app=app,
            UI=Ui_MainWindow,
            **kwargs,
        )
        self.kwargs = kwargs
        self.dialogs = list()

    def set_listener(self):
        super(MainMenuWindow, self).set_listener()
        self.ui.pushbtn_simconfig.clicked.connect(self.btn_simconfig_clicked)
        self.ui.pushbtn_jetsonconfig.clicked.connect(self.btn_jetsonconfig_clicked)

    def btn_simconfig_clicked(self):
        self.auto_wire_window(target_window=SimConfigWindow)

    def btn_jetsonconfig_clicked(self):
        self.auto_wire_window(target_window=JetsonConfigWindow)

    def auto_wire_window(self, target_window):
        target_app = target_window(self.app, **self.kwargs)
        self.dialogs.append(target_app)
        target_app.show()
        self.hide()
        target_app.show()
        target_app.closeEvent = self.app_close_event

    # rewires annotation_app's closing event
    def app_close_event(self, close_event):
        self.show()
