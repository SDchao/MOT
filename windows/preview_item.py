from PySide2.QtWidgets import QListWidgetItem
from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon, QPixmap, QImage


class PreviewItem(QListWidgetItem):
    video_path: str

    def __init__(self, name: str, icon: QImage, video_path: str, size: QSize = None):
        show_name = name
        if len(name) > 15:
            show_name = name[:15] + "..."

        super().__init__(show_name)
        self.setIcon(QIcon(QPixmap.fromImage(icon)))
        self.setToolTip(name)
        self.video_path = video_path
        if size:
            self.setSizeHint(size)
        else:
            self.setSizeHint(QSize(300, 150))
