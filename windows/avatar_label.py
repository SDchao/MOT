from PySide2.QtWidgets import QLabel, QSizePolicy
from PySide2.QtGui import QPixmap, QResizeEvent
from PySide2.QtCore import Qt, QPoint


class AvatarLabel(QLabel):
    now_pos: QPoint = None
    aspect_ratio = 0.5
    raw_pixmap: QPixmap = None
    all_pos: list = []

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignCenter)
        self.setMaximumSize(100, 300)
        self.setMinimumSize(50, 150)

        self.setObjectName("AvatarLabel")
        self.set_avatar("data/group1/image/1/c1_10_682_94_47_144_10.jpg")

    def resizeEvent(self, event: QResizeEvent):
        if self.raw_pixmap:
            self.set_avatar(self.raw_pixmap)

    def set_avatar(self, avatar_path: str) -> None:
        pixmap = QPixmap(avatar_path)
        self.raw_pixmap = pixmap
        new_pixmap = pixmap.scaled(self.width(), self.height(),
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(new_pixmap)
        self.setMaximumSize(new_pixmap.size())
