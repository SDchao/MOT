from typing import List, Dict

from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QPaintEvent, QPen, QPainter, QColor
from PySide2.QtWidgets import QWidget


class TrackWidget(QWidget):
    track_points: Dict[int, List] = {}
    final_points: Dict[int, QPoint] = {}
    colors: Dict[int, QColor] = {}
    background_color = Qt.blue

    kw = 1
    kh = 1

    def __init__(self, w, h, raw_w, raw_h):
        super().__init__()

        self.setFixedSize(w, h)
        self.kw = w / raw_w
        self.kh = h / raw_h

        # pal = QPalette()
        # pal.setColor(QPalette.Background, Qt.blue)
        self.setAutoFillBackground(True)
        # self.setPalette(pal)

        self.setObjectName("TrackWidget")

    def paintEvent(self, event: QPaintEvent):
        super(TrackWidget, self).paintEvent(event)
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)
        painter.fillRect(0, 0, self.width(), self.height(), self.background_color)

        index = 0
        pen.setWidth(10)
        for key in self.track_points.keys():
            last_point = None
            color = self.colors[key]
            pen.setColor(color)
            painter.setPen(pen)
            for point in self.track_points[key]:
                if last_point:
                    painter.drawLine(last_point, point)
                else:
                    painter.drawPoint(point)
                last_point = point
            index += 1
        pen.setColor(Qt.red)
        pen.setWidth(20)
        painter.setPen(pen)

        for point in self.final_points.values():
            painter.drawPoint(point)

    def add_points(self, point_dict: Dict[int, List]):
        for (key, point) in self.final_points.items():
            if key in self.track_points.keys():
                self.track_points[key].append(point)
            else:
                self.track_points[key] = [point]

        self.final_points = {}

        for (key, info) in point_dict.items():
            info[0].setX(info[0].x() * self.kw)
            info[0].setY(info[0].y() * self.kh)
            self.final_points[key] = info[0]
            self.colors[key] = info[1]

        self.update()

    def clear(self):
        self.track_points = {}
        self.final_points = {}
        self.colors = {}
