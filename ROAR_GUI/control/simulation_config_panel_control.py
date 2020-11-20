from control.utilities import BaseWindow, PydanticModelEntry
from PyQt5 import QtCore, QtGui, QtWidgets
from view.simulation_config_panel import Ui_SimulationConfigWindow
from ROAR_Sim.configurations.configuration import Configuration as SimulationConfig
from pprint import pprint
import json
from typing import Dict, Union
from pathlib import Path

class SimConfigWindow(BaseWindow):
    def __init__(self, app: QtWidgets.QApplication, sim_config_json_file_path: Path):
        super().__init__(app, Ui_SimulationConfigWindow)
        self.simulation_config = SimulationConfig()
        self.simulation_config_json_file_path = sim_config_json_file_path
        self.fill_config_list()


    def fill_config_list(self):
        model_info: Dict[str, Union[str, int, float, bool]] = dict()
        self.simulation_config.parse_file(self.simulation_config_json_file_path)

        for key_name, entry in self.simulation_config.dict().items():
            if type(entry) in [str, int, float, bool]:
                model_info[key_name] = entry

        for name, entry in model_info.items():
            self.add_entry_to_settings_gui(name=name,
                                           value=entry)

    def add_entry_to_settings_gui(self, name: str, value: Union[str, int, float, bool]):
        label = QtWidgets.QLabel()
        label.setText(name)
        input_field = QtWidgets.QTextEdit()
        input_field.setText(str(value))
        self.ui.formLayout.addRow(label, input_field)

    def set_listener(self):
        super(SimConfigWindow, self).set_listener()
