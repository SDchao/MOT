import os

from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QApplication

from manage_tools.widgets.modifier_widget_parent import ModifierWidget
from operators.motlogging import logger


class ModifierMainWindow(QMainWindow):
    opening_file_path = ""

    def __init__(self, main_widget: ModifierWidget):
        super(ModifierMainWindow, self).__init__()
        self.setWindowTitle("MOT Modifier")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("文件")
        # open_data
        open_action = QAction("打开..", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_data)
        self.file_menu.addAction(open_action)
        # save_data
        self.save_action = QAction("保存", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_data)
        self.save_action.setEnabled(False)
        self.file_menu.addAction(self.save_action)
        # save_as_data
        self.save_as_action = QAction("另存为", self)
        self.save_as_action.setShortcut("Ctrl+Alt+S")
        self.save_as_action.triggered.connect(self.save_as_data)
        self.save_as_action.setEnabled(False)
        self.file_menu.addAction(self.save_as_action)
        # exit
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.exit)
        self.file_menu.addAction(exit_action)

        self.setCentralWidget(main_widget)

    def open_data(self, path: str = None):
        if not path:
            user_video_path = QFileDialog.getOpenFileName(self,
                                                          "选择打开的视频文件", ".",
                                                          "*.avi;;*.mp4;;*.flv")[0]
        else:
            user_video_path = path

        if user_video_path:
            video_name = os.path.splitext(user_video_path)[0]
            data_path = video_name + self.centralWidget().file_ext
            if not os.path.exists(data_path):
                logger.error(f"Unable to find {data_path}")
                error_box = QMessageBox(QMessageBox.Critical, "错误", "无法找到视频对应的数据文件")
                error_box.exec_()
                self.save_action.setEnabled(False)
                self.save_as_action.setEnabled(False)
                return
            if self.centralWidget().open(data_path) == 0:
                self.opening_file_path = data_path
                self.centralWidget().set_video(user_video_path)
                self.save_action.setEnabled(True)
                self.save_as_action.setEnabled(True)

    def save_data(self):
        if self.opening_file_path:
            self.centralWidget().save(self.opening_file_path)

    def save_as_data(self):
        if self.opening_file_path:
            user_select_path = QFileDialog.getSaveFileName(self,
                                                           "选择另存为路径", "..", "*" + self.centralWidget().file_ext)[0]
            if user_select_path:
                if self.centralWidget().save(user_select_path) == 0:
                    self.opening_file_path = user_select_path
                    self.setWindowTitle(os.path.split(user_select_path)[1])

    def exit(self):
        self.close()

    def center_screen(self):
        desktop_rect = QApplication.primaryScreen().geometry()
        center = desktop_rect.center()
        self.move(center.x() - self.centralWidget().width() * 0.5,
                  center.y() - self.centralWidget().height() * 0.5)

    def adjustSize(self):
        super(QMainWindow, self).adjustSize()
        self.setFixedSize(self.size())
        self.center_screen()
