from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout, QLabel, QSlider, QLineEdit


class TrackSliderLayout(QHBoxLayout):
    label: QLabel
    slider: QSlider
    line_edit: QLineEdit

    def __init__(self, width):
        QHBoxLayout.__init__(self)

        self.label = QLabel("轨迹显示个数")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(5)
        self.slider.setValue(1)
        self.slider.setFixedWidth(width)
        self.slider.valueChanged.connect(self.__on_slider_max_track_value_changed)

        self.line_edit = QLineEdit()
        self.line_edit.setText("1")
        self.line_edit.setEnabled(False)

        self.addWidget(self.label)
        self.addWidget(self.slider)
        self.addWidget(self.line_edit)

    def __on_slider_max_track_value_changed(self, value):
        self.line_edit.setText(str(value))
