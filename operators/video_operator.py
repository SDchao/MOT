import cv2
from PySide2.QtGui import QImage
from PySide2.QtCore import QSize
import os


class VideoInfo(object):
    no_err: bool
    preview_image: QImage
    size: QSize
    name: str
    fps: int
    map_pos: tuple

    def __init__(self, no_err: bool, img: QImage = None, size: QSize = None, name: str = None, fps: int = None,
                 map_pos: tuple = None):
        self.no_err = no_err
        self.preview_image = img
        self.size = size
        self.name = name
        self.fps = fps
        assert len(map_pos) == 2
        self.map_pos = map_pos

    def __str__(self):
        return f"""status: {self.no_err}
Size-x: {self.size.width()}
Size-y: {self.size.height()}
name: {self.name}
fps: {self.fps}
mapPos: {self.map_pos}
        """


def get_video_info(video_path: str, map_pos: str = None) -> VideoInfo:
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
    if map_pos:
        pos = tuple(map_pos.split(" "))
        return VideoInfo(True, q_image, size, name, fps, pos)
    return VideoInfo(True, q_image, size, name, fps)
