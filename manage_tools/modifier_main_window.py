import os

from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog

from manage_tools.widgets.modifier_widget_parent import ModifierWidget


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

    def open_data(self):
        user_select_path = QFileDialog.getOpenFileName(self,
                                                       "选择打开的数据文件", "..", self.centralWidget().file_filter)[0]
        if user_select_path:
            if self.centralWidget().open(user_select_path) == 0:
                self.opening_file_path = user_select_path
                self.save_action.setEnabled(True)
                self.save_as_action.setEnabled(True)
                self.setWindowTitle(os.path.split(user_select_path)[1])

    def save_data(self):
        if self.opening_file_path:
            self.centralWidget().save(self.opening_file_path)

    def save_as_data(self):
        if self.opening_file_path:
            user_select_path = QFileDialog.getSaveFileName(self,
                                                           "选择另存为路径", "..", self.centralWidget().file_filter)[0]
            if user_select_path:
                if self.centralWidget().save(user_select_path) == 0:
                    self.opening_file_path = user_select_path
                    self.setWindowTitle(os.path.split(user_select_path)[1])

    def exit(self):
        self.close()
