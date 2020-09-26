from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QSize, QRect, QPoint
from PySide2.QtGui import QPainter, QPen, QFont, QFontMetrics, QMouseEvent
from typing import List, Dict

from operators.video_operator import VideoDataCollection, VideoData
from operators.reid_operator import ReidContainer
import operators.video_operator as video_operator
from windows.track_widget import TrackWidget


class PaintBoard(QWidget):
    now_data_collection: VideoDataCollection
    reid_container: ReidContainer = None
    selecting_ids: list = []
    now_info: List[List] = []
    showing_info: List = []
    now_time: int = 0
    kw: float = 1
    kh: float = 1
    text_offset = [30, 30]
    font = QFont("Microsoft YaHei", 12)
    metrics = QFontMetrics(font)
    last_raw_size: QSize = None
    track_widget: TrackWidget = None
    init_show_all: bool = False

    color_list = [Qt.green, Qt.red, Qt.blue, Qt.cyan, Qt.magenta, Qt.gray]

    def __init__(self, parent=None, track_view=None, init_show_all=False):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setPalette(Qt.transparent)
        self.track_widget = track_view
        self.init_show_all = init_show_all

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen()

        if hasattr(self, "now_data_collection"):
            data_list_in_frame = self.now_data_collection.get_data_by_time(self.now_time)
            self.now_info = []
            self.showing_info = []
            for data in data_list_in_frame:
                show_rect = QRect(data.vertexes[0] * self.kw, data.vertexes[1] * self.kh, data.vertexes[2] * self.kw,
                                  data.vertexes[3] * self.kh)
                self.now_info.append([show_rect, data.no])

                # 若不在选定ID中则不再绘制
                if data.no not in self.selecting_ids:
                    # 若Select ID不为空或未规定空时显示全部
                    if self.selecting_ids or not self.init_show_all:
                        continue

                self.showing_info.append([show_rect, data.no])
                if data.no in self.selecting_ids:
                    color = self.color_list[self.selecting_ids.index(data.no) % len(self.color_list)]
                else:
                    color = self.color_list[data.no % len(self.color_list)]
                # 设置笔刷
                pen.setColor(color)
                pen.setWidth(3)
                pen.setCapStyle(Qt.RoundCap)

                painter.setPen(pen)
                painter.setFont(self.font)

                painter.drawRect(show_rect)
                # text_point = [vertexes[0] + self.text_offset[0], vertexes[1] + self.text_offset[1]]

                text_w = self.metrics.width(str(data.no))
                text_h = self.metrics.height()
                text_rect = QRect(show_rect.x(), show_rect.y(), text_w, text_h)
                painter.fillRect(show_rect.x(), show_rect.y(), text_w, text_h, color)
                painter.setPen(Qt.white)
                painter.drawText(text_rect, Qt.AlignCenter, str(data.no))
                # painter.drawRect(1, 1, 157, 452)
        if self.track_widget:
            points: Dict[int, QPoint] = {}
            for info in self.showing_info:
                rect: QRect = info[0]
                points[info[1]] = rect.center()

            self.track_widget.add_points(points)

    def read_data(self, video_path: str, fps: float):
        if hasattr(self, "now_data_collection"):
            del self.now_data_collection
        self.now_data_collection = video_operator.get_video_data(video_path, fps)

    def set_now_time(self, now_time: int):
        self.now_time = now_time

    def set_raw_size(self, raw_size: QSize):
        self.last_raw_size = raw_size
        self.kw = self.size().width() / raw_size.width()
        self.kh = self.size().height() / raw_size.height()

    def update_k(self):
        if self.last_raw_size:
            self.kw = self.size().width() / self.last_raw_size.width()
            self.kh = self.size().height() / self.last_raw_size.height()

    def renew_select(self, last_index: int, new_index: int):
        if self.selecting_ids:
            now_id = self.selecting_ids[0]
            if self.reid_container:
                new_id = self.reid_container.get_reid(last_index, now_id, new_index)
                if new_id > 0:
                    self.__set_id(new_id)
                    print(f"Reid {now_id} -> {new_id}")
                else:
                    self.selecting_ids = []
            else:
                self.selecting_ids = []

    def __set_id(self, target_id: int):
        self.selecting_ids = []
        ws_list = self.now_data_collection.get_ws_id_list(target_id)
        if ws_list:
            for new_id in ws_list:
                self.selecting_ids.append(new_id)
        else:
            self.selecting_ids.append(target_id)

    def on_click(self, event: QMouseEvent):
        click_point = event.pos()
        if self.track_widget:
            self.track_widget.clear()
        for info in self.now_info:
            rect: QRect = info[0]
            if rect.contains(click_point):
                target_id = info[1]
                self.__set_id(target_id)
                return

        self.selecting_ids = []
