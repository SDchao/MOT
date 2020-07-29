from PySide2.QtWidgets import QApplication
import sys
from windows.main_window import Main_Window
from windows.main_widget import Main_Widget


app = QApplication(sys.argv)

main_widget = Main_Widget()
main_window = Main_Window(main_widget)
main_window.show()

preview_list = main_widget.preview_list
img_l = []
for i in range(1,10):
    img_l.append("windows/images/Default.png")
preview_list.insert_item(img_l)

sys.exit(app.exec_())