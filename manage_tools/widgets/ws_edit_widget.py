from PySide2.QtWidgets import QWidget, QFormLayout, QLineEdit

from operators.ws_reader import WsData


class WsEditWidget(QWidget):
    _pass_flag = [False, False, False]

    def __init__(self, parent=None):
        super(WsEditWidget, self).__init__(parent=parent)

        # Line Edits
        self.victim_edit = QLineEdit()
        self.follower_edit = QLineEdit()
        self.prob_edit = QLineEdit()

        self.victim_edit.textChanged.connect(self.on_victim_changed)
        self.follower_edit.textChanged.connect(self.on_follower_changed)
        self.prob_edit.textChanged.connect(self.on_prob_changed)

        self.main_form_layout = QFormLayout()
        self.main_form_layout.addRow("被跟随ID: ", self.victim_edit)
        self.main_form_layout.addRow("跟随ID: ", self.follower_edit)
        self.main_form_layout.addRow("概率: ", self.prob_edit)

        self.setLayout(self.main_form_layout)

    def on_victim_changed(self, text):
        try:
            int(text)
            self._pass_flag[0] = True
            self.victim_edit.setStyleSheet("color: black;")
        except ValueError:
            self._pass_flag[0] = False
            self.victim_edit.setStyleSheet("color: red;")

    def on_follower_changed(self, text):
        try:
            int(text)
            self._pass_flag[1] = True
            self.follower_edit.setStyleSheet("color: black;")
        except ValueError:
            self._pass_flag[1] = False
            self.follower_edit.setStyleSheet("color: red;")

    def on_prob_changed(self, text):
        try:
            prob = float(text)
            if 0 <= prob <= 1:
                self._pass_flag[2] = True
                self.prob_edit.setStyleSheet("color: black;")
            else:
                raise ValueError
        except ValueError:
            self._pass_flag[2] = False
            self.prob_edit.setStyleSheet("color: red;")

    def set_ws_data(self, ws_data: WsData):
        self.victim_edit.setText(str(ws_data.victim))
        self.follower_edit.setText(str(ws_data.follower))
        self.prob_edit.setText(str(ws_data.prob))

    def get_ws_data(self):
        if all(self._pass_flag):
            return WsData(int(self.victim_edit.text()), int(self.follower_edit.text()), float(self.prob_edit.text()))
        else:
            return None
