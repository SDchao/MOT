from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtWidgets import (QWidget, QPushButton, QGridLayout,
                               QSizePolicy, QAbstractItemView, QStyle, QListWidgetItem)

from operators.convertor import get_absolute_qurl
from operators.motlogging import logger
from windows.preview_item import PreviewItem
from windows.preview_list_widget import PreviewListWidget
from windows.video_view import VideoGraphicsView


class CompareWidget(QWidget):
    last_index: int = -1
    screenw: int = 0
    screenh: int = 0
    window = None
    data_root1 = ""
    data_root2 = ""

    def __init__(self, screenw: int, screenh: int, window):
        QWidget.__init__(self)
        self.screenw = screenw
        self.screenh = screenh
        self.window = window

        # 模拟分辨率调试
        # screenw = 1920
        # screenh = 1080

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # 播放器
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # 设置帧触发器
        self.player.positionChanged.connect(self.__on_position_changed)
        self.player.durationChanged.connect(self.__on_duration_changed)
        # self.player.setPlaybackRate(3)
        self.player.setNotifyInterval(1000 / 30)
        self.play_list = QMediaPlaylist()

        self.play_list.setPlaybackMode(QMediaPlaylist.Loop)
        self.play_list.currentIndexChanged.connect(self.__current_index_changed)

        self.player.setPlaylist(self.play_list)
        self.player2.setPlaylist(self.play_list)

        # 视频预览列表
        self.preview_list = PreviewListWidget()
        self.preview_list.currentItemChanged.connect(self.__on_current_item_changed)
        self.preview_list.setSelectionMode(QAbstractItemView.SingleSelection)

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
        video_width = screenw * 0.4
        video_height = video_width * 0.5625

        self.video_view1 = VideoGraphicsView(self.player, video_width, video_height)
        self.video_view2 = VideoGraphicsView(self.player2, video_width, video_height)

        self.video_view1.paint_board.init_show_all = True
        self.video_view2.paint_board.init_show_all = True

        # 暂停按钮
        self.pause_button = QPushButton()
        self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pause_button.clicked.connect(self.__on_pause_button_clicked)
        self.pause_button.setMinimumWidth(100)

        self.video_view1.mousePressEvent = self.__on_video_mouse_press

        # 窗口的底层Layout
        self.main_layout = QGridLayout()
        # 视频预览
        self.main_layout.addWidget(self.preview_list, 0, 1, 1, 2)
        # 视频播放
        self.main_layout.addWidget(self.video_view1, 1, 1, Qt.AlignCenter)
        self.main_layout.addWidget(self.video_view2, 1, 2, Qt.AlignCenter)
        # 暂停按钮
        self.main_layout.addWidget(self.pause_button, 2, 1, 1, 2, Qt.AlignCenter)
        # # 右侧状态
        # self.main_layout.addLayout(right_v_layout, 1, 2, 2, 1)

        # 设置宽度
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 3)
        self.main_layout.setColumnStretch(2, 1)

        self.main_layout.setColumnMinimumWidth(2, self.screenw * 0.2)

        # self.button_open_main.setDisabled(True)

        self.setLayout(self.main_layout)
        self.player.play()
        self.player2.play()

        self.window.show_message("准备就绪")
        logger.info("compare_widget init completed")

    def __on_position_changed(self, pos):
        self.video_view1.paint_board.set_now_time(pos)
        self.video_view1.paint_board.update()
        self.video_view2.paint_board.set_now_time(pos)
        self.video_view2.paint_board.update()

    def __on_duration_changed(self, duration):
        self.video_view1.paint_board.set_total_time(duration)
        self.video_view2.paint_board.set_total_time(duration)

    def __on_video_mouse_press(self, event: QMouseEvent):
        pass
        # ws_mode = True
        # if self.layout_mode == LAYOUT_REID or self.layout_mode == LAYOUT_MOT:
        #     ws_mode = False
        #
        # target_id = self.first_video_view.paint_board.on_click(event, ws_mode)
        # self.first_video_view.paint_board.update()
        #
        # self.window.show_message("视频点击已处理")

    def __change_video(self, new_index: int):
        logger.info(f"Now playing index {new_index}")
        self.play_list.setCurrentIndex(new_index)

    def __change_video_data(self, item: PreviewItem):
        self.video_view1.paint_board.read_data(item.video_path, item.fps)
        self.video_view1.paint_board.set_raw_size(item.video_size)
        self.video_view2.paint_board.read_data(item.video_path.replace(self.data_root1, self.data_root2), item.fps)
        self.video_view2.paint_board.set_raw_size(item.video_size)

    def __current_index_changed(self, index: int):
        if index >= 0:
            self.preview_list.setCurrentRow(index)
            self.preview_list.item(index).setSelected(True)

            self.__change_video_data(self.preview_list.item(index))
            if self.last_index >= 0:
                pos = self.player.position()
                if pos == 0:
                    pos = 9223372036854775807
                last_item = self.preview_list.item(self.last_index)
                if isinstance(last_item, PreviewItem):
                    self.video_view1.paint_board.renew_select(self.last_index, index, pos, last_item.fps,
                                                              self.data_root1,
                                                              False)
                    self.video_view2.paint_board.renew_select(self.last_index, index, pos, last_item.fps,
                                                              self.data_root2,
                                                              False)

            self.last_index = index
            self.window.show_message(f"正在播放 {index + 1} 号视频")
            self.player.play()
            self.player2.play()

    def __on_current_item_changed(self, current: QListWidgetItem, pre: QListWidgetItem):
        if isinstance(current, PreviewItem):
            self.__change_video(self.preview_list.currentIndex().row())

    def clear_data(self):
        self.preview_list.clear()
        self.play_list.clear()

    def add_video(self, item: PreviewItem):
        self.__add_video_to_playlist(item.video_path)
        self.preview_list.insert_item(item)

    def __add_video_to_playlist(self, path: str):
        qurl = get_absolute_qurl(path)
        self.play_list.addMedia(qurl)

    def __on_pause_button_clicked(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.player2.pause()
            self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.window.show_message("暂停视频")
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
            self.player2.play()
            self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.window.show_message("播放视频")

    def set_data(self, data_root: str):
        self.data_root1 = data_root
        if not self.data_root2:
            self.data_root2 = self.data_root1

    def set_compare_data(self, data_root: str):
        self.data_root2 = data_root

    def reset_data(self):
        if self.data_root1:
            pass
            self.preview_list.clearSelection()
            self.window.set_data(self.data_root1)

    def adjustSize(self):
        super().adjustSize()
        self.window.adjustSize()
