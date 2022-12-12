from PyQt5.QtCore import QObject, pyqtSignal


class WindowSignals(QObject):

    sg_show_sign_up_window = pyqtSignal()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)