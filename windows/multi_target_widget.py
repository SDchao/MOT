from PySide2.QtWidgets import (QWidget, QPushButton, QGridLayout, QStyle, QListWidgetItem)
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtGui import QMouseEvent
from PySide2.QtCore import Qt
from windows.preview_list_widget import PreviewListWidget
from windows.video_view import VideoGraphicsView
from windows.preview_item import PreviewItem
from operators.convertor import get_absolute_qurl
from operators.reid_operator import ReidContainer


class MultiTargetWidget(QWidget):
    last_index: int = -1

    def __init__(self):
        QWidget.__init__(self)
        # 播放器
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # 设置帧触发器
        self.player.positionChanged.connect(self.__on_position_changed)
        self.player.setNotifyInterval(1000 / 30)
        self.play_list = QMediaPlaylist()
        self.play_list.setPlaybackMode(QMediaPlaylist.Loop)
        self.play_list.currentIndexChanged.connect(self.__current_index_changed)

        self.player.setPlaylist(self.play_list)

        # 视频预览列表
        self.preview_list = PreviewListWidget()
        self.preview_list.itemActivated.connect(self.__on_list_item_activated)

        self.main_video_view = VideoGraphicsView(self.player, 1272, 720, True)

        # 暂停按钮
        self.pause_button = QPushButton()
        self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pause_button.clicked.connect(self.__on_pause_button_clicked)
        self.pause_button.setMinimumWidth(100)

        self.main_video_view.mousePressEvent = self.__on_video_mouse_press

        # 窗口的底层Layout
        base_layout = QGridLayout()
        # 视频预览
        base_layout.addWidget(self.preview_list, 0, 1, 1, 2)
        # 主视频播放
        base_layout.addWidget(self.main_video_view, 1, 1, Qt.AlignCenter)
        # 暂停按钮
        base_layout.addWidget(self.pause_button, 2, 1, Qt.AlignCenter)

        base_layout.setColumnStretch(0, 1)

        self.setLayout(base_layout)
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
        self.main_video_view.paint_board.read_data(item.video_path, item.fps)
        self.main_video_view.paint_board.set_raw_size(item.video_size)

    def __current_index_changed(self, index: int):
        self.preview_list.setCurrentRow(index)
        self.preview_list.item(index).setSelected(True)

        self.player.play()

        self.__change_video_data(self.preview_list.item(index))
        self.main_video_view.paint_board.renew_select(self.last_index, index)

        self.last_index = index

    def __on_list_item_activated(self, item: QListWidgetItem):
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
