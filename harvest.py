from PyQt5.QtWidgets import QApplication
from ft.window import MobDex
import json

class EternalHarvest(QApplication):

    def __init__(self, argv) -> None:
        super().__init__(argv)

        self.retrieve_paths()

        self.window: MobDex = MobDex(self.paths)

        self.signal_connection()
        self.window.show()

    def retrieve_paths(self) -> None:
        with open('paths.json', 'r') as file:
            self.paths: dict = json.load(file)

    def signal_connection(self) -> None:
        pass