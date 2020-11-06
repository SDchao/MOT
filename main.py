from PySide2.QtWidgets import QApplication
import sys
from windows.main_window import MainWindow
from windows.main_widget import MainWidget
import operators.video_operator as video_operator
from operators.reid_operator import ReidContainer
import json
from windows.preview_item import PreviewItem
from operators.motlogging import logger

app = QApplication(sys.argv)

desktopRect = QApplication.primaryScreen().geometry()

main_window = MainWindow()
main_widget = MainWidget(desktopRect.width(), desktopRect.height(), main_window)
main_window.main_widget = main_widget
main_window.setCentralWidget(main_widget)

app.setStyleSheet(open("windows/qss/MainStyle.qss", "r").read())

main_window.show()

# Test info
# main_window.set_data("data/group1_clean")

main_window.adjustSize()

sys.exit(app.exec_())
