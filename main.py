from PySide2.QtWidgets import QApplication
import sys
from windows.main_window import MainWindow
from windows.main_widget import MainWidget

app = QApplication(sys.argv)

main_widget = MainWidget()
main_window = MainWindow(main_widget)

app.setStyleSheet(open("windows/qss/MainStyle.qss", "r").read())

main_window.show()

preview_list = main_widget.preview_list
img_l = []
for i in range(1, 10):
    img_l.append("windows/images/Default.png")
preview_list.insert_item(img_l)

# Center Screen
desktopRect = QApplication.desktop().availableGeometry(main_window)
center = desktopRect.center()
main_window.move(center.x() - main_window.width() * 0.5,
                 center.y() - main_window.height() * 0.5)

sys.exit(app.exec_())
