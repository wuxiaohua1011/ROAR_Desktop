from PyQt5 import QtWidgets
import sys
from pathlib import Path
import os
import logging


class Launcher:
    def __init__(self, debug=False, demo=False):
        self.logger = logging.getLogger(__name__)
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        logging.basicConfig(level=logging.INFO)
        logging.basicConfig(level=logging.WARNING)
        logging.basicConfig(level=logging.ERROR)
        logging.basicConfig(level=logging.CRITICAL)
        self.demo = demo  # not working yet

    def run(self, add_debug_path: bool = False):
        if add_debug_path:
            sys.path.append(Path(os.getcwd()).parent.parent.as_posix())

        app = QtWidgets.QApplication([])
        from control.main_menu_panel_control import MainMenuWindow
        from control.control_panel_control import ControlPanelWindow
        _ = MainMenuWindow(app, sim_config_json_file_path=Path(os.getcwd()).parent.parent /
                                                          "ROAR_Sim" / "configurations" / "configuration.json",
                           jetson_config_json_file_path=Path(os.getcwd()).parent.parent / "ROAR_Jetson" /
                                                        "configurations" / "configuration.json")
        app.exec()


if __name__ == "__main__":
    launcher = Launcher(debug=True)
    launcher.run(add_debug_path=True)
