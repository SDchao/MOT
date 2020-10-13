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
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setMinimumSize(100, 200)

        self.setObjectName("MapLabel")

    def resizeEvent(self, event: QResizeEvent):
        if self.raw_pixmap:
            self.set_avatar(self.raw_pixmap)

    def set_avatar(self, avatar_path: QPixmap) -> None:
        pixmap = QPixmap(avatar_path)
        self.raw_pixmap = pixmap
        new_pixmap = pixmap.scaled(self.width(), self.height(),
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(new_pixmap)
        self.setMinimumSize(new_pixmap.size())
