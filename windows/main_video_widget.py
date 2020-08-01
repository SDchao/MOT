from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QGraphicsView
from PySide2.QtGui import QPainter
from PySide2.QtCore import Qt, QRect


class MainVideoWidget(QVideoWidget):
    def __init__(self):
        QVideoWidget.__init__(self)

    def paintEvent(self, event):
        QVideoWidget.paintEvent(event)
        print("Ok")
        painter = QPainter(self)
        painter.drawRect(QRect(10, 20, 300, 400))
        
