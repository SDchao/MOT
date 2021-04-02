import abc

from PySide2.QtWidgets import QWidget


class ModifierWidget(QWidget):
    file_filter = "*.*"

    def __init__(self):
        super(ModifierWidget, self).__init__()
        self.setFixedSize(1280, 720)

    @abc.abstractmethod
    def open(self, file_path: str):
        pass

    @abc.abstractmethod
    def save(self, save_path: str):
        pass
