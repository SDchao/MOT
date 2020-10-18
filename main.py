from PySide2.QtWidgets import QApplication
import sys
from windows.main_window import MainWindow
from windows.main_widget import MainWidget
import operators.video_operator as video_operator
from operators.reid_operator import ReidContainer
import json
from windows.preview_item import PreviewItem

app = QApplication(sys.argv)

desktopRect = QApplication.primaryScreen().geometry()

main_window = MainWindow()
main_widget = MainWidget(desktopRect.width(), desktopRect.height(), main_window)
main_window.setCentralWidget(main_widget)

app.setStyleSheet(open("windows/qss/MainStyle.qss", "r").read())

main_window.show()

# Test info
info_path = "data/group1/info.json"
reid_container = ReidContainer(info_path)
video_path = "data/group1/videos/"
info = json.load(open(info_path, "r", encoding="utf8"))
main_window.setWindowTitle(info["name"])
cameras_info = info["cameras"]
map_poses = info["mapPos"]
main_widget.map_label.set_map("data/group1/map.jpg", map_poses)
main_widget.set_reid_container(reid_container)

video_item_dict = {}

for camera_info in cameras_info:
    for video in camera_info["videos"]:
        video_name = video[0]
        video_index = video[1]
        video_info = video_operator.get_video_info(video_path + video_name)
        if not video_info.no_err:
            print("Unable to find " + video_name)
            continue
        index = int(camera_info["mapPosIndex"])
        item = PreviewItem(video_info, map_poses[index])
        # main_widget.add_video(item)
        video_item_dict[video_index] = item

video_index_list = list(video_item_dict.keys())
video_index_list.sort()
for index in video_index_list:
    main_widget.add_video(video_item_dict[index])

main_window.adjustSize()

sys.exit(app.exec_())
