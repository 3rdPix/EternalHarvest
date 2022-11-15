from PyQt5.QtWidgets import QLabel, QGroupBox, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QEvent
from math import ceil


class MobLabel(QLabel):

    def __init__(self, pt: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_image(pt)

    def set_image(self, pt: str) -> None:
        image: QPixmap = QPixmap(pt)
        self.setPixmap(image)
        self.setScaledContents(True)

    def set_base_size(self) -> None:
        self.ex_width = self.width()
        self.ex_height = self.height()

    def enterEvent(self, event: QEvent) -> None:
        center_point = self.geometry().center()
        new_width = ceil(self.ex_width * 1.2)
        new_height = ceil(self.ex_height * 1.2)
        self.resize(new_width, new_height)
        sillhouette = self.frameGeometry()
        sillhouette.moveCenter(center_point)
        self.move(sillhouette.topLeft())
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        center_point = self.geometry().center()
        self.resize(self.ex_width, self.ex_height)
        sillhouette = self.frameGeometry()
        sillhouette.moveCenter(center_point)
        self.move(sillhouette.topLeft())
        return super().leaveEvent(event)

class MobBox(QGroupBox):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def set_base_size(self) -> None:
        self.ex_width = self.width()
        self.ex_height = self.height()

    def enterEvent(self, event: QEvent) -> None:
        center_point = self.geometry().center()
        new_width = ceil(self.ex_width * 1.1)
        new_height = ceil(self.ex_height * 1.1)
        self.resize(new_width, new_height)
        sillhouette = self.frameGeometry()
        sillhouette.moveCenter(center_point)
        self.move(sillhouette.topLeft())
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        center_point = self.geometry().center()
        self.resize(self.ex_width, self.ex_height)
        sillhouette = self.frameGeometry()
        sillhouette.moveCenter(center_point)
        self.move(sillhouette.topLeft())
        return super().leaveEvent(event)