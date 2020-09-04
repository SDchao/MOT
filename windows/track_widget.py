from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QPalette, QPaintEvent, QPen, QPainter
from typing import List


class TrackWidget(QWidget):
    track_points = []
    final_points = []

    kw = 1
    kh = 1

    def __init__(self, w, h, raw_w, raw_h):
        super().__init__()

        self.setMinimumSize(w, h)
        self.kw = w / raw_w
        self.kh = h / raw_h

        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.darkBlue)
        self.setAutoFillBackground(True)
        self.setPalette(pal)

    def paintEvent(self, event: QPaintEvent):
        super(TrackWidget, self).paintEvent(event)
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(5)
        pen.setColor(Qt.yellow)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        last_point: QPoint = None
        for point in self.track_points:
            if last_point:
                painter.drawLine(last_point, point)
            else:
                painter.drawPoint(point)
            last_point = point

        pen.setColor(Qt.red)
        pen.setWidth(20)
        painter.setPen(pen)

        for point in self.final_points:
            painter.drawPoint(point)

    def add_points(self, point_list: List[QPoint]):
        for old_final_point in self.final_points:
            self.track_points.append(old_final_point)

        self.final_points = []

        for new_final_point in point_list:
            new_final_point.setX(new_final_point.x() * self.kw)
            new_final_point.setY(new_final_point.y() * self.kh)
            self.final_points.append(new_final_point)

        self.update()

    def clear(self):
        self.track_points = []
        self.final_points = []
