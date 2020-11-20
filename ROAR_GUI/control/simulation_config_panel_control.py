from control.utilities import ConfigWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from view.simulation_config_panel import Ui_SimulationConfigWindow
from ROAR_Sim.configurations.configuration import Configuration as SimulationConfig
from pprint import pprint
import json
from typing import Dict, Union
from pathlib import Path
from control.agent_config_panel import AgentConfigWindow


class SimConfigWindow(ConfigWindow):
    def __init__(self, app,  **kwargs):
        super(SimConfigWindow, self).__init__(app=app,
                                              UI=Ui_SimulationConfigWindow,
                                              config_json_file_path=kwargs["sim_config_json_file_path"],
                                              ConfigModel=SimulationConfig,
                                              NextWindowClass=AgentConfigWindow
                                              )
