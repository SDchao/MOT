from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QPalette

class PaintBoard(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setPalette(Qt.transparent)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.red)
        painter.drawRect(1,1,100,100)