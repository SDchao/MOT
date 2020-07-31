from PySide2.QtWidgets import QMainWindow, QAction
from PySide2.QtCore import Slot
import sys


class Main_Window(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)

        self.setWindowTitle("MOT")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("文件")
        # File
        ## Exit
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)

        # Help
        self.help_menu = self.menu.addMenu("帮助")
        ## About
        about_action = QAction("关于", self)
        self.help_menu.addAction(about_action)

        # Status
        self.status = self.statusBar()
        self.status.showMessage("准备就绪")

        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self):
        sys.exit()
