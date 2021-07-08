import os
from typing import List, Union, Tuple

import cv2
from PySide2.QtCore import QSize, QRect
from PySide2.QtGui import QImage

from operators.convertor import cv_frame_2_qimage
from operators.data_reader import VideoData, read_data
from operators.ws_reader import read_ws


class VideoInfo(object):
    no_err: bool
    preview_image: QImage
    size: QSize
    name: str
    fps: float
    path: str

    def __init__(self, no_err: bool, img: QImage = None, size: QSize = None, name: str = None, fps: float = None,
                 path: str = None):
        self.no_err = no_err
        self.preview_image = img
        self.size = size
        self.name = name
        self.fps = fps
        self.path = path

    def __str__(self):
        return f"""status: {self.no_err}
Size-x: {self.size.width()}
Size-y: {self.size.height()}
name: {self.name}
fps: {self.fps}
        """


class VideoDataCollection(object):
    data_list: List[VideoData] = []
    ws_list: List[Tuple[int, int, float]] = []  # [(target id, target wser id, porb)]
    fps: float

    def __init__(self, data_path: str, ws_path: str, fps: float):
        self.fps = fps
        self.data_list = []
        self.ws_list = []
        self.last_index = 0

        self.data_list = read_data(data_path)

        self.ws_list = read_ws(ws_path)

    def get_ws_id_list(self, target_id: int) -> List[Tuple[int, float]]:
        result = []
        for ws_info in self.ws_list:
            if target_id == ws_info[0]:
                result.append((ws_info[1], ws_info[2]))

        return result

    def update_data(self, new_data: List[VideoData]):
        self.data_list = new_data

    def get_data_by_time(self, time: int) -> List[VideoData]:

        if not self.data_list:
            return []

        now_sec = time / 1000
        now_frame = round(now_sec * self.fps)
        result = []
        # wrong last_index
        if self.last_index >= len(self.data_list):
            self.last_index = 0

        i = self.last_index
        found = False
        while i < len(self.data_list):
            if self.data_list[i].frame == now_frame:
                if not found:
                    self.last_index = i
                    found = True
                result.append(self.data_list[i])
            elif self.data_list[i].frame > now_frame:
                break
            i += 1

        if not found:
            self.last_index = 0

        return result

    def get_first_show_time(self, target_id: int):
        for data in self.data_list:
            if data.no == target_id:
                return round(data.frame / self.fps * 1000)

        return 0

    def get_highlight(self, target_id: int) -> List[Tuple[int, int]]:
        shown = False
        shown_in_frame = False
        now_frame = -1
        start = -1

        result = []
        for data in self.data_list:
            if data.frame > now_frame:
                # 如果已经在这帧出现但之前未出现
                if shown_in_frame and not shown:
                    start = now_frame
                    shown = True
                # 如果已经出现但这帧没有出现
                elif shown and not shown_in_frame:
                    shown = False
                    result.append((self.__f2p(start), self.__f2p(now_frame)))
                now_frame = data.frame
                shown_in_frame = False

            if data.no == target_id:
                shown_in_frame = True

        if shown:
            result.append((self.__f2p(start), self.__f2p(now_frame)))

        return result

    def __f2p(self, frame):
        return round(frame / self.fps * 1000)


def get_video_info(video_path: str) -> VideoInfo:
    name = os.path.splitext(os.path.split(video_path)[1])[0]
    cap = cv2.VideoCapture(video_path)

    ret = False
    frame = None

    for i in range(10):
        ret, frame = cap.read()
        if ret:
            break

    if not ret:
        return VideoInfo(False)
    size = QSize(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    q_image = cv_frame_2_qimage(frame, size)
    return VideoInfo(True, q_image, size, name, fps, video_path)


def get_video_data(video_path: str, fps: float, use_clean_data=False) -> VideoDataCollection:
    head_path = os.path.splitext(video_path)[0]
    data_path = head_path + ".data"
    if use_clean_data:
        data_path += "m"
        ws_path = os.path.split(video_path)[0] + "\\clean.wsm"
    else:
        ws_path = head_path + ".ws"
    return VideoDataCollection(data_path, ws_path, fps)


def get_video_shot(video_path: str, pos: int, rect: QRect) -> Union[None, QImage]:
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
    success, frame = cap.read()
    if not success:
        return None
    size = QSize(rect.width(), rect.height())
    cropped = frame[rect.y():rect.y() + rect.height(), rect.x():rect.x() + rect.width()]
    cropped = cropped.copy(order="C")
    qimage = cv_frame_2_qimage(cropped, size)
    return qimage
