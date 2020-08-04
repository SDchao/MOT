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

    def __init__(self, no_err: bool, img: QImage = None, size: QSize = None, name: str = None, fps: int = None):
        self.no_err = no_err
        self.preview_image = img
        self.size = size
        self.name = name
        self.fps = fps

    def __str__(self):
        return f"""status: {self.no_err}
Size-x: {self.size.width()}
Size-y: {self.size.height()}
name: {self.name}
fps: {self.fps}
        """


def get_video_info(video_path: str) -> VideoInfo:
    name = os.path.splitext(os.path.split(video_path)[1])[0]
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        return VideoInfo(False)
    size = QSize(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    cap.release()
    qimage = QImage(frame_rgb.data, size.width(), size.height(), 3 * size.width(),
                    QImage.Format_RGB888).rgbSwapped()
    return VideoInfo(True, qimage, size, name, fps)