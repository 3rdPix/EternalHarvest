from PyQt5.QtWidgets import QLabel, QGroupBox, QFrame, QMdiArea, QMdiSubWindow,\
    QLayout, QVBoxLayout, QHBoxLayout, QGridLayout
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

    def __init__(self, pt: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.setMouseTracking(True)
        self.create_image(pt)

    def create_image(self, pt: str) -> None:
        self.mob = QLabel(parent=self)
        image = QPixmap(pt)
        self.mob.setPixmap(image)
        self.mob.setScaledContents(True)
        grid = QGridLayout()
        grid.addWidget(self.mob, 1, 1)
        self.setLayout(grid)
        # self.set_sizes()

    def set_sizes(self) -> None:
        base_x: int = self.mob.width()
        base_y: int = self.mob.height()
        self.base_mob_size = QSize(base_x, base_y)
        self.expa_mob_size = QSize(ceil(base_x * 1.1), ceil(base_y * 1.1))

    def enterEvent(self, event: QEvent) -> None:
        self.mob.resize(self.expa_mob_size)
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.mob.resize(self.base_mob_size)
        return super().leaveEvent(event)


class CellBox(QLabel):

    def __init__(self, image_path: str, name: str, w: int, h: int,
    cell_style: str, background_path: str, hover_path: str,
    text_style: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.non_hover_back: QPixmap = QPixmap(background_path)
        self.hover_back: QPixmap = QPixmap(hover_path)
        self.setPixmap(self.non_hover_back)
        self.setMinimumSize(w, h)
        self.setStyleSheet(cell_style)
        self.setScaledContents(True)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.set_content(image_path, name, text_style)

    def set_content(self, image_path: str, name: str, style: str) -> None:
        mob_label: QLabel = QLabel(parent=self)
        mob_image: QPixmap = QPixmap(image_path)
        mob_label.setPixmap(mob_image)
        mob_label.setScaledContents(True)

        name_label: QLabel = QLabel(parent=self, text=name)
        name_label.setWordWrap(True)
        name_label.setStyleSheet(style)

        self.setLayout(hpad_this(
            mob_label,
            name_label
        ))

    def enterEvent(self, event: QEvent) -> None:
        self.setPixmap(self.hover_back)
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.setPixmap(self.non_hover_back)
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

def hpad_this(*args) -> QVBoxLayout:
        padded_boxes: list = list()
        layout = QVBoxLayout()
        for widget in args:
            local_pad = QHBoxLayout()
            local_pad.addStretch()
            if type(widget) == type(args):
                for each in widget: local_pad.addWidget(each)
            elif type(widget) == type(QVBoxLayout) or\
                type(widget) == type(QHBoxLayout):
                local_pad.addLayout(widget)
            else: local_pad.addWidget(widget)
            local_pad.addStretch()
            padded_boxes.append(local_pad)
        for box in padded_boxes:
            layout.addStretch()
            layout.addLayout(box)
        layout.addStretch()
        return layout