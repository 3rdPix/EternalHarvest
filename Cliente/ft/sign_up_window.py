from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QGridLayout,\
    QPushButton, QComboBox
from PyQt5.QtGui import QIcon
import json
from os.path import join


class SignUpWindow(QWidget):

    def __init__(self, program_paths: dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self.paths = program_paths.get('front')
        self.self_settings()
        self.init_gui()
        self.lang_init()

    def self_settings(self) -> None:
        path: str = join(*self.paths.get('preset_window'))
        with open(path, 'r') as par: self.setting: dict = json.load(par)
        self.setted_lang: str = self.setting.get('language')
        path: str = join(
            *self.paths.get('languages').get(self.setted_lang))
        with open(path, 'r', encoding='utf-8') as file:
            self.text: dict = json.load(file)

    def init_gui(self) -> None:
        self.advice_label: QLabel = QLabel()
        self.advice_label.setWordWrap(True)

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

        self.user_label: QLabel = QLabel()
        self.user_textbox: QLineEdit = QLineEdit()

        self.pass_label: QLabel = QLabel()
        self.pass_textbox: QLineEdit = QLineEdit()
        self.pass_textbox.setEchoMode(QLineEdit.Password)

        self.enter_button: QPushButton = QPushButton()

        # Containers
        grid: QGridLayout = QGridLayout()
        grid.addWidget(self.advice_label, 1, 1, 1, 2)
        grid.addWidget(self.lang_selec, 1, 3)
        grid.addWidget(self.user_label, 2, 1)
        grid.addWidget(self.user_textbox, 2, 2, 1, 2)
        grid.addWidget(self.pass_label, 3, 1)
        grid.addWidget(self.pass_textbox, 3, 2, 1, 2)
        grid.addWidget(self.enter_button, 4, 2)
        self.setLayout(grid)

    def lang_init(self) -> None:
        self.advice_label.setText(self.text.get('log_in').get('advice'))
        self.user_label.setText(self.text.get('log_in').get('user'))
        self.pass_label.setText(self.text.get('log_in').get('pass'))
        self.enter_button.setText(self.text.get('log_in').get('enter'))