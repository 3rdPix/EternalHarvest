from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGroupBox, QLabel,\
    QMdiArea, QFrame, QHBoxLayout, QListWidget, QListView, QScrollArea
from PyQt5.QtGui import QPixmap, QCloseEvent
from PyQt5.QtCore import Qt, QRect
from ft.custom_elements import MobLabel, MobBox, MobMdi, FlowLayout, CellBox
import json
from os.path import join
import requests


class MobDex(QWidget):

    def __init__(self, program_paths: dict) -> None:
        super().__init__()
        self.paths = program_paths.get('front')
        self.self_settings()
        self.init_gui()

        #MUST DELETE
        # self.test_set3()
    
    def self_settings(self) -> None:
        
        """
        Window's geometry is saved each time the app is opened, reopening the
        app with the size and position from last session
        """
        path: str = join(*self.paths.get('preset_window'))
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
            *self.paths.get('languages').get(setted_lang))
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
            marco.set_style()
            lay.addWidget(marco)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        transition_w = QWidget()
        transition_w.setLayout(lay)
        scroll.setWidget(transition_w)
        transition_l = QHBoxLayout()
        transition_l.addWidget(scroll)
        self.setLayout(transition_l)

    def init_gui(self) -> None:
        panel: QScrollArea = self.create_scroll_area()

        # delete
        transition = QHBoxLayout()
        transition.addWidget(panel)
        self.setLayout(transition)

    def create_scroll_area(self) -> QScrollArea:
        area: QScrollArea = QScrollArea()
        area.setWidgetResizable(True)
        flow_container: FlowLayout = FlowLayout()
        with open('arch.json', 'r') as file: ARCHIS = json.load(file)
        
        pt_cell_style: list = self.paths.get('css').get('cell')
        with open(join(*pt_cell_style), 'r') as file: cell_css = file.read()
        pt_sprite_archs: list = self.paths.get('arch')
        pt_style_par = self.paths.get('styling_par')
        with open(join(*pt_style_par), 'r') as file: 
            sty_par: dict = json.load(file)
        cell_w, cell_h = sty_par.get('widgets').get('cell_dimensions')
        cell_background_path: str = join(*self.paths.get('background_im').\
            get('cell'))
        cell_background_on_path: str = join(*self.paths.get('background_im').\
            get('on_cell'))
        with open(join(*self.paths.get('css').get('cell_text')), 'r') as file:
            cell_text_css: str = file.read()
        for archi in ARCHIS:
            mob_id: int = archi.get('_id')
            image_path: str = join(*(pt_sprite_archs + [f'{mob_id}.png']))
            cell = CellBox(image_path=image_path, name=archi.get('name'),
            w=cell_w, h=cell_h, cell_style=cell_css,
            background_path=cell_background_path,
            hover_path=cell_background_on_path, text_style=cell_text_css)
            flow_container.addWidget(cell)
        
        transition = QWidget()
        transition.setLayout(flow_container)
        area.setWidget(transition)
        return area

    def create_cell(self, archi: dict, css: str, pt_sprite: list,
                w: int, h: int) -> MobBox:
        arch_id = archi.get('_id')
        pt_img = pt_sprite + [f'{arch_id}.png']
        
        new_cell: MobBox = MobBox(join(*pt_img), title=archi.get('name'))
        new_cell.setStyleSheet(css)
        new_cell.setFixedSize(w, h)
        return new_cell
        

    def closeEvent(self, event: QCloseEvent) -> None:
        sillhouette = self.geometry().getRect()
        self.setting['geometry'] = sillhouette
        path: str = join(*self.paths.get('preset_window'))
        with open(path, 'w') as par: json.dump(self.setting, par)
        return super().closeEvent(event)