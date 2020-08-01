from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QPalette
import random


class PaintBoard(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setPalette(Qt.transparent)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.red)
        painter.drawRect(random.randint(1, 700), random.randint(
            1, 700), random.randint(1, 700), random.randint(1, 700))
