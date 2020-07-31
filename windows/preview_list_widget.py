from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import QListView, QListWidget, QListWidgetItem, QSizePolicy, QAbstractItemView
from PySide2.QtGui import QIcon
from typing import List


class Preview_List_Widget(QListWidget):
    def __init__(self):
        QListWidget.__init__(self)
        self.setFlow(QListView.LeftToRight)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(100, 100))
        self.setWrapping(False)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.setMinimumWidth(500)
        self.setFixedHeight(150)
        self.setSpacing(10)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMovement(QListView.Static)

    def insert_item(self, img_list: List):
        """Insert serveral image items into ListView

        Args:
            byteImgList (List): Image List contains image bytes
        """
        for img in img_list:
            item = QListWidgetItem("Default")
            item.setIcon(QIcon(img))
            self.addItem(item)
