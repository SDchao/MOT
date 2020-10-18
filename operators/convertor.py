from PySide2.QtCore import QPoint, QUrl, QFileInfo, QSize
from PySide2.QtGui import QImage
import os
import re


def str_2_point(pos: str) -> QPoint:
    pos_list = pos.split(" ")
    assert len(pos_list) == 2
    return QPoint(int(pos_list[0]), int(pos_list[1]))


def get_absolute_qurl(path: str) -> QUrl:
    return QUrl.fromLocalFile(QFileInfo(path).absoluteFilePath())


def cv_frame_2_qimage(frame, size: QSize) -> QImage:
    return QImage(frame, size.width(), size.height(), 3 * size.width(),
                  QImage.Format_RGB888).rgbSwapped()


def img_path_2_frame(path: str) -> int:
    file_name = os.path.splitext(os.path.split(path)[1])[0]
    file_name = file_name[:file_name.find(".")]
    return int(file_name.split("_")[2])


def img_path_2_id(path: str) -> int:
    file_name = os.path.splitext(os.path.split(path)[1])[0]
    file_name = file_name[:file_name.find(".")]
    return int(file_name.split("_")[1])


def txt_path_2_img_path(path: str) -> str:
    match = re.match(r"(.*)reid_data.([0-9])-[0-9]([/\\].*?).txt", path)
    if match:
        return match.group(1) + match.group(2) + match.group(3)
    else:
        return ""
