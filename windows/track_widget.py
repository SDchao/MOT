from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QPalette, QPaintEvent, QPen, QPainter
from typing import List, Dict


class TrackWidget(QWidget):
    track_points: Dict[int, List] = {}
    final_points: Dict[int, QPoint] = {}
    colors = [Qt.green, Qt.red, Qt.darkYellow, Qt.blue]
    background_color = Qt.blue

    kw = 1
    kh = 1

    def __init__(self, w, h, raw_w, raw_h):
        super().__init__()

        self.setMinimumSize(w, h)
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

        pen.setColor(Qt.white)
        painter.setPen(pen)
        painter.fillRect(0, 0, self.width(), self.height(), self.background_color)
        painter.drawRect(0, 0, self.width() - 3, self.height() - 3)

        index = 0
        pen.setWidth(10)
        for key in self.track_points.keys():
            last_point = None
            color = self.colors[index % len(self.colors)]
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

    def add_points(self, point_dict: Dict[int, QPoint]):
        for (key, point) in self.final_points.items():
            if key in self.track_points.keys():
                self.track_points[key].append(point)
            else:
                self.track_points[key] = [point]

        self.final_points = {}

        for (key, new_point) in point_dict.items():
            new_point.setX(new_point.x() * self.kw)
            new_point.setY(new_point.y() * self.kh)
            self.final_points[key] = new_point

        self.update()

    def clear(self):
        self.track_points = {}
        self.final_points = {}
