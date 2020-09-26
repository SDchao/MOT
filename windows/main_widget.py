from PySide2.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QGridLayout,
                               QSizePolicy, QTableWidget, QTableWidgetItem,
                               QAbstractItemView, QStyle, QListWidgetItem)
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtGui import QPixmap, QMouseEvent, QResizeEvent
from PySide2.QtCore import Qt
from windows.preview_list_widget import PreviewListWidget
from windows.paint_board import PaintBoard
from windows.video_view import VideoGraphicsView
from windows.preview_item import PreviewItem
from windows.map_label import MapLabel
from operators.convertor import get_absolute_qurl
from operators.reid_operator import ReidContainer
from windows.track_widget import TrackWidget


class MainWidget(QWidget):
    last_index: int = -1
    screenw: int = 0
    screenh: int = 0

    def __init__(self, screenw: int, screenh: int):
        QWidget.__init__(self)
        self.screenw = screenw
        self.screenh = screenh

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # 播放器
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # 设置帧触发器
        self.player.positionChanged.connect(self.__on_position_changed)
        # self.player.setPlaybackRate(3)
        self.player.setNotifyInterval(1000 / 30)
        self.play_list = QMediaPlaylist()
        # self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile("windows/videos/default.mp4")))
        # self.play_list.addMedia(QUrl.fromLocalFile(QFileInfo("windows/videos/default.mp4").absoluteFilePath()))
        self.play_list.setPlaybackMode(QMediaPlaylist.Loop)
        self.play_list.currentIndexChanged.connect(self.__current_index_changed)

        self.player.setPlaylist(self.play_list)

        # 左侧按钮
        self.button_open_main = QPushButton("主界面")
        self.button_open_mot = QPushButton("MOT")
        self.button_open_ReID = QPushButton("ReID")

        self.button_open_main.clicked.connect(self.__on_button_open_main_clicked)
        self.button_open_mot.clicked.connect(self.__on_button_open_mot_clicked)

        left_button_group = (
            self.button_open_main, self.button_open_mot, self.button_open_ReID)

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
        self.preview_list.itemPressed.connect(self.__on_list_item_pressed)

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

        # 暂停按钮
        self.pause_button = QPushButton()
        self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pause_button.clicked.connect(self.__on_pause_button_clicked)
        self.pause_button.setMinimumWidth(100)

        self.main_video_view.mousePressEvent = self.__on_video_mouse_press

        # 右下轨迹图
        self.track_view = TrackWidget(screenw * 0.2, screenh * 0.2, 1272, 720)
        self.main_video_view.paint_board.track_widget = self.track_view

        # 右下地图
        self.map_label = MapLabel()
        # self.map_label.setFixedSize(411 * 2, 282 * 2)

        # 右下布局
        right_v_layout = QVBoxLayout()
        right_v_layout.addWidget(self.track_view, 0, Qt.AlignCenter)
        right_v_layout.addWidget(self.map_label, 0, Qt.AlignCenter)

        # 窗口的底层Layout
        self.main_layout = QGridLayout()
        # 左侧功能按钮
        self.main_layout.addLayout(left_v_layout, 0, 0, 3, 1)
        # 视频预览
        self.main_layout.addWidget(self.preview_list, 0, 1, 1, 2)
        # 主视频播放
        self.main_layout.addWidget(self.main_video_view, 1, 1, Qt.AlignCenter)
        # 暂停按钮
        self.main_layout.addWidget(self.pause_button, 2, 1, Qt.AlignCenter)
        # 右侧状态
        self.main_layout.addLayout(right_v_layout, 1, 2, 2, 1)

        # 设置宽度
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 3)
        self.main_layout.setColumnStretch(2, 1)

        self.main_layout.setColumnMinimumWidth(2, self.screenw * 0.2)

        self.button_open_main.setDisabled(True)

        self.setLayout(self.main_layout)
        self.player.play()

    def set_reid_container(self, c: ReidContainer):
        self.main_video_view.paint_board.reid_container = c
        print(f"Set reid container, record {len(c.info)}")

    def __on_position_changed(self, pos):
        self.main_video_view.paint_board.set_now_time(pos)
        self.main_video_view.paint_board.update()

    def __on_video_mouse_press(self, event: QMouseEvent):
        self.main_video_view.paint_board.on_click(event)
        self.main_video_view.paint_board.update()

    def __change_video(self, new_index: int):
        print(f"Now playing index {new_index}")
        self.play_list.setCurrentIndex(new_index)

    def __change_video_data(self, item: PreviewItem):
        self.map_label.set_now_pos(item.map_pos)
        self.main_video_view.paint_board.read_data(item.video_path, item.fps)
        self.main_video_view.paint_board.set_raw_size(item.video_size)

    def __current_index_changed(self, index: int):
        self.preview_list.setCurrentRow(index)
        self.preview_list.item(index).setSelected(True)

        self.player.play()

        self.__change_video_data(self.preview_list.item(index))
        self.main_video_view.paint_board.renew_select(self.last_index, index)
        self.track_view.clear()

        self.last_index = index

    def __on_list_item_pressed(self, item: QListWidgetItem):
        if isinstance(item, PreviewItem):
            self.__change_video(self.preview_list.currentIndex().row())

    def add_video(self, item: PreviewItem):
        self.__add_video_to_playlist(item.video_path)
        self.preview_list.insert_item(item)

    def __add_video_to_playlist(self, path: str):
        qurl = get_absolute_qurl(path)
        self.play_list.addMedia(qurl)

    def __on_pause_button_clicked(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
            self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def __on_button_open_mot_clicked(self):
        print("Switching MOT layout")
        self.track_view.hide()
        self.map_label.hide()
        self.main_layout.setColumnMinimumWidth(2, 0)
        self.button_open_main.setDisabled(False)
        self.button_open_mot.setDisabled(True)
        self.button_open_ReID.setDisabled(False)

        self.main_video_view.paint_board.init_show_all = True

        self.adjustSize()

    def __on_button_open_main_clicked(self):
        print("Switching Main layout")
        self.track_view.show()
        self.map_label.show()
        # 设置宽度
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 3)
        self.main_layout.setColumnStretch(2, 1)

        self.main_layout.setColumnMinimumWidth(2, self.screenw * 0.2)

        self.button_open_main.setDisabled(True)
        self.button_open_mot.setDisabled(False)
        self.button_open_ReID.setDisabled(False)

        self.main_video_view.paint_board.init_show_all = False
        self.track_view.clear()

        self.adjustSize()

    def adjustSize(self):
        super().adjustSize()
        self.window().adjustSize()
