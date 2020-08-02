from PySide2.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QGridLayout,
                               QSizePolicy, QTableWidget, QTableWidgetItem, QAbstractItemView, QLabel)
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtCore import QUrl
from PySide2.QtGui import QPixmap, QMouseEvent
from windows.preview_list_widget import PreviewListWidget
from windows.paint_board import PaintBoard
from windows.video_view import VideoGraphicsView


class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # 播放器
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # 设置帧触发器
        self.player.positionChanged.connect(self.position_changed)
        self.player.setNotifyInterval(1000 / 30)
        self.play_list = QMediaPlaylist()
        # self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile("windows/videos/default.mp4")))
        self.play_list.addMedia(QUrl("windows/videos/default.mp4"))
        self.play_list.setPlaybackMode(QMediaPlaylist.Loop)
        self.player.setPlaylist(self.play_list)

        # 左侧按钮
        self.button_select_face = QPushButton("选择人脸输入")
        self.button_open_mot = QPushButton("打开MOT")
        self.button_open_ReID = QPushButton("打开ReID")

        self.left_button_group = (
            self.button_select_face, self.button_open_mot, self.button_open_ReID)

        for button in self.left_button_group:
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            button.setMinimumWidth(300)
            button.setMaximumHeight(200)

        # 左侧功能按钮布局
        self.left_v_layout = QVBoxLayout()
        self.left_v_layout.setSpacing(10)
        self.left_v_layout.setMargin(10)

        for button in self.left_button_group:
            self.left_v_layout.addWidget(button)

        # 视频预览列表
        self.preview_list = PreviewListWidget()

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
        self.main_video_view.scene().addWidget(self.paint_board)

        self.main_video_view.mousePressEvent = self.video_mouse_press

        # 右下摄像机表格
        self.camrea_table = QTableWidget(3, 5)
        self.camrea_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.camrea_table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.camrea_table.setHorizontalHeaderLabels(
            ["C1", "C2", "C3", "C4", "C5"])
        self.camrea_table.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        count = 0
        for i in range(0, 3):
            for j in range(0, 5):
                count += 1
                self.camrea_table.setItem(i, j, QTableWidgetItem(str(count)))

        # 右下尾随状态
        self.follow_state = QLabel("Test")
        pixmap = QPixmap("windows/images/Default.png")
        self.follow_state.setPixmap(pixmap)
        self.follow_state.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.follow_state.setScaledContents(True)

        # 右下布局
        self.right_v_layout = QVBoxLayout()
        self.right_v_layout.setSpacing(10)
        self.right_v_layout.setMargin(10)

        self.right_v_layout.addWidget(self.camrea_table)
        self.right_v_layout.addWidget(self.follow_state)

        # 窗口的底层Layout
        self.base_layout = QGridLayout()
        # 左侧功能按钮 0 0 -> 3 1
        self.base_layout.addLayout(self.left_v_layout, 0, 0, 3, 1)
        # 视频预览 0 1 -> 1 5
        self.base_layout.addWidget(self.preview_list, 0, 1, 1, 5)
        # 主视频播放 1 1 -> 3 3
        self.base_layout.addWidget(self.main_video_view, 1, 1, 2, 2)
        # 右下状态 1 4 -> 3 5
        self.base_layout.addLayout(self.right_v_layout, 1, 4, 2, 1)

        self.base_layout.setHorizontalSpacing(10)
        self.base_layout.setVerticalSpacing(10)

        self.setLayout(self.base_layout)
        self.player.play()

    def position_changed(self, pos):
        if(hasattr(self, "paint_board")):
            self.paint_board.update()

    def video_mouse_press(self, event : QMouseEvent):
        print(event.x(), event.y())