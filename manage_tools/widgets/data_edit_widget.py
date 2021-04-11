from PySide2.QtWidgets import QWidget, QFormLayout, QLineEdit


class DataEditWidget(QWidget):
    _pass_flag = [False]

    def __init__(self):
        super(DataEditWidget, self).__init__()
        edit_form_layout = QFormLayout()
        self.id_edit = QLineEdit()
        self.id_edit.textChanged.connect(self.on_id_changed)
        edit_form_layout.addRow("将ID修改为: ", self.id_edit)
        self.setLayout(edit_form_layout)

    def clear(self):
        self.id_edit.setText("")

    def on_id_changed(self, text):
        try:
            int(text)
            self._pass_flag[0] = True
            self.id_edit.setStyleSheet("color: black;")
        except ValueError:
            self._pass_flag[0] = False
            self.id_edit.setStyleSheet("color: red;")

    def get_data(self):
        if all(self._pass_flag):
            return int(self.id_edit.text())
        else:
            return None
