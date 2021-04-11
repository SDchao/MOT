import abc
import os

from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QStyle

from manage_tools.widgets.progress_bar import ProgressBar
from operators.convertor import get_absolute_qurl
from operators.video_operator import VideoInfo, get_video_info
from windows.paint_board import PaintBoard
from windows.video_view import VideoGraphicsView


class ModifierWidget(QWidget):
    file_ext = ".*"

    player: QMediaPlayer
    player_list: QMediaPlaylist
    main_video_view: VideoGraphicsView
    paint_board: PaintBoard
    now_player_rate_index = 2
    __player_rate_list = [0.5, 0.7, 1.0, 1.5, 2.0, 3.0]

    left_v_layout: QVBoxLayout
    right_v_layout: QVBoxLayout
    central_v_layout: QVBoxLayout

    now_video_info: VideoInfo

    def __init__(self):
        super(ModifierWidget, self).__init__()
        self.setFixedSize(int(1920 * 0.8), int(1080 * 0.8))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        video_width = self.width() * 0.5
        video_height = video_width * 0.5625

        # 播放器
        self.player = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        # 设置帧触发器
        self.player.positionChanged.connect(self._on_position_changed)
        self.player.durationChanged.connect(self._on_duration_changed)
        # self.player.setPlaybackRate(3)
        self.player.setNotifyInterval(1000 / 30)
        self.play_list = QMediaPlaylist()
        self.play_list.setPlaybackMode(QMediaPlaylist.Loop)

        self.player.setPlaylist(self.play_list)

        self.main_video_view = VideoGraphicsView(self.player, video_width, video_height)
        self.paint_board = self.main_video_view.paint_board

        # Progress Bar
        self.progress_bar = ProgressBar(video_width)
        self.progress_bar.mousePressEvent = self._on_progress_bar_pressed
        self.progress_bar.mouseMoveEvent = self._on_progress_bar_move
        self.progress_bar.mouseReleaseEvent = self._on_progress_bar_released

        # PlayerControl
        self.player_control_widget = QWidget()
        self.player_control_layout = QHBoxLayout()
        self.player_control_layout.setSpacing(0)
        # Pause
        self.pause_button = QPushButton()
        self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pause_button.clicked.connect(self._on_pause_button_clicked)
        self.pause_button.setFixedWidth(150)
        self.pause_button.setFixedHeight(30)
        # Faster
        self.faster_button = QPushButton()
        self.faster_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.faster_button.clicked.connect(self._on_faster_button_clicked)
        self.faster_button.setFixedWidth(50)
        self.faster_button.setFixedHeight(30)
        # Slower
        self.slower_button = QPushButton()
        self.slower_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.slower_button.clicked.connect(self._on_slower_button_clicked)
        self.slower_button.setFixedWidth(50)
        self.slower_button.setFixedHeight(30)
        # Forward
        self.forward_button = QPushButton()
        self.forward_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forward_button.clicked.connect(self._on_forward_button_clicked)
        self.forward_button.setFixedWidth(50)
        self.slower_button.setFixedHeight(30)
        # Backward
        self.backward_button = QPushButton()
        self.backward_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.backward_button.clicked.connect(self._on_backward_button_clicked)
        self.backward_button.setFixedWidth(50)
        self.backward_button.setFixedHeight(30)

        self.player_control_layout.addWidget(self.slower_button)
        self.player_control_layout.addWidget(self.backward_button)
        self.player_control_layout.addWidget(self.pause_button)
        self.player_control_layout.addWidget(self.forward_button)
        self.player_control_layout.addWidget(self.faster_button)

        self.player_control_widget.setLayout(self.player_control_layout)
        self.player_control_widget.setFixedWidth(video_width)

        # Layout
        self.parent_layout = QHBoxLayout(self)

        self.left_v_layout = QVBoxLayout()
        self.central_v_layout = QVBoxLayout()
        self.central_v_layout.setAlignment(Qt.AlignHCenter)
        self.right_v_layout = QVBoxLayout()

        # Add widget to layout
        self.central_v_layout.addStretch(1)
        self.central_v_layout.addWidget(self.main_video_view)
        self.central_v_layout.addWidget(self.progress_bar)
        self.central_v_layout.addWidget(self.player_control_widget)
        self.central_v_layout.addStretch(1)

        self.parent_layout.addLayout(self.left_v_layout)
        self.parent_layout.addLayout(self.central_v_layout)
        self.parent_layout.addLayout(self.right_v_layout)
        self.setLayout(self.parent_layout)

    @abc.abstractmethod
    def open(self, file_path: str):
        pass

    @abc.abstractmethod
    def save(self, save_path: str):
        pass

    def set_video(self, video_path):
        if os.path.exists(video_path):
            self.now_video_info = get_video_info(video_path)

            if not self.now_video_info.no_err:
                return -1

            self.main_video_view.paint_board.read_data(self.now_video_info.path, self.now_video_info.fps)
            self.main_video_view.paint_board.set_raw_size(self.now_video_info.size)

            self.play_list.clear()
            qurl = get_absolute_qurl(video_path)
            self.play_list.addMedia(qurl)
            self.player.play()
            self._on_pause_button_clicked()

    def _on_position_changed(self, pos):
        self.main_video_view.paint_board.set_now_time(pos)
        self.main_video_view.paint_board.update()
        self.progress_bar.update_pos(pos)

    def _on_duration_changed(self, duration):
        self.main_video_view.paint_board.set_total_time(duration)
        self.progress_bar.set_duration(duration)

    # Progress Bar
    def _on_progress_bar_move(self, event: QMouseEvent):
        if self.progress_bar.is_pressing:
            ratio = event.pos().x() / self.progress_bar.width()
            if ratio >= 1:
                ratio = 1
            elif ratio < 0:
                ratio = 0
            self.player.setPosition(ratio * self.player.duration())

    def _on_progress_bar_pressed(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.progress_bar.is_pressing = True
            self._on_progress_bar_move(event)

    def _on_progress_bar_released(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.progress_bar.is_pressing = False

    # Player_Control
    def _on_faster_button_clicked(self):
        self.now_player_rate_index += 1
        self.slower_button.setEnabled(True)
        if self.now_player_rate_index >= len(self.__player_rate_list) - 1:
            self.faster_button.setDisabled(True)

        self.player.setPlaybackRate(self.__player_rate_list[self.now_player_rate_index])

    def _on_slower_button_clicked(self):
        self.now_player_rate_index -= 1
        self.faster_button.setEnabled(True)
        if self.now_player_rate_index <= 0:
            self.slower_button.setDisabled(True)

        self.player.setPlaybackRate(self.__player_rate_list[self.now_player_rate_index])

    def _on_pause_button_clicked(self):
        if self.player.state() == QMediaPlayer.State.PausedState:
            self.player.play()
            self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        elif self.player.state() == QMediaPlayer.State.PlayingState:
            self.player.pause()
            self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def _on_forward_button_clicked(self):
        new_position = self.player.position() + 5 * 1000
        if new_position > self.player.duration():
            new_position = self.player.duration()
        self.player.setPosition(new_position)

    def _on_backward_button_clicked(self):
        new_position = self.player.position() - 5 * 1000
        if new_position < 0:
            new_position = 0
        self.player.setPosition(new_position)
