from PySide2.QtMultimediaWidgets import QGraphicsVideoItem
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene
from PySide2.QtCore import Qt, QSizeF

class VideoGraphicsView(QGraphicsView):
    def __init__(self, player, w, h):
        QGraphicsView.__init__(self)
        self.video_scene = QGraphicsScene()
        self.video_item = QGraphicsVideoItem()

        self.setScene(self.video_scene)
        self.setFixedSize(w, h + 4)
        self.video_item.setSize(QSizeF(w, h))
        self.video_scene.setSceneRect(0, 0, w, h)
        self.video_scene.addItem(self.video_item)

        player.setVideoOutput(self.video_item)


        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)