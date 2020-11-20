from control.utilities import BaseWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from view.agent_config_panel import Ui_AgentConfigWindow
from control.control_panel_control import ControlPanelWindow
from ROAR.configurations.configuration import Configuration as AgentConfiguration
from pprint import pprint
import json
from typing import Dict, Union
from pathlib import Path


class AgentConfigWindow(BaseWindow):
    def __init__(self, app: QtWidgets.QApplication, agent_config_path: Path, **kwargs):
        super().__init__(app, Ui_AgentConfigWindow, **kwargs)
        self.agent_config = AgentConfiguration()
        self.agent_config_path: Path = agent_config_path
        self.fill_config_list()

    def set_listener(self):
        super(AgentConfigWindow, self).set_listener()
        self.ui.pushButton_confirm.clicked.connect(self.pushButton_confirm)
        self.ui.actionSave.triggered.connect(self.action_save)

    def action_save(self):
        config_file = self.agent_config_path.open('w')
        content = json.dumps(self.agent_config.dict(), indent=2)
        config_file.write(content)
        config_file.close()
        self.logger.info(f"Configuration saved to {self.agent_config_path}")

    def fill_config_list(self):
        model_info: Dict[str, Union[str, int, float, bool]] = dict()
        self.agent_config.parse_file(self.agent_config_path)
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
