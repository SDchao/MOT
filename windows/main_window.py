import json

from PySide2.QtWidgets import QMainWindow, QAction, QApplication
from PySide2.QtCore import Slot
import sys

from operators import video_operator
from operators.motlogging import logger
from windows.preview_item import PreviewItem
from windows.main_widget import MainWidget


class MainWindow(QMainWindow):
    main_widget: MainWidget = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("MOT")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("文件")
        # Exit
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)
        # Data Mode
        # self.data_mode = self.menu.addMenu("数据模式")
        #
        # self.data_mode_auto_action = QAction("自动数据", self)
        # self.data_mode_auto_action.triggered.connect(self.set_data_mode_auto)
        # self.data_mode_auto_action.setCheckable(True)
        #
        # self.data_mode_clean_action = QAction("clean数据", self)
        # self.data_mode_clean_action.triggered.connect(self.set_data_mode_clean)
        # self.data_mode_clean_action.setCheckable(True)
        # self.data_mode_clean_action.setChecked(True)
        #
        # self.data_mode.addAction(self.data_mode_auto_action)
        # self.data_mode.addAction(self.data_mode_clean_action)

        # Help
        self.help_menu = self.menu.addMenu("帮助")
        # About
        about_action = QAction("关于", self)
        self.help_menu.addAction(about_action)

        # Status
        self.status = self.statusBar()
        self.status.showMessage("正在加载主界面")

    def set_data(self, data_root: str):

        self.main_widget.clear_data()

        self.main_widget.data_root = data_root

        info_path = data_root + "/info.json"
        video_path = data_root + "/videos/"
        info = json.load(open(info_path, "r", encoding="utf8"))
        self.setWindowTitle(info["name"])
        cameras_info = info["cameras"]
        map_poses = info["mapPos"]
        self.main_widget.map_label.set_map(data_root + "/map.jpg", map_poses)
        # main_widget.set_reid_container(reid_container)

        video_item_dict = {}

        for camera_info in cameras_info:
            for video in camera_info["videos"]:
                video_name = video[0]
                video_index = video[1]
                video_info = video_operator.get_video_info(video_path + video_name)
                if not video_info.no_err:
                    logger.error("Unable to find " + video_name)
                    continue
                index = int(camera_info["mapPosIndex"])
                item = PreviewItem(video_info, map_poses[index])
                # main_widget.add_video(item)
                video_item_dict[video_index] = item

        video_index_list = list(video_item_dict.keys())
        video_index_list.sort()
        for index in video_index_list:
            self.main_widget.add_video(video_item_dict[index])

    def center_screen(self):
        desktop_rect = QApplication.primaryScreen().geometry()
        center = desktop_rect.center()
        self.move(center.x() - self.width() * 0.5,
                  center.y() - self.height() * 0.5)

    def adjustSize(self):
        super(MainWindow, self).adjustSize()
        self.center_screen()

    def show_message(self, msg: str, timeout=5000):
        self.status.showMessage(msg, timeout)

    @Slot()
    def exit_app(self):
        sys.exit()

    @Slot()
    def set_data_mode_auto(self):
        self.main_widget.set_data_mode(False)
        self.data_mode_auto_action.setChecked(True)
        self.data_mode_clean_action.setChecked(False)

    @Slot()
    def set_data_mode_clean(self):
        self.main_widget.set_data_mode(True)
        self.data_mode_auto_action.setChecked(False)
        self.data_mode_clean_action.setChecked(True)
