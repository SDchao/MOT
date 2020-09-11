from PySide2.QtCore import QPoint, QUrl, QFileInfo, QSize
from PySide2.QtGui import QImage


def str_2_point(pos: str) -> QPoint:
    pos_list = pos.split(" ")
    assert len(pos_list) == 2
    return QPoint(int(pos_list[0]), int(pos_list[1]))


def get_absolute_qurl(path: str) -> QUrl:
    return QUrl.fromLocalFile(QFileInfo(path).absoluteFilePath())


def cv_frame_2_qimage(frame, size: QSize) -> QImage:
    return QImage(frame, size.width(), size.height(), 3 * size.width(),
                  QImage.Format_RGB888).rgbSwapped()
