from PySide2.QtCore import QPoint, QUrl, QFileInfo


def str_2_point(pos: str) -> QPoint:
    pos_list = pos.split(" ")
    assert len(pos_list) == 2
    return QPoint(int(pos_list[0]), int(pos_list[1]))


def get_absolute_qurl(path: str) -> QUrl:
    return QUrl.fromLocalFile(QFileInfo(path).absoluteFilePath())
