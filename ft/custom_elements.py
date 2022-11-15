from PyQt5.QtWidgets import QLabel, QGroupBox, QFrame, QMdiArea, QMdiSubWindow,\
    QLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QEvent, QRect, QPoint, QMargins, Qt, QSize
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

class MobMdi(QMdiArea):
    def fixGeometry(self, window, viewGeo):
        winGeo = window.geometry()
        if not viewGeo.contains(winGeo):
            if winGeo.right() > viewGeo.right():
                winGeo.moveRight(viewGeo.right())
            if winGeo.x() < 0:
                winGeo.moveLeft(0)
            if winGeo != window.geometry():
                window.setGeometry(winGeo)
                return True
        return False

    def eventFilter(self, obj, event):
        if (event.type() == event.Move and 
            isinstance(obj, QMdiSubWindow) and
            self.fixGeometry(obj, self.viewport().geometry())):
                return True
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        viewGeo = self.viewport().geometry()
        for win in self.subWindowList():
            self.fixGeometry(win, viewGeo)

    def order(self) -> None:
        list = self.subWindowList()
        print(list)


# This class was taken from Qt Documentation
class FlowLayout(QLayout):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._item_list = []

    def __del__(self):
        item = self.takeAt(0)
        while item: item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list): return self._item_list[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list): return self._item_list.pop(index)
        return None

    def expandingDirections(self): return Qt.Orientation(0)

    def hasHeightForWidth(self): return True

    def heightForWidth(self, width):
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self): return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())
        size += QSize(
            2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()
        for item in self._item_list:
            space_x = spacing
            space_y = spacing
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = next_x
            line_height = max(line_height, item.sizeHint().height())
        return y + line_height - rect.y()