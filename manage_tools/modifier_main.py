import sys

from PySide2.QtWidgets import QApplication

from manage_tools.modifier_main_window import ModifierMainWindow
from manage_tools.widgets.ws_modifier_widget import WsModifyWidget

app = QApplication(sys.argv)

ws_modifier_widget = WsModifyWidget()
main_window = ModifierMainWindow(ws_modifier_widget)
main_window.show()
sys.exit(app.exec_())
