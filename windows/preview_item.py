from PySide2.QtWidgets import QListWidgetItem
from PySide2.QtCore import QSize, QPoint
from PySide2.QtGui import QIcon, QPixmap, QImage


class PreviewItem(QListWidgetItem):
    video_path: str
    map_pos: QPoint

    def __init__(self, name: str, icon: QImage, video_path: str, map_pos_str: str, size: QSize = None):
        """

        @param name: 视频预览的显示名称
        @param icon: 视频预览的图片
        @param video_path: 视频路径，可为相对路径
        @param map_pos_str: 地图坐标，为字符串，x、y以空格相隔
        @param size: 预览Item的大小
        """
        show_name = name
        if len(name) > 15:
            show_name = name[:15] + "..."

        super().__init__(show_name)
        self.setIcon(QIcon(QPixmap.fromImage(icon)))
        self.setToolTip(name)
        self.video_path = video_path
        map_pos_list = map_pos_str.split(" ")
        assert len(map_pos_list) == 2
        self.map_pos = QPoint(int(map_pos_list[0]), int(map_pos_list[1]))
        if size:
            self.setSizeHint(size)
        else:
            self.setSizeHint(QSize(300, 150))
