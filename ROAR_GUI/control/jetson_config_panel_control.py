from control.utilities import BaseWindow, PydanticModelEntry
from PyQt5 import QtCore, QtGui, QtWidgets
from view.jetson_config_panel import Ui_JetsonConfigWindow
from control.control_panel_control import ControlPanelWindow
from ROAR_Jetson.configurations.configuration import Configuration as JetsonConfigModel
from pprint import pprint
import json
from typing import Dict, Union
from pathlib import Path

class JetsonConfigWindow(BaseWindow):
    def __init__(self, app: QtWidgets.QApplication, jetson_config_json_file_path:Path, **kwargs):
        super().__init__(app, Ui_JetsonConfigWindow, **kwargs)
        self.dialogs = list()
        self.jetson_config = JetsonConfigModel()
        self.jetson_config_json_file_path:Path = jetson_config_json_file_path
        self.fill_config_list()

    def set_listener(self):
        super(JetsonConfigWindow, self).set_listener()
        self.ui.pushButton_confirm.clicked.connect(self.pushButton_confirm)

    def fill_config_list(self):
        model_info: Dict[str, Union[str, int, float, bool]] = dict()
        self.jetson_config.parse_file(self.jetson_config_json_file_path)
        for key_name, entry in self.jetson_config.dict().items():
            if type(entry) in [str, int, float, bool]:
                model_info[key_name] = entry

        for name, entry in model_info.items():
            self.add_entry_to_settings_gui(name=name, value=entry)

    def add_entry_to_settings_gui(self, name: str, value: Union[str, int, float, bool]):
        label = QtWidgets.QLabel()
        label.setText(name)
        input_field = QtWidgets.QTextEdit()
        input_field.setText(str(value))
        self.ui.formLayout.addRow(label, input_field)

    def pushButton_confirm(self):
        self.auto_wire_window(ControlPanelWindow)

    def auto_wire_window(self, target_window):
        target_app = target_window(self.app)
        self.dialogs.append(target_app)
        target_app.show()
        self.hide()
        target_app.show()
        target_app.closeEvent = self.app_close_event

    # rewires annotation_app's closing event
    def app_close_event(self, close_event):
        self.show()
