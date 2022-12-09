from PyQt5.QtWidgets import QLabel, QGroupBox, QFrame, QMdiArea, QMdiSubWindow,\
    QLayout, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import QEvent, QRect, QPoint, QMargins, Qt, QSize, pyqtSignal
from math import ceil
from itertools import count

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
    text_style: str, click_back_path: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.non_hover_back: QPixmap = QPixmap(background_path)
        self.hover_back: QPixmap = QPixmap(hover_path)
        self.click_back: QPixmap = QPixmap(click_back_path)
        self.setPixmap(self.non_hover_back)
        self.setFixedSize(w, h)
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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton: self.setPixmap(self.click_back)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.setPixmap(self.hover_back)
        return super().mouseReleaseEvent(event)


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


class TabLabel(QLabel):

    tab_index = count(0, 1)

    def get_active(self) -> bool: return self._active
    def set_active(self, state: bool) -> None:
        if state:
            self.setPixmap(self.im_selected_normal)
            self._active = state
        else:
            self.setPixmap(self.im_disabled_normal)
            self._active = state
    active = property(get_active, set_active)

    def __init__(self, pt_disabled_normal: str, pt_disabled_pressed: str,
    pt_selected_normal: str, pt_selected_over: str, pt_selected_pressed: str,
    tab_w: int, tab_h: int, sg_tab_click: pyqtSignal, **kwargs) -> None:
        super().__init__(**kwargs)
        self._active: bool = False
        self.sg_point: pyqtSignal = sg_tab_click
        self.setFixedSize(tab_w, tab_h)
        self.setScaledContents(True)
        self.create_pixmaps(pt_disabled_normal, pt_disabled_pressed,
        pt_selected_normal, pt_selected_over, pt_selected_pressed)
        self.setPixmap(self.im_disabled_normal)
        self._id = next(self.tab_index)
        self.create_text()

    def create_text(self) -> None:
        self.tab_text: QLabel = QLabel()
        hor_box: QHBoxLayout = QHBoxLayout()
        hor_box.addStretch()
        hor_box.addWidget(self.tab_text)
        hor_box.addStretch()
        self.setLayout(hor_box)

    def setTabText(self, txt: str) -> None:
        self.tab_text.setText(txt)
        self.tab_text.repaint()

    def create_pixmaps(self, disabled_normal: str, disabled_pressed: str,
    selected_normal: str, selected_over: str, selected_pressed: str) -> None:
        self.im_disabled_normal: QPixmap = QPixmap(disabled_normal)
        self.im_disabled_pressed: QPixmap = QPixmap(disabled_pressed)
        self.im_selected_normal: QPixmap = QPixmap(selected_normal)
        self.im_selected_over: QPixmap = QPixmap(selected_over)
        self.im_selected_pressed: QPixmap = QPixmap(selected_pressed)

    def change_state(self) -> None:
        self.active = not self.active

    def enterEvent(self, event: QEvent) -> None:
        if self.active: self.setPixmap(self.im_selected_over)
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        if self.active: self.setPixmap(self.im_selected_normal)
        return super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.active: self.setPixmap(self.im_selected_pressed)
        else: self.setPixmap(self.im_disabled_pressed)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.active: self.setPixmap(self.im_selected_over)
        else: self.sg_point.emit(self._id)
        return super().mouseReleaseEvent(event)

class HudBox(QLabel):

    def __init__(self, pt_icon: str, pt_back: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.setPixmap(QPixmap(pt_back))
        self.setScaledContents(True)
        self.setFixedWidth(260)
        self.init_gui(pt_icon)

    def init_gui(self, pt_icon) -> None:
        # Icon
        icon_map: QPixmap = QPixmap(pt_icon)
        icon: QLabel = QLabel()
        icon.setPixmap(icon_map)
        icon.setFixedSize(25, 25)
        icon.setScaledContents(True)

        # Text
        self.title: QLabel = QLabel()

        # Content
        self.content_box: QFrame = QFrame()

        # Layouts
        
        title_layout: QHBoxLayout = QHBoxLayout()
        title_layout.addWidget(icon, 0)
        title_layout.addWidget(self.title, 0)
        title_layout.addStretch(1)

        box_layout: QVBoxLayout = QVBoxLayout()
        box_layout.addLayout(title_layout, 0)
        box_layout.addWidget(self.content_box)
        self.setLayout(box_layout)

    def setContent(self, box: QLayout) -> None:
        self.content_box.setLayout(box)

    def setBoxTitle(self, title: str) -> None:
        self.title.setText(title)
        self.title.repaint()