from PySide2.QtWidgets import QLabel, QSizePolicy
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap


class IllustrationLabel(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setFixedSize(360, 101)

        self.setObjectName("IllustrationLabel")

        self.setPixmap(QPixmap("windows/images/illustration.png"))
