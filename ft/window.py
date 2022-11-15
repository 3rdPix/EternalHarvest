from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGroupBox, QLabel
from PyQt5.QtGui import QPixmap
from ft.custom_elements import MobLabel, MobBox
import json
from os.path import join


class MobDex(QWidget):

    def __init__(self, program_paths: dict) -> None:
        super().__init__()
        self.paths = program_paths
        self.self_settings()
        self.init_gui()
    
    def self_settings(self) -> None:
        
        """
        Windows' geometry is saved each time the app is opened, reopening the
        app with the size and position from last session
        """
        path: str = join(*self.paths.get('front').get('styling_par'))
        with open(path, 'r') as par: setting: dict = json.load(par)
        geometry: list = setting.get('window').get('geometry')
        self.setGeometry(*geometry)

        """
        Reads the language setted in the app, then retrieves all the data
        containing the text in string format
        """
        setted_lang: str = setting.get('window').get('language')
        

        pass

    def init_gui(self) -> None:
        
        pass