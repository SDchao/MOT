import json

from PySide2.QtWidgets import QMainWindow, QAction, QApplication, QFileDialog, QMessageBox, QProgressDialog
from PySide2.QtCore import Slot, Qt
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
        # Select data
        open_action = QAction("打开..", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_data)
        self.file_menu.addAction(open_action)

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

    @Slot()
    def open_data(self):
        user_selected_dir = QFileDialog.getExistingDirectory(self, "选择数据文件夹", ".", QFileDialog.ShowDirsOnly)
        if user_selected_dir:
            err_text = self.set_data(user_selected_dir)
            if err_text:
                self.show_message("无法载入数据")
                msg_box = QMessageBox()
                msg_box.setText(f"无法载入数据\n{err_text}")
                msg_box.setWindowTitle("错误")
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("成功")
                msg_box.setText("载入成功")
                msg_box.exec_()

    def set_data(self, data_root: str):
        # Open Process Dialog
        progress_dialog = QProgressDialog("正在读取数据", "取消", 0, 100, self)
        progress_dialog.setWindowTitle("请稍后")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)

        self.main_widget.clear_data()
        self.main_widget.set_data(data_root)

        info_path = data_root + "/info.json"
        video_path = data_root + "/videos/"
        try:
            info = json.load(open(info_path, "r", encoding="utf8"))
            self.setWindowTitle(info["name"])
            cameras_info = info["cameras"]
            map_poses = info["mapPos"]
            self.main_widget.map_label.set_map(data_root + "/map.jpg", map_poses)
            # main_widget.set_reid_container(reid_container)

            video_item_dict = {}

            i = 0
            progress_dialog.setMaximum(len(cameras_info))

            for camera_info in cameras_info:
                progress_dialog.setValue(i)
                i += 1
                for video in camera_info["videos"]:

                    if progress_dialog.wasCanceled():
                        self.main_widget.clear_data()
                        return "用户取消"

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

            progress_dialog.close()

            for index in video_index_list:
                self.main_widget.add_video(video_item_dict[index])

            return ""
        except FileNotFoundError as e:
            logger.error(f"Cannot load file {e.filename}")
            self.main_widget.clear_data()
            return f"无法载入文件{e.filename}"
        except KeyError as e:
            logger.error(f"Incorrect info json {info_path}, no key named {e}")
            self.main_widget.clear_data()
            return f"错误数据格式\n{info_path}\n无法找到键: {e}"

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
