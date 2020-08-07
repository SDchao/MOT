from PySide2.QtWidgets import QLabel


class MapLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setScaledContents(True)
