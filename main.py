from PySide2.QtWidgets import QApplication
import sys
from windows.main_window import Main_Window
from windows.main_widget import Main_Widget


app = QApplication(sys.argv)

mainWindow = Main_Window(Main_Widget())
mainWindow.show()

sys.exit(app.exec_())