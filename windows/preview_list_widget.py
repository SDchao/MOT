from PySide2.QtCore import QSize
from PySide2.QtWidgets import QListView, QListWidget

class Preview_List_Widget(QListWidget):
    def __init__(self):
        QListWidget.__init__(self)
        self.setFlow(QListView.LeftToRight)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(100, 100))
    