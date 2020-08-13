import cv2
from PySide2.QtGui import QImage
from PySide2.QtCore import QSize
import os

from typing import List
from operator import attrgetter


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
    fps: float

    def __init__(self, data_path: str, fps: float):
        self.fps = fps
        self.data_list = []

        self.last_index = 0
        try:
            with open(data_path, "r") as f:
                for line in f:
                    line = line.strip()
                    l_list = line.split(",")
                    if len(l_list) == 10:
                        data = VideoData(int(l_list[0]), int(l_list[1]), int(l_list[2]), int(l_list[3]), int(l_list[4]),
                                         int(l_list[5]))
                        self.data_list.append(data)
            self.data_list.sort(key=attrgetter("frame"))
            print(f"Read data {data_path} , found {len(self.data_list)} lines")
        except IOError as e:
            print("Unable to read data: " + data_path)
            print(e)

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

        # make i to first same frame index
        while self.data_list[i].frame < now_frame:
            i += 1

        self.last_index = i

        while self.data_list[i].frame == now_frame:
            result.append(self.data_list[i])
            i += 1

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
    q_image = QImage(frame, size.width(), size.height(), 3 * size.width(),
                     QImage.Format_RGB888).rgbSwapped()
    return VideoInfo(True, q_image, size, name, fps, video_path)


def get_video_data(video_path: str, fps: float) -> VideoDataCollection:
    data_path = os.path.splitext(video_path)[0] + ".data"
    return VideoDataCollection(data_path, fps)
