from PySide2.QtWidgets import QLabel, QSizePolicy
from PySide2.QtGui import QPixmap, QResizeEvent, QPaintEvent, QPainter, QPen
from PySide2.QtCore import Qt, QPoint


class MapLabel(QLabel):
    now_pos: QPoint = None
    aspect_ratio = 0.5
    raw_pixmap: QPixmap = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def resizeEvent(self, event: QResizeEvent):
        if self.raw_pixmap:
            self.set_map(self.raw_pixmap)

    def set_map(self, pixmap: QPixmap) -> None:
        self.raw_pixmap = pixmap
        self.setPixmap(pixmap.scaled(self.width(), self.height(),
                                     Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def paintEvent(self, event: QPaintEvent):
        super(MapLabel, self).paintEvent(event)
        if self.now_pos:
            # 计算真正的绘图坐标
            raw_size = self.raw_pixmap.size()
            now_size = self.pixmap().size()

            k_w = now_size.width() / raw_size.width()
            k_h = now_size.height() / raw_size.height()

            pos = QPoint(self.now_pos.x() * k_w, self.now_pos.y() * k_h)
            painter = QPainter(self)
            pen = QPen()
            pen.setWidth(20)
            pen.setColor(Qt.red)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.drawPoint(pos)

    def set_now_pos(self, pos: QPoint = None):
        self.now_pos = pos
        self.update()
