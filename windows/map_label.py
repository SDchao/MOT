from PySide2.QtWidgets import QLabel, QSizePolicy
from PySide2.QtGui import QPixmap, QResizeEvent, QPaintEvent, QPainter, QPen
from PySide2.QtCore import Qt, QPoint
from operators.convertor import str_2_point


class MapLabel(QLabel):
    now_pos: QPoint = None
    aspect_ratio = 0.5
    raw_pixmap: QPixmap = None
    all_pos: list = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setMinimumSize(500, 500)

    def resizeEvent(self, event: QResizeEvent):
        if self.raw_pixmap:
            self.set_map(self.raw_pixmap)

    def set_map(self, map_path: QPixmap, all_pos: list = None) -> None:
        pixmap = QPixmap(map_path)
        self.raw_pixmap = pixmap
        self.setPixmap(pixmap.scaled(self.width(), self.height(),
                                     Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if all_pos:
            self.all_pos = []
            for pos in all_pos:
                self.all_pos.append(str_2_point(pos))

    def paintEvent(self, event: QPaintEvent):
        super(MapLabel, self).paintEvent(event)
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(20)
        pen.setColor(Qt.blue)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        for pos in self.all_pos:
            self.__draw_point(pos, painter)

        if self.now_pos:
            # 计算真正的绘图坐标
            pen.setColor(Qt.red)
            painter.setPen(pen)
            self.__draw_point(self.now_pos, painter)

    def __draw_point(self, point: QPoint, painter: QPainter):
        raw_size = self.raw_pixmap.size()
        now_size = self.pixmap().size()

        k_w = now_size.width() / raw_size.width()
        k_h = now_size.height() / raw_size.height()

        pos = QPoint(point.x() * k_w, point.y() * k_h)
        painter.drawPoint(pos)

    def set_now_pos(self, pos: QPoint = None):
        self.now_pos = pos
        self.update()
