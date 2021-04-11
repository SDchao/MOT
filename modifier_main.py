import sys

from PySide2.QtWidgets import QApplication

from manage_tools.modifier_main_window import ModifierMainWindow
from manage_tools.widgets.data_modifier_widget import DataModifierWidget

app = QApplication(sys.argv)
app.setStyleSheet(open("windows/qss/ModifierStyle.qss", "r").read())

modifier_widget = DataModifierWidget()
main_window = ModifierMainWindow(modifier_widget)
main_window.adjustSize()
main_window.show()

# TEST ONLY
main_window.open_data("data/group1/videos/文-3001-牌坊东小路_2020-07-22_13h38min10s.avi")

sys.exit(app.exec_())
