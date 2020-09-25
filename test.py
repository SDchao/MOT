import operators.video_operator as video_operator
from PySide2.QtCore import QRect

rect = QRect(719, 211, 79, 315)
video_operator.get_video_shot("data/group1/videos/文-3001-牌坊东小路_2020-07-22_13h38min10s.avi", 457, rect)
