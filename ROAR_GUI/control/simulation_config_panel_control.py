from control.utilities import BaseWindow, PydanticModelEntry
from PyQt5 import QtCore, QtGui, QtWidgets
from view.simulation_config_panel import Ui_SimulationConfigWindow
from control.control_panel_control import ControlPanelWindow
from ROAR_Sim.configurations.configuration import Configuration as SimulationConfig
from pprint import pprint
import json
from typing import Dict, Union, Any
from pathlib import Path


class SimConfigWindow(BaseWindow):
    def __init__(self, app: QtWidgets.QApplication, sim_json_config_file_path: Path, **kwargs):
        super().__init__(app, Ui_SimulationConfigWindow, **kwargs)
        self.setting_list = []
        self.setting_dict = dict()
        self.dialogs = list()
        self.simulation_config = SimulationConfig()
        self.json_config_file_path: Path = sim_json_config_file_path
        self.model_info: Dict[str, PydanticModelEntry] = self.fill_config_list()

        # self.text_change()
        #####
        # self.currentTextChanged.connect(self.onCurrentTextChanged)

    # def onCurrentTextChanged(self, text):
    #     print("\n text changed \n")

    def fill_config_list(self) -> Dict[str, Any]:
        model_info: Dict[str, Any] = dict()
        for key_name, entry in self.simulation_config.schema()['properties'].items():
            if "type" not in entry:
                continue
            model_info[key_name] = entry['title'] #PydanticModelEntry.parse_obj(entry)
            #pprint(entry)

        json_dict: dict = json.load(self.json_config_file_path.open('r'))
        for key_name, entry in json_dict.items():
            pass
            model_info[key_name] = entry
            # TODO update model_info
            #print(key_name, entry)
        model_values = self.simulation_config.dict()
        # print("len:  ",len(model_info.items()))
        ##print(self.test_input_list)
        # print(self.setting_dict)

        for name, entry in model_info.items():
            # TODO do not populate if it is not of type [int, float, string, bool]
            curr_value = model_values[name] if name in model_values else entry.default
            self.add_entry_to_settings_gui(name=name,
                                           value=curr_value)
            # self.test_input_list.append([name,str(curr_value)])

            self.setting_dict[name] = curr_value
        # self.logger.debug()
        return model_info

    def add_entry_to_settings_gui(self, name: str, value: Union[str, int, float, bool]):
        label = QtWidgets.QLabel()
        label.setText(name)
        input_field = QtWidgets.QLineEdit()  # QTextEdit()
        input_field.setText(str(value))
        input_field.setObjectName(name)
        self.setting_list.append(input_field)
        # input_field.textChanged.connect(self.on_change)
        # self.test_input_list.append(str(value))

        self.ui.formLayout.addRow(label, input_field)

    def set_listener(self):
        super(SimConfigWindow, self).set_listener()
        self.ui.pushButton_confirm.clicked.connect(self.pushButton_confirm)

    # def on_change(self,text):
    #     print("text changed: ", text)
    #     print(self.setting_list[1].text())
    #     print(self.setting_list[1].objectName())
    # print(self.setting_dict)

    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def pushButton_confirm(self):
        self.auto_wire_window(ControlPanelWindow)
        sim_config_json = {}
        #     "a" : "1",
        #     "b" : "2",
        #     "c" : "3"
        # }
        # print("start print\n")
        # for key_name, entry in self.simulation_config.schema()['properties'].items():
        # self.fill_config_list()
        # for key_name, entry in self.fill_config_list():
        #    print(key_name," : ",entry)
        # print(self.input_list)
        ##test_str = ""
        for widget in self.setting_list:
            # if isinstance(widget, QtWidgets.QLineEdit):
            # print(widget.objectName(),":", widget.text())
            if widget.text().isnumeric():
                sim_config_json[widget.objectName()] = int(widget.text())
            elif self.isfloat(widget.text()):
                sim_config_json[widget.objectName()] = float(widget.text())
            elif widget.text().lower() == "true":
                sim_config_json[widget.objectName()] = True
            elif widget.text().lower() == "false":
                sim_config_json[widget.objectName()] = False
            else:
                sim_config_json[widget.objectName()] = widget.text()

            ##test_str = test_str + "\n" + str(widget.objectName()) + " : " + str(widget.text())

        # print("\ntest_str= \n",test_str,"\n")
        # print("\njson= \n", sim_config_json, "\n")
        # print("\n end print\n")
        sim_config_json["weather"] = {
            "cloudiness": 10,
            "precipitation": 0,
            "precipitation_deposits": 0,
            "wind_intensity": 0,
            "sun_azimuth_angle": 90,
            "sun_altitude_angle": 90,
            "fog_density": 0,
            "fog_distance": 0,
            "wetness": 0
        }
        sim_config_json["color"] = {
            "r": 255,
            "g": 0,
            "b": 0,
            "a": 255
        }
        json_object = json.dumps(sim_config_json, indent=2)
        # current C:\Users\Zetian\Desktop\project\ROAR\ROAR_Desktop\ROAR_GUI
        # need    C:\Users\Zetian\Desktop\project\ROAR\ROAR_Sim\configurations
        # pathlib
        with open("../../ROAR_Sim/configurations/configuration_test.json", "w") as outfile:
            outfile.write(json_object)

    def auto_wire_window(self, target_window):
        target_app = target_window(self.app)
        self.dialogs.append(target_app)
        target_app.show()
        self.hide()
        target_app.show()
        target_app.closeEvent = self.app_close_event

    def app_close_event(self, close_event):
        self.show()
