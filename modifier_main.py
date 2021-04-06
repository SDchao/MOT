import sys

from PySide2.QtWidgets import QApplication

from manage_tools.modifier_main_window import ModifierMainWindow
from manage_tools.widgets.ws_modifier_widget import WsModifyWidget

app = QApplication(sys.argv)
app.setStyleSheet(open("windows/qss/ModifierStyle.qss", "r").read())

ws_modifier_widget = WsModifyWidget()
main_window = ModifierMainWindow(ws_modifier_widget)
main_window.adjustSize()
main_window.show()

# TEST ONLY
main_window.open_data("data/group1_clean/videos/文-3001-牌坊东小路_2020-07-22_13h38min10s.avi")

sys.exit(app.exec_())
