from control.utilities import ConfigWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from view.jetson_config_panel import Ui_JetsonConfigWindow
from control.agent_config_panel import AgentConfigWindow
from ROAR_Jetson.configurations.configuration import Configuration as JetsonConfigModel
from pprint import pprint
import json
from typing import Dict, Union
from pathlib import Path


class JetsonConfigWindow(ConfigWindow):
    def __init__(self, app, **kwargs):
        super(JetsonConfigWindow, self).__init__(app=app,
                                                 UI=Ui_JetsonConfigWindow,
                                                 config_json_file_path=kwargs["jetson_config_json_file_path"],
                                                 ConfigModel=JetsonConfigModel,
                                                 NextWindowClass=AgentConfigWindow
                                                 )


