from control.utilities import BaseWindow, PydanticModelEntry
from PyQt5 import QtCore, QtGui, QtWidgets
from view.jetson_config_panel import Ui_JetsonConfigWindow
from control.control_panel_control import ControlPanelWindow
from ROAR_Jetson.configurations.configuration import Configuration as JetsonConfigModel
from pprint import pprint
import json
from typing import Dict, Union


class JetsonConfigWindow(BaseWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__(app, Ui_JetsonConfigWindow)
        self.dialogs = list()
        self.jetson_config = JetsonConfigModel()
        self.fill_config_list()

    def set_listener(self):
        super(JetsonConfigWindow, self).set_listener()
        self.ui.pushButton_confirm.clicked.connect(self.pushButton_confirm)

    def fill_config_list(self):
        model_info: Dict[str, PydanticModelEntry] = dict()
        for key_name, entry in self.jetson_config.schema()['properties'].items():
            if "type" not in entry:
                continue
            model_info[key_name] = PydanticModelEntry.parse_obj(entry)
        model_values = self.jetson_config.dict()

        for name, entry in model_info.items():
            self.add_entry_to_settings_gui(name=name,
                                           value=model_values[name] if name in model_values else entry.default)

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
