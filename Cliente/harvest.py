from PyQt5.QtWidgets import QApplication
from ft.main_window import WindowVisual
from ft.sign_up_window import SignUpWindow
from bk.window_bk import WindowLogic
import json

class EternalHarvest(QApplication):

    def __init__(self, argv) -> None:
        super().__init__(argv)

        self.retrieve_paths()

        self.logic: WindowLogic = WindowLogic(self.paths)
        
        self.window: WindowVisual = WindowVisual(self.paths)
        self.log_in: SignUpWindow = SignUpWindow(self.paths)

        self.signal_connection()
        self.logic.log_to_server()

    def retrieve_paths(self) -> None:
        with open('paths.json', 'r') as file:
            self.paths: dict = json.load(file)

    def signal_connection(self) -> None:
        self.logic.sg_show_sign_up_window.connect(
            self.log_in.show)
        
        self.log_in.signal_button_enter.connect(
            self.logic.create_user)