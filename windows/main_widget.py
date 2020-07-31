from PySide2.QtWidgets import QWidget,QPushButton, QVBoxLayout, QGridLayout, QSizePolicy
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtCore import QUrl
from PySide2.QtMultimediaWidgets import QVideoWidget
from windows.preview_list_widget import Preview_List_Widget

class Main_Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # 播放器
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.play_list = QMediaPlaylist()
        # self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile("windows/videos/default.mp4")))
        self.play_list.addMedia(QUrl("windows/videos/default.mp4"))
        self.play_list.setPlaybackMode(QMediaPlaylist.Loop)
        self.player.setPlaylist(self.play_list)


        # 左侧按钮
        self.button_select_face = QPushButton("选择人脸输入")
        self.button_open_mot = QPushButton("打开MOT")
        self.button_open_ReID = QPushButton("打开ReID")

        self.left_button_group = (self.button_select_face, self.button_open_mot, self.button_open_ReID)

        for button in self.left_button_group:
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


        # 左侧功能按钮布局
        self.left_v_layout = QVBoxLayout()
        self.left_v_layout.setSpacing(10)
        self.left_v_layout.setMargin(10)

        for button in self.left_button_group:
            self.left_v_layout.addWidget(button)

        # 视频预览列表
        self.preview_list = Preview_List_Widget()

        # 视频窗口
        self.main_video_player = QVideoWidget()
        self.player.setVideoOutput(self.main_video_player)
        self.main_video_player.setMinimumSize(720, 405)

        self.player.play()

        # 窗口的底层Layout
        self.base_layout = QGridLayout()
        # 左侧功能按钮 0 0 -> 3 1
        self.base_layout.addLayout(self.left_v_layout, 0, 0, 3, 1)
        # 视频预览 0 1 -> 1 5
        self.base_layout.addWidget(self.preview_list, 0, 1, 1, 4)
        # 主视频播放 1 1 -> 3 3
        self.base_layout.addWidget(self.main_video_player, 1, 1, 2, 2)

        self.base_layout.setHorizontalSpacing(10)
        self.base_layout.setVerticalSpacing(10)

        self.setLayout(self.base_layout)