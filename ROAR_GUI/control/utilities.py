from PyQt5 import QtWidgets  # type: ignore
from PyQt5.QtWidgets import QApplication  # type: ignore
from pathlib import Path
import logging
from abc import abstractmethod
from pydantic import BaseModel


class BaseWindow(QtWidgets.QMainWindow):
    def __init__(
            self,
            app: QApplication,
            UI,
            show=True,
    ):
        """
        Args:
            app: QApplication
            UI: a callable that represents a class. ex: Ui_MainWindow in view/mainwindow_ui.py
        """
        super().__init__()
        self.logger = logging.getLogger(str(self.__class__))
        self.app = app
        self.ui = UI()
        try:
            self.ui.setupUi(self)
        except AttributeError:
            raise AttributeError(
                "Given UI {} does not have setupUi function. Please see documentation".format(
                    UI,
                ),
            )
        self.set_listener()
        if show:
            self.show()

    @abstractmethod
    def set_listener(self):
        self.ui.actionQuit.triggered.connect(self.close)


class PydanticModelEntry(BaseModel):
    title: str
    default: str
    type: str
