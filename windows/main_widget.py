from PySide2.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QGridLayout,
                               QSizePolicy, QTableWidget, QTableWidgetItem,
                               QAbstractItemView, QLabel, QListWidgetItem)
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtCore import QUrl, QFileInfo, QSize, QModelIndex
from PySide2.QtGui import QPixmap, QMouseEvent
from windows.preview_list_widget import PreviewListWidget
from windows.paint_board import PaintBoard
from windows.video_view import VideoGraphicsView
from windows.preview_item import PreviewItem
from windows.map_label import MapLabel
from operators.convertor import get_absolute_qurl


class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # 播放器
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # 设置帧触发器
        self.player.positionChanged.connect(self.__on_position_changed)
        self.player.setPlaybackRate(3)
        self.player.setNotifyInterval(1000 / 30)
        self.play_list = QMediaPlaylist()
        # self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile("windows/videos/default.mp4")))
        # self.play_list.addMedia(QUrl.fromLocalFile(QFileInfo("windows/videos/default.mp4").absoluteFilePath()))
        self.play_list.setPlaybackMode(QMediaPlaylist.Loop)
        self.play_list.currentIndexChanged.connect(self.__current_index_changed)

        self.player.setPlaylist(self.play_list)

        # 左侧按钮
        self.button_select_face = QPushButton("选择人脸输入")
        self.button_open_mot = QPushButton("打开MOT")
        self.button_open_ReID = QPushButton("打开ReID")

        left_button_group = (
            self.button_select_face, self.button_open_mot, self.button_open_ReID)

        for button in left_button_group:
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            button.setMaximumHeight(100)

        # 左侧功能按钮布局
        left_v_layout = QVBoxLayout()
        left_v_layout.setSpacing(10)
        left_v_layout.setMargin(10)

        for button in left_button_group:
            left_v_layout.addWidget(button)

        # 视频预览列表
        self.preview_list = PreviewListWidget()
        self.preview_list.itemActivated.connect(self.__on_list_item_activated)

        # 视频窗口
        """
        # 视频容器，用于添加子控件
        self.main_video_container = QWidget()
        # layout，作为容器的布局
        # lay = QVBoxLayout(self.main_video_container)
        lay = QVBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)

        self.main_video_container.setLayout(lay)

        # 显示视频的控件，放置于layout中
        self.main_video_widget = QVideoWidget()
        self.player.setVideoOutput(self.main_video_widget)
        self.main_video_widget.setMinimumSize(1272, 720)
        lay.addWidget(self.main_video_widget)
        """
        self.main_video_view = VideoGraphicsView(self.player, 1272, 720)
        self.paint_board = PaintBoard()
        self.paint_board.setFixedSize(self.main_video_view.size())
        self.main_video_view.scene().addWidget(self.paint_board)

        self.main_video_view.mousePressEvent = self.__on_video_mouse_press

        # 右下摄像机表格
        self.camera_table = QTableWidget(3, 5)
        self.camera_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.camera_table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.camera_table.setHorizontalHeaderLabels(
            ["C1", "C2", "C3", "C4", "C5"])
        self.camera_table.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        count = 0
        for i in range(0, 3):
            for j in range(0, 5):
                count += 1
                self.camera_table.setItem(i, j, QTableWidgetItem(str(count)))

        # 右下地图
        self.map_label = MapLabel()
        # self.map_label.setFixedSize(411 * 2, 282 * 2)

        # 右下布局
        right_v_layout = QVBoxLayout()
        right_v_layout.setSpacing(10)
        right_v_layout.setMargin(10)

        right_v_layout.addWidget(self.camera_table)
        right_v_layout.addWidget(self.map_label)

        # 窗口的底层Layout
        base_layout = QGridLayout()
        # 左侧功能按钮
        base_layout.addLayout(left_v_layout, 0, 0, 2, 1)
        # 视频预览
        base_layout.addWidget(self.preview_list, 0, 1, 1, 2)
        # 主视频播放
        base_layout.addWidget(self.main_video_view, 1, 1)
        # 右下状态
        base_layout.addLayout(right_v_layout, 1, 2)
        base_layout.setColumnStretch(0, 1)
        base_layout.setColumnStretch(1, 5)
        base_layout.setColumnStretch(2, 3)
        base_layout.setColumnMinimumWidth(2, 500)

        base_layout.setHorizontalSpacing(10)
        base_layout.setVerticalSpacing(10)

        self.setLayout(base_layout)
        self.player.play()

    def __on_position_changed(self, pos):
        if hasattr(self, "paint_board"):
            self.paint_board.set_now_time(pos)
            self.paint_board.update()

    def __on_video_mouse_press(self, event: QMouseEvent):
        print(event.x(), event.y())

    def __change_video(self, path: str):
        qurl = get_absolute_qurl(path)
        media_count = self.play_list.mediaCount()
        found = False
        for i in range(0, media_count):
            if self.play_list.media(i) == qurl:
                found = True
                print("Now playing: " + path)
                self.play_list.setCurrentIndex(i)
                self.player.play()

        if not found:
            print(f"Cannot found media {path}")

    def __current_index_changed(self, index: int):
        self.preview_list.setCurrentRow(index)
        self.preview_list.item(index).setSelected(True)
        self.__on_list_item_activated(self.preview_list.item(index))

    def __on_list_item_activated(self, item: QListWidgetItem):
        if isinstance(item, PreviewItem):
            self.__change_video(item.video_path)
            self.map_label.set_now_pos(item.map_pos)
            self.paint_board.read_data(item.video_path, item.fps)
            self.paint_board.set_raw_size(item.video_size)
        else:
            print("Selected item is not a video preview!")

    def add_video(self, item: PreviewItem):
        self.__add_video_to_playlist(item.video_path)
        self.preview_list.insert_item(item)

    def __add_video_to_playlist(self, path: str):
        qurl = get_absolute_qurl(path)
        self.play_list.addMedia(qurl)
