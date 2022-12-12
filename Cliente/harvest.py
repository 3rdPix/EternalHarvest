from PyQt5.QtWidgets import QApplication
from ft.main_window import WindowVisual
from ft.sign_up_window import SignUpWindow
import json

class EternalHarvest(QApplication):

    def __init__(self, argv) -> None:
        super().__init__(argv)

        self.retrieve_paths()

        self.window: WindowVisual = WindowVisual(self.paths)
        self.log_in: SignUpWindow = SignUpWindow(self.paths)

        self.signal_connection()
        self.log_in.show()

    def retrieve_paths(self) -> None:
        with open('paths.json', 'r') as file:
            self.paths: dict = json.load(file)

    def signal_connection(self) -> None:
        pass