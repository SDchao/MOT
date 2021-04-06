from typing import List, Tuple

from PySide2.QtCore import Qt
from PySide2.QtGui import QPaintEvent, QPainter, QColor
from PySide2.QtWidgets import QWidget


class ProgressBar(QWidget):
    duration: int = 0
    now_position: int = 0
    highlight_positions: List[Tuple[int, int]] = []
    is_pressing = False     # USED BY WIDGET PARENT

    background_color = Qt.black
    played_color = QColor(66, 165, 245)
    highlight_future_color = Qt.yellow
    highlight_played_color = QColor(10, 101, 174)

    def __init__(self, width: int, height: int = 10):
        super(ProgressBar, self).__init__()
        self.setFixedSize(width, height)

        self.setStyleSheet("""border-style: outset;
border-color: #757575;
border-width: 2px;""")

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        height = self.height()

        # Total Duration
        painter.fillRect(0, 0, self.width(), height, self.background_color)

        # Played Position
        played_width = self.__pos_to_x(self.now_position)
        painter.fillRect(0, 0, played_width, height, self.played_color)

        # Highlight
        for highlight in self.highlight_positions:
            x1 = self.__pos_to_x(highlight[0])
            x2 = self.__pos_to_x(highlight[1])

            now_x = played_width

            if x2 <= now_x:
                painter.fillRect(x1, 0, x2 - x1, height, self.highlight_played_color)
            elif x1 <= now_x < x2:
                painter.fillRect(x1, 0, now_x - x1, height, self.highlight_played_color)
                painter.fillRect(now_x, 0, x2 - now_x, height, self.highlight_future_color)
            else:
                painter.fillRect(x1, 0, x2 - x1, height, self.highlight_future_color)

    def update_pos(self, pos: int):
        self.now_position = pos
        self.update()

    def set_highlight(self, highlights: List[Tuple[int, int]]):
        self.highlight_positions = highlights
        self.update()

    def set_duration(self, duration: int):
        self.duration = duration
        self.update()

    def __pos_to_x(self, pos: int):
        if self.duration != 0:
            return int(pos / self.duration * self.width())
        else:
            return 0
