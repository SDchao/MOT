import sys

from PySide2.QtWidgets import QApplication

from windows.main_window import MainWindow

app = QApplication(sys.argv)

main_window = MainWindow()
# main_widget = MainWidget(desktopRect.width(), desktopRect.height(), main_window)
# main_window.main_widget = main_widget

# compare_widget = CompareWidget(desktopRect.width(), desktopRect.height(), main_window)
# main_window.compare_widget = compare_widget

main_window.set_main_widget()

app.setStyleSheet(open("windows/qss/MainStyle.qss", "r").read())

main_window.show()

# Test info
# main_window.set_data("data/group1_clean")

main_window.adjustSize()

sys.exit(app.exec_())
