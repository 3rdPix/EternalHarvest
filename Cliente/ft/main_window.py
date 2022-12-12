from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGroupBox, QLabel,\
    QMdiArea, QFrame, QHBoxLayout, QListWidget, QListView, QScrollArea,\
    QTabWidget, QLineEdit, QProgressBar, QVBoxLayout, QGridLayout, QComboBox,\
        QSizePolicy, QStyle, QStackedLayout
from PyQt5.QtGui import QPixmap, QCloseEvent, QIcon
from PyQt5.QtCore import Qt, QRect, QSize, pyqtSignal
from ft.custom_elements import MobLabel, MobBox, FlowLayout, CellBox,\
    TabLabel, hpad_this, HudBox
import json
from os.path import join
import requests


class WindowVisual(QWidget):

    sg_tab_clicked = pyqtSignal(int)

    def __init__(self, program_paths: dict) -> None:
        super().__init__()
        self.paths = program_paths.get('front')
        self.self_settings()
        self.init_gui()
        self.stylize_gui()
        self.lang_ize_gui()
        self.signal_connection()
    
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
        self.setted_lang: str = self.setting.get('language')
        path: str = join(
            *self.paths.get('languages').get(self.setted_lang))
        with open(path, 'r', encoding='utf-8') as file:
            self.text: dict = json.load(file)
        
        """
        Retrieves styling parameters
        """
        pt_style_par = self.paths.get('styling_par')
        with open(join(*pt_style_par), 'r') as file: 
            self.sty_par: dict = json.load(file)

    def init_gui(self) -> None:
        """
        Tabs
        """
        # Tabs navigator

        tab_w, tab_h = self.sty_par.get('widgets').get('tabs_dimensions')
        pt_dis_normal = join(
            *self.paths.get('background_im').get('t_dis_normal'))
        pt_dis_press = join(
            *self.paths.get('background_im').get('t_dis_press'))
        pt_sel_normal = join(
            *self.paths.get('background_im').get('t_sel_normal'))
        pt_sel_over = join(
            *self.paths.get('background_im').get('t_sel_over'))
        pt_sel_press = join(
            *self.paths.get('background_im').get('t_sel_pressed'))

        self.arch_tab_bt: TabLabel = TabLabel(
            pt_disabled_normal=pt_dis_normal,
            pt_disabled_pressed=pt_dis_press,
            pt_selected_normal=pt_sel_normal,
            pt_selected_over=pt_sel_over,
            pt_selected_pressed=pt_sel_press,
            tab_w=tab_w, tab_h=tab_h,
            sg_tab_click=self.sg_tab_clicked)
        self.arch_tab_bt.change_state() # archis selected by default

        self.boss_tab_bt: TabLabel = TabLabel(
            pt_disabled_normal=pt_dis_normal,
            pt_disabled_pressed=pt_dis_press,
            pt_selected_normal=pt_sel_normal,
            pt_selected_over=pt_sel_over,
            pt_selected_pressed=pt_sel_press,
            tab_w=tab_w, tab_h=tab_h,
            sg_tab_click=self.sg_tab_clicked)
        
        tab_bar_container: QHBoxLayout = QHBoxLayout()
        tab_bar_container.setContentsMargins(0, 0, 0, 0)
        tab_bar_container.addWidget(self.arch_tab_bt, 0)
        tab_bar_container.addWidget(self.boss_tab_bt, 0)
        tab_bar_container.addStretch(1)

        # Tabs content
        self.arch_scroll: QScrollArea = QScrollArea()
        self.boss_scroll: QScrollArea = QScrollArea()
        self.tab_content_container: QStackedLayout = QStackedLayout()
        self.tab_content_container.addWidget(self.arch_scroll)
        self.tab_content_container.addWidget(self.boss_scroll)
        self.tab_content_container.setCurrentIndex(0)

        """
        Boxes
        """
        pt_box_back = join(*self.paths.get('ill').get('box_back'))

        # Search box
        pt_im_search = join(*self.paths.get('ill').get('search_icon'))
        self.search_box: HudBox = HudBox(pt_im_search, pt_box_back)
        self.search_bar: QLineEdit = QLineEdit()
        search_container = QHBoxLayout()
        search_container.addWidget(self.search_bar)
        self.search_box.setContent(search_container)
        self.search_box.setFrameStyle(QFrame.Box | QFrame.Sunken)

        # Progress box
        pt_im_progress = join(*self.paths.get('ill').get('progress_icon'))
        self.progress_box: HudBox = HudBox(pt_im_progress, pt_box_back)
        
        self.arch_pro_name: QLabel = QLabel()
        self.arch_pro_bar: QProgressBar = QProgressBar()
        
        self.boss_pro_name: QLabel = QLabel()
        self.boss_pro_bar: QProgressBar = QProgressBar()

        self.gen_pro_name: QLabel = QLabel()
        self.gen_pro_bar : QProgressBar = QProgressBar()

        progress_container: QGridLayout = QGridLayout()        
        progress_container.addWidget(self.arch_pro_name, 1, 1)
        progress_container.addWidget(self.arch_pro_bar, 1, 2, 1, 2)
        progress_container.addWidget(self.boss_pro_name, 2, 1)
        progress_container.addWidget(self.boss_pro_bar, 2, 2, 1, 2)
        progress_container.addWidget(self.gen_pro_name, 3, 1)
        progress_container.addWidget(self.gen_pro_bar, 3, 2, 1, 2)
        self.progress_box.setContent(progress_container)
        self.progress_box.setFrameStyle(QFrame.Box | QFrame.Sunken)


        # Configurations
        pt_im_config = join(*self.paths.get('ill').get('setting_icon'))
        self.config_box: HudBox = HudBox(pt_im_config, pt_box_back)

        self.lang_selec_text: QLabel = QLabel()
        self.lang_selec: QComboBox = QComboBox()

        pt_im_spanish = join(*self.paths.get('lang_im').get('spanish'))
        spanish: QIcon = QIcon(pt_im_spanish)
        pt_im_english = join(*self.paths.get('lang_im').get('english'))
        english: QIcon = QIcon(pt_im_english)
        pt_im_french = join(*self.paths.get('lang_im').get('french'))
        french: QIcon = QIcon(pt_im_french)
        self.lang_selec.addItem(spanish, 'Español')
        self.lang_selec.addItem(english, 'English')
        self.lang_selec.addItem(french, 'Français')

        configuration_container: QHBoxLayout = QHBoxLayout()
        configuration_container.addWidget(self.lang_selec_text)
        configuration_container.addWidget(self.lang_selec)
        self.config_box.setContent(configuration_container)
        self.config_box.setFrameStyle(QFrame.Box | QFrame.Sunken)
        
        # #del
        full_container: QVBoxLayout = QVBoxLayout()
        full_container.setContentsMargins(0, 0, 0, 0)
        full_container.addLayout(tab_bar_container)
        full_container.addLayout(self.tab_content_container)

        right_panel: QVBoxLayout = QVBoxLayout()
        right_panel.addWidget(self.search_box)
        right_panel.addWidget(self.progress_box)
        right_panel.addWidget(self.config_box)

        win_container: QHBoxLayout = QHBoxLayout()
        win_container.addLayout(full_container, 1)
        win_container.addLayout(right_panel, 0)
        self.setLayout(win_container)

    def stylize_gui(self) -> None:
        self.setWindowIcon(QIcon(join(
            *self.paths.get('ill').get('window_icon'))))
        self.setWindowTitle(self.text.get('window_title'))

    def lang_ize_gui(self) -> None:
        self.arch_tab_bt.setTabText(self.text.get('arch_tab'))
        self.boss_tab_bt.setTabText(self.text.get('boss_tab'))
        self.search_box.setBoxTitle(self.text.get('search_box'))
        self.progress_box.setBoxTitle(self.text.get('progress_box'))
        self.config_box.setBoxTitle(self.text.get('config_box'))
        self.arch_pro_name.setText(self.text.get('arch_tab'))
        self.boss_pro_name.setText(self.text.get('boss_tab'))
        self.gen_pro_name.setText(self.text.get('general_pro'))
        self.lang_selec_text.setText(self.text.get('lang_selec'))

    def signal_connection(self) -> None:
        self.sg_tab_clicked.connect(
            self.change_active_tab)

    def change_active_tab(self, index: int) -> None:
        self.tab_content_container.setCurrentIndex(index)
        self.arch_tab_bt.change_state()
        self.boss_tab_bt.change_state()



    """
    unpure
    """

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
        cell_click_path: str = join(*self.paths.get('background_im').\
            get('cell_click'))
        with open(join(*self.paths.get('css').get('cell_text')), 'r') as file:
            cell_text_css: str = file.read()
        for archi in ARCHIS:
            mob_id: int = archi.get('_id')
            image_path: str = join(*(pt_sprite_archs + [f'{mob_id}.png']))
            cell = CellBox(image_path=image_path, name=archi.get('name'),
            w=cell_w, h=cell_h, cell_style=cell_css,
            background_path=cell_background_path, 
            hover_path=cell_background_on_path, text_style=cell_text_css,
            click_back_path=cell_click_path)
            flow_container.addWidget(cell)
        transition = QWidget()
        scroll_back = QPixmap(join(*self.paths.get('background_im').\
            get('big_back')))
        transition.setLayout(flow_container)
        area.setWidget(transition)
        return area


        
    def closeEvent(self, event: QCloseEvent) -> None:
        sillhouette = self.geometry().getRect()
        self.setting['geometry'] = sillhouette
        path: str = join(*self.paths.get('preset_window'))
        with open(path, 'w') as par: json.dump(self.setting, par)
        return super().closeEvent(event)