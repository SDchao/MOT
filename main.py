from PySide2.QtWidgets import QApplication
import sys
from windows.main_window import MainWindow
from windows.main_widget import MainWidget
import operators.video_operator as video_operator
import json
from windows.preview_item import PreviewItem

app = QApplication(sys.argv)

main_widget = MainWidget()
main_window = MainWindow(main_widget)

# app.setStyleSheet(open("windows/qss/MainStyle.qss", "r").read())

main_window.show()

# preview_list = main_widget.preview_list
# img_l = []
# for i in range(1, 10):
#     img_l.append("windows/images/Default.png")
# preview_list.insert_item(img_l)


# Test info
info_path = "data/group1/info.json"
video_path = "data/group1/videos/"
info = json.load(open(info_path, "r", encoding="utf8"))
main_window.setWindowTitle(info["name"])
main_widget.set_map("data/group1/map.jpg")
cameras_info = info["cameras"]
for camera_info in cameras_info:
    for video in camera_info["videos"]:
        video_info = video_operator.get_video_info(video_path + video)
        if not video_info.no_err:
            print("Unable to find " + video)
            continue
        item = PreviewItem(video_info, camera_info["mapPos"])
        main_widget.preview_list.insert_item(item)

# Center Screen
desktopRect = QApplication.desktop().availableGeometry(main_window)
center = desktopRect.center()
main_window.move(center.x() - main_window.width() * 0.5,
                 center.y() - main_window.height() * 0.5)

sys.exit(app.exec_())
