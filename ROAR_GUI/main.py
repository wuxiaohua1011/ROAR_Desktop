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
        _ = ControlPanelWindow(app)
        app.exec()


if __name__ == "__main__":
    launcher = Launcher(debug=True)
    launcher.run(add_debug_path=True)
    # import numpy as np
    # import cv2
    #
    # cap = cv2.VideoCapture(0)
    #
    # while True:
    #     # Capture frame-by-frame
    #     ret, frame = cap.read()
    #
    #     # Our operations on the frame come here
    #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #
    #     # Display the resulting frame
    #     cv2.imshow('frame', gray)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #
    # # When everything done, release the capture
    # cap.release()
    # cv2.destroyAllWindows()
