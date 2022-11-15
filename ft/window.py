from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGroupBox, QLabel,\
    QMdiArea, QFrame, QHBoxLayout, QListWidget, QListView, QScrollArea
from PyQt5.QtGui import QPixmap, QCloseEvent
from PyQt5.QtCore import Qt, QRect
from ft.custom_elements import MobLabel, MobBox, MobMdi, FlowLayout
import json
from os.path import join


class MobDex(QWidget):

    def __init__(self, program_paths: dict) -> None:
        super().__init__()
        self.paths = program_paths
        self.self_settings()
        self.init_gui()

        #MUST DELETE
        self.test_set3()
    
    def self_settings(self) -> None:
        
        """
        Window's geometry is saved each time the app is opened, reopening the
        app with the size and position from last session
        """
        path: str = join(*self.paths.get('front').get('preset_window'))
        with open(path, 'r') as par: self.setting: dict = json.load(par)
        geometry: list = self.setting.get('geometry')
        rect: QRect = QRect(*geometry)
        self.setGeometry(rect)

        """
        Reads the language setted in the app, then retrieves all the data
        containing the text
        """
        setted_lang: str = self.setting.get('language')
        path: str = join(
            *self.paths.get('front').get('languages').get(setted_lang))
        with open(path, 'r') as file: self.text: dict = json.load(file)

        """
        Setting window's presentation
        """
        title: str = self.text.get('window_title')
        self.setWindowTitle(title)

    def test_set3(self) -> None:
        lay = FlowLayout()
        for i in range(286):
            marco = MobBox(title=str(i))
            marco.setMinimumSize(100, 120)
            marco.resize(marco.minimumSize())
            marco.set_base_size()
            lay.addWidget(marco)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        transition_w = QWidget()
        transition_w.setLayout(lay)
        scroll.setWidget(transition_w)
        transition_l = QHBoxLayout()
        transition_l.addWidget(scroll)
        self.setLayout(transition_l)
        pass

    def init_gui(self) -> None:
        
        pass

    def closeEvent(self, event: QCloseEvent) -> None:
        sillhouette = self.frameGeometry().getRect()
        self.setting['geometry'] = sillhouette
        path: str = join(*self.paths.get('front').get('preset_window'))
        with open(path, 'w') as par: json.dump(self.setting, par)
        return super().closeEvent(event)