from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel, QSizePolicy


class IllustrationLabel(QLabel):

    def __init__(self, width, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setFixedSize(width, width / 360 * 101)
        self.setObjectName("IllustrationLabel")

        self.setPixmap(QPixmap("windows/images/illustration.png").scaled(QSize(width, width / 360 * 101)))
