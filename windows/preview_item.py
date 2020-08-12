from PySide2.QtWidgets import QListWidgetItem
from PySide2.QtCore import QSize, QPoint
from PySide2.QtGui import QIcon, QPixmap, QImage
from operators.video_operator import VideoInfo


class PreviewItem(QListWidgetItem):
    video_path: str
    map_pos: QPoint
    fps: float
    video_size: QSize

    def __init__(self, video_info: VideoInfo, map_pos: str, size_hint: QSize = None):
        show_name = video_info.name
        if len(show_name) > 15:
            show_name = show_name[:15] + "..."

        super().__init__(show_name)
        self.setIcon(QIcon(QPixmap.fromImage(video_info.preview_image)))
        self.setToolTip(video_info.name)
        self.video_path = video_info.path
        self.fps = video_info.fps
        map_pos_list = map_pos.split(" ")
        assert len(map_pos_list) == 2
        self.map_pos = QPoint(int(map_pos_list[0]), int(map_pos_list[1]))
        self.video_size = video_info.size
        if size_hint:
            self.setSizeHint(size_hint)
        else:
            self.setSizeHint(QSize(300, 150))
