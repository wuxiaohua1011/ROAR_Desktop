from control.utilities import BaseWindow, PydanticModelEntry
from PyQt5 import QtCore, QtGui, QtWidgets
from view.simulation_config_panel import Ui_SimulationConfigWindow
from ROAR_Sim.configurations.configuration import Configuration as SimulationConfig
from pprint import pprint
import json
from typing import Dict, Union


class SimConfigWindow(BaseWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__(app, Ui_SimulationConfigWindow)

        self.simulation_config = SimulationConfig()
        self.fill_config_list()

    def fill_config_list(self):
        model_info: Dict[str, PydanticModelEntry] = dict()
        for key_name, entry in self.simulation_config.schema()['properties'].items():
            if "type" not in entry:
                continue
            model_info[key_name] = PydanticModelEntry.parse_obj(entry)
        model_values = self.simulation_config.dict()

        for name, entry in model_info.items():
            self.add_entry_to_settings_gui(name=name,
                                           value=model_values[name] if name in model_values else entry.default)

    def add_entry_to_settings_gui(self, name: str, value: Union[str, int, float, bool]):
        label = QtWidgets.QLabel()
        label.setText(name)
        input_field = QtWidgets.QTextEdit()
        input_field.setText(str(value))
        self.ui.formLayout.addRow(label, input_field)

    def set_listener(self):
        super(SimConfigWindow, self).set_listener()
