from control.utilities import BaseWindow, PydanticModelEntry
from PyQt5 import QtCore, QtGui, QtWidgets
from view.jetson_config_panel import Ui_JetsonConfigWindow
from control.control_panel_control import ControlPanelWindow
from ROAR_Jetson.configurations.configuration import Configuration as JetsonConfigModel
from pprint import pprint
import json
from typing import Dict, Union


class JetsonConfigWindow(BaseWindow):
    def __init__(self, app: QtWidgets.QApplication, **kwargs):
        super().__init__(app, Ui_JetsonConfigWindow, **kwargs)
        self.setting_list = []
        self.setting_dict = dict()
        self.dialogs = list()
        self.jetson_config = JetsonConfigModel()
        self.fill_config_list()

    def set_listener(self):
        super(JetsonConfigWindow, self).set_listener()
        self.ui.pushButton_confirm.clicked.connect(self.pushButton_confirm)

    def fill_config_list(self):
        model_info: Dict[str, PydanticModelEntry] = dict()
        for key_name, entry in self.jetson_config.schema()["properties"].items():
            if "type" not in entry:
                continue
            model_info[key_name] = PydanticModelEntry.parse_obj(entry)
        model_values = self.jetson_config.dict()

        for name, entry in model_info.items():
            curr_value = model_values[name] if name in model_values else entry.default
            self.add_entry_to_settings_gui(name=name, value=curr_value)
            # self.test_input_list.append([name,str(curr_value)])
            self.setting_dict[name] = curr_value

    def add_entry_to_settings_gui(self, name: str, value: Union[str, int, float, bool]):
        label = QtWidgets.QLabel()
        label.setText(name)
        input_field = QtWidgets.QLineEdit()  # QTextEdit()
        input_field.setText(str(value))
        input_field.setObjectName(name)
        self.setting_list.append(input_field)
        # input_field.textChanged.connect(self.on_change)
        self.ui.formLayout.addRow(label, input_field)

    # def on_change(self,text): #changes debuging
    #     print("text changed: ", text)
    #     print(self.setting_list[1].text())
    #     print(self.setting_list[1].objectName())

    def isfloat(self, value):  # Check if its float in pushButton_confirm
        try:
            float(value)
            return True
        except ValueError:
            return False

    def pushButton_confirm(self):
        self.auto_wire_window(ControlPanelWindow)
        jetson_config_json = {}
        # print("start print\n")
        ## test_str = ""
        for widget in self.setting_list:
            # if isinstance(widget, QtWidgets.QLineEdit):
            # print(widget.objectName(), ":", widget.text())
            if widget.text().isnumeric():
                jetson_config_json[widget.objectName()] = int(widget.text())
            elif self.isfloat(widget.text()):
                jetson_config_json[widget.objectName()] = float(widget.text())
            elif widget.text().lower() == "true":
                jetson_config_json[widget.objectName()] = True
            elif widget.text().lower() == "false":
                jetson_config_json[widget.objectName()] = False
            else:
                jetson_config_json[widget.objectName()] = widget.text()

            # #test_str = test_str + "\n" + str(widget.objectName()) + " : " + str(widget.text())

        # print("\ntest_str= \n", test_str, "\n")
        # print("\njson= \n", jetson_config_json, "\n")
        # print("\n end print\n")

        json_object = json.dumps(jetson_config_json, indent=2)
        with open(
            "../../ROAR_Jetson/configurations/configuration_test.json", "w"
        ) as outfile:
            outfile.write(json_object)

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
