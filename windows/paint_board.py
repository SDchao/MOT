from typing import List, Dict, Optional

import psutil
from PySide2.QtCore import Qt, QSize, QRect, QPoint
from PySide2.QtGui import QPainter, QPen, QFont, QFontMetrics, QMouseEvent, QColor
from PySide2.QtWidgets import QWidget, QSlider

import operators.video_operator as video_operator
from operators.convertor import img_path_2_id, txt_path_2_img_path
from operators.motlogging import logger
from operators.reid_operator import get_reid_dict
from operators.video_operator import VideoDataCollection
from operators.ws_reader import WsData
from windows.avatar_label import AvatarLabel
from windows.track_widget import TrackWidget


def prob_to_color(prob: float) -> QColor:
    if prob < 0.2:
        return Qt.blue
    elif prob < 0.3:
        return Qt.yellow
    elif prob < 0.4:
        return QColor(255, 153, 0)
    elif prob < 0.5:
        return QColor(255, 192, 203)
    else:
        return Qt.red


class PaintBoard(QWidget):
    now_data_collection: VideoDataCollection
    user_selected_id: int = -1
    selecting_ids: list = []
    selecting_colors: list = []
    ws_list: list = []
    now_info: List[List] = []
    showing_info: List = []  # 正在展示的信息，[QRect, id， color]
    now_time: int = 0
    total_time: int = 0
    kw: float = 1
    kh: float = 1
    text_offset = [30, 30]
    font = QFont("Microsoft YaHei", 12)
    dash_font = QFont("Terminal", 15)
    metrics = QFontMetrics(font)
    last_raw_size: QSize = None
    track_widget: TrackWidget = None
    avatar_label: AvatarLabel = None
    init_show_all: bool = False

    color_list = [Qt.green, Qt.red, Qt.blue, Qt.cyan, Qt.magenta]

    track_max_count: int = -1
    max_track_slider: QSlider

    _last_cpu_call_time = 0
    _last_cpu: str = "CPU: 0.0%"

    @property
    def last_cpu_call_time(self):
        return PaintBoard._last_cpu_call_time

    @property
    def last_cpu(self):
        return PaintBoard._last_cpu

    @last_cpu_call_time.setter
    def last_cpu_call_time(self, value):
        PaintBoard._last_cpu_call_time = value

    @last_cpu.setter
    def last_cpu(self, value):
        PaintBoard._last_cpu = value

    def __init__(self, parent=None, track_view=None, init_show_all=False):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setPalette(Qt.transparent)
        self.track_widget = track_view
        self.init_show_all = init_show_all

    def set_avatar_label(self, avatar_label):
        self.avatar_label = avatar_label

    def set_max_track_slider(self, max_track_slider: QSlider):
        self.max_track_slider = max_track_slider

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen()

        if hasattr(self, "now_data_collection"):
            data_list_in_frame = self.now_data_collection.get_data_by_time(self.now_time)
            self.now_info = []
            self.showing_info = []
            now_color_list = self.selecting_colors if self.selecting_colors else self.color_list
            for data in data_list_in_frame:
                show_rect = QRect(data.vertexes[0] * self.kw, data.vertexes[1] * self.kh, data.vertexes[2] * self.kw,
                                  data.vertexes[3] * self.kh)
                self.now_info.append([show_rect, data.no])

                # 若不在选定ID中则不再绘制
                if data.no not in self.selecting_ids:
                    # 若Select ID不为空或未规定空时显示全部
                    if self.selecting_ids or not self.init_show_all:
                        continue

                if data.no in self.selecting_ids:
                    color = now_color_list[self.selecting_ids.index(data.no) % len(now_color_list)]
                else:
                    color = now_color_list[data.no % len(now_color_list)]

                self.showing_info.append([show_rect, data.no, color])
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
            points: Dict[int, List[QPoint, QColor]] = {}
            now_count = -1  # 确保目标进入轨迹显示

            # 添加目标id
            for now_id in self.selecting_ids:
                for info in self.showing_info:
                    if info[1] == now_id:
                        rect: QRect = info[0]
                        points[info[1]] = [rect.center(), info[2]]
                        break

                now_count += 1
                if now_count >= self.track_max_count > 0:
                    break

            self.track_widget.add_points(points)

        # 绘制dashboard
        if self.now_time > 0:
            painter.setFont(self.dash_font)
            painter.setPen(Qt.green)
            painter.setBrush(Qt.black)
            block_length = 15
            block_per_line = 3
            all_text_list = []

            # CPU
            p = psutil.Process()
            if self.now_time - self.last_cpu_call_time > 300:
                cpu_usage = f"CPU: {psutil.cpu_percent()}%"
                self.last_cpu = cpu_usage
                self.last_cpu_call_time = self.now_time
            else:
                cpu_usage = self.last_cpu
            all_text_list.append(cpu_usage)

            # MEM
            mem_percentage_str = format(p.memory_percent("vms"), ".2f")
            mem_usage = f"MEM: {mem_percentage_str}%"
            all_text_list.append(mem_usage)

            # PRG
            progress = ""
            if self.total_time > 0:
                progress_percentage_str = format(self.now_time / self.total_time * 100, ".2f") + "%"
                progress = f"PRG: {self.now_time} / {self.total_time} ({progress_percentage_str})"
            all_text_list.append(progress)

            # ws prob
            now_count = 0
            for ws_item in self.ws_list:
                all_text_list.append(f"ws {ws_item[0]}: {ws_item[1]}")
                now_count += 1
                if now_count >= self.track_max_count > 0:
                    break

            all_text = "   "
            now_line_count = 0
            for text in all_text_list:
                all_text += text.ljust(block_length, " ")
                now_line_count += 1
                if now_line_count >= block_per_line:
                    all_text += "\n   "
                    now_line_count = 0

            if not all_text.endswith("\n   "):
                all_text += "\n   "

            # Drawing
            painter.drawText(self.rect(), Qt.AlignLeft | Qt.AlignBottom, all_text)

    def read_data(self, video_path: str, fps: float, use_clean_data: bool = False):
        if hasattr(self, "now_data_collection"):
            del self.now_data_collection
        self.now_data_collection = video_operator.get_video_data(video_path, fps, use_clean_data)

    def set_now_time(self, now_time: int):
        self.now_time = now_time

    def set_total_time(self, total_time: int):
        self.total_time = total_time

    def set_raw_size(self, raw_size: QSize):
        self.last_raw_size = raw_size
        self.kw = self.size().width() / raw_size.width()
        self.kh = self.size().height() / raw_size.height()

    def update_k(self):
        if self.last_raw_size:
            self.kw = self.size().width() / self.last_raw_size.width()
            self.kh = self.size().height() / self.last_raw_size.height()

    def renew_select(self, last_index: int, new_index: int, last_pos: int, last_fps: float, data_root: str,
                     ws_mode=True):
        if self.selecting_ids:
            now_id = self.user_selected_id
            # if self.reid_container:
            #     new_id = self.reid_container.get_reid(last_index, now_id, new_index)
            #     if new_id > 0:
            #         self.__set_id(new_id)
            #         print(f"Reid {now_id} -> {new_id}")
            #     else:
            #         self.selecting_ids = []
            # else:
            #     self.selecting_ids = []
            now_frame = round(last_pos / 1000 * last_fps)
            reid_dict = get_reid_dict(last_index, now_id, now_frame, new_index, data_root)
            if "list" in reid_dict and reid_dict["list"]:
                new_id = img_path_2_id(reid_dict["list"][0])
                self.set_id(new_id, ws_mode)
                origin_img_path = txt_path_2_img_path(reid_dict["origin"])
                self.avatar_label.set_avatar(origin_img_path)
                # self.avatar_label.set_id(new_index, new_id)
                logger.info(f"REID: {now_id} -> {new_id}")
            else:
                self.selecting_ids = []
                self.avatar_label.clear_id()
                logger.info(f"REID: no paring id, clearing")

    def set_id(self, target_id: int, ws_mode=True):
        self.user_selected_id = target_id
        self.selecting_ids = []
        self.selecting_colors = []
        self.ws_list = []
        if ws_mode:
            ws_list = self.now_data_collection.get_ws_id_list(target_id)  # [(wser id, prob)]
            if ws_list:
                # sort ws list
                ws_list.sort(key=lambda elem: elem[1], reverse=True)
                # Add target id in list
                self.selecting_ids.append(target_id)
                self.selecting_colors.append(Qt.green)
                # Add wser
                for ws_info in ws_list:
                    if ws_info[1] > 0.1:
                        self.selecting_ids.append(ws_info[0])
                        self.selecting_colors.append(prob_to_color(ws_info[1]))
                        self.ws_list.append((ws_info[0], ws_info[1]))
                        logger.info(f"Find wser {ws_info[0]}, prob: {ws_info[1]}")

                if self.max_track_slider.value() > len(self.ws_list):
                    self.max_track_slider.setValue(len(self.ws_list))
                self.max_track_slider.setMaximum(len(self.ws_list))
            else:
                self.selecting_ids.append(target_id)
        else:
            self.selecting_ids.append(target_id)
        logger.info(f"Targeting new id {self.selecting_ids}")

    def set_ws_focus(self, ws_data: WsData):
        self.clear_id()
        self.selecting_ids = [ws_data.victim, ws_data.follower]
        self.selecting_colors = [Qt.green, prob_to_color(ws_data.prob)]
        logger.info(f"Targeting ws: {ws_data}")

    def set_ids(self, targets: List[int]):
        self.clear_id()
        self.selecting_ids = targets
        logger.info(f"Targeting new ids {self.selecting_ids}")

    def on_click(self, event: QMouseEvent, ws_mode=True) -> Optional[int]:
        click_point = event.pos()
        if self.track_widget:
            self.track_widget.clear()
        for info in self.now_info:
            rect: QRect = info[0]
            if rect.contains(click_point):
                target_id = info[1]
                self.set_id(target_id, ws_mode)
                return target_id

        self.selecting_ids = []
        self.user_selected_id = -1
        return None

    def clear_id(self):
        if self.track_widget:
            self.track_widget.clear()

        if self.avatar_label:
            self.avatar_label.clear_id()

        self.selecting_ids = []
        self.selecting_colors = []
        self.user_selected_id = -1

    def set_track_max_count(self, value):
        self.track_max_count = value
