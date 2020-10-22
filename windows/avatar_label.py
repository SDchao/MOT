from typing import List
import os

from PySide2.QtWidgets import QLabel, QSizePolicy
from PySide2.QtGui import QPixmap, QResizeEvent
from PySide2.QtCore import Qt
from operators.convertor import img_path_2_frame, img_path_2_id
from operators.motlogging import logger


class AvatarLabel(QLabel):
    raw_pixmap: QPixmap = None
    img_list: List[str] = []
    fps: float = 1
    now_img_index = -1
    IMG_ROOT_PATH = "data/group1/image"
    need_update = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(200, 320)
        self.setMaximumSize(250, 400)

        self.setObjectName("AvatarLabel")

    def resizeEvent(self, event: QResizeEvent):
        if self.raw_pixmap:
            self.set_avatar(self.raw_pixmap)

    def set_avatar(self, avatar_path: str) -> None:
        pixmap = QPixmap(avatar_path)
        self.raw_pixmap = pixmap
        new_pixmap = pixmap.scaled(self.maximumWidth(), self.maximumHeight(),
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(new_pixmap)

    def check_avatar_update(self, pos: int, force_update=False):
        pos = round(pos / 1000 * self.fps)
        if self.now_img_index >= 0 and (self.need_update or force_update):
            self.need_update = False
            img_list = self.img_list
            now_pos_dif = abs(pos - img_path_2_frame(img_list[self.now_img_index]))
            result_index = None
            for i in range(len(img_list)):
                pos_dif = pos - img_path_2_frame(img_list[i])
                if pos_dif > 0:
                    if pos_dif < now_pos_dif:
                        result_index = i

            if result_index and result_index != self.now_img_index:
                self.now_img_index = result_index
                self.set_avatar(img_list[result_index])

    def set_id(self, video_index: int, new_id: int):
        self.img_list = []
        video_num = video_index + 1
        img_video_path = self.IMG_ROOT_PATH + "/" + str(video_num)
        img_raw_list = os.listdir(img_video_path)
        for path in img_raw_list:
            path = img_video_path + "/" + path
            if img_path_2_id(path) == new_id:
                self.img_list.append(path)
                self.now_img_index = 0
                self.need_update = True
        logger.info(f"Find new id avatar, has {len(self.img_list)} images")

    def clear_id(self):
        self.now_img_index = -1
        self.img_list = []
        self.setPixmap(QPixmap())

    def get_now_img_path(self):
        if self.now_img_index >= 0:
            return self.img_list[self.now_img_index]
        else:
            return None

    def set_data(self, fps: float):
        self.fps = fps
