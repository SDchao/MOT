import cv2
from PySide2.QtGui import QImage
from PySide2.QtCore import QSize, QRect
import os
import re

from typing import List, Union, Tuple
from operator import attrgetter
from operators.convertor import cv_frame_2_qimage
from operators.motlogging import logger


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


class VideoData(object):
    frame: int
    no: int
    vertexes: tuple

    def __init__(self, frame: int, no: int, a: int, b: int, c: int, d: int):
        self.frame = frame
        self.no = no
        self.vertexes = (a, b, c, d)

    def __str__(self):
        return f"""frame: {self.frame}
no: {self.no}
vertexes: {self.vertexes}"""


class VideoDataCollection(object):
    data_list: List[VideoData] = []
    ws_list: List[Tuple[int, int, float]] = []  # [(target id, target wser id, porb)]
    fps: float

    def __init__(self, data_path: str, ws_path: str, fps: float):
        self.fps = fps
        self.data_list = []
        self.ws_list = []
        self.last_index = 0
        # 读取data
        try:
            with open(data_path, "r", encoding="utf8") as f:
                for line in f:
                    line = line.strip()
                    l_list = line.split(",")
                    if len(l_list) == 10:
                        data = VideoData(int(l_list[0]), int(l_list[1]), int(l_list[2]), int(l_list[3]), int(l_list[4]),
                                         int(l_list[5]))
                        self.data_list.append(data)
                    else:
                        logger.error(f"Invalid data in {data_path}: {line}")
            self.data_list.sort(key=attrgetter("frame"))
            logger.info(f"Read data {data_path} , found {len(self.data_list)} lines")
        except IOError as e:
            logger.error("Unable to read data: " + data_path)
            logger.error(e)
        # 读取ws
        try:
            with open(ws_path, "r", encoding="utf8") as f:
                for line in f:
                    line = line.strip()
                    if line[0] == "#":
                        continue

                    # l_list = line.split("<-")
                    l_list = re.split(r"<-|,", line)
                    if len(l_list) == 2:
                        self.ws_list.append((int(l_list[0]), int(l_list[1]), 1.0))
                    elif len(l_list) == 3:
                        self.ws_list.append((int(l_list[0]), int(l_list[1]), float(l_list[2])))
                    else:
                        logger.error(f"Invalid data in {ws_path}: {line}")

                logger.info(f"Read ws {ws_path} , found {len(self.ws_list)} lines")
        except IOError as e:
            logger.error("Unable to read ws: " + ws_path)
            logger.error(e)

    def get_ws_id_list(self, target_id: int) -> List[Tuple[int, float]]:
        result = []
        for ws_info in self.ws_list:
            if target_id == ws_info[0]:
                result.append((ws_info[1], ws_info[2]))

        return result

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


def get_video_info(video_path: str) -> VideoInfo:
    name = os.path.splitext(os.path.split(video_path)[1])[0]
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        return VideoInfo(False)
    size = QSize(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    q_image = cv_frame_2_qimage(frame, size)
    return VideoInfo(True, q_image, size, name, fps, video_path)


def get_video_data(video_path: str, fps: float, use_clean_data) -> VideoDataCollection:
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
