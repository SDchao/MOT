from PySide2.QtCore import QSize
from PySide2.QtWidgets import QListView, QListWidget, QListWidgetItem, QSizePolicy
from PySide2.QtCore import Qt

from operators.motlogging import logger
from windows.preview_item import PreviewItem


class PreviewListWidget(QListWidget):
    def __init__(self):
        QListWidget.__init__(self)
        self.setFlow(QListView.LeftToRight)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(150, 150))
        self.setWrapping(False)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        # self.setMinimumWidth(500)
        self.setFixedHeight(130)
        self.setSpacing(2)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMovement(QListView.Static)

    def insert_item(self, item: PreviewItem):
        self.addItem(item)
        logger.info("Found video: " + item.video_path)
