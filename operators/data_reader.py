from operator import attrgetter
from typing import List

from operators.motlogging import logger


class VideoData(object):
    frame: int
    no: int
    vertexes: tuple

    def __init__(self, frame: int, no: int, a: int, b: int, c: int, d: int):
        self.frame = frame
        self.no = no
        self.vertexes = (a, b, c, d)

    def __str__(self):
        return \
            f"{self.frame},{self.no}," \
            f"{self.vertexes[0]},{self.vertexes[1]},{self.vertexes[2]},{self.vertexes[3]},-1,-1,-1,-1"


def read_data(path: str) -> List[VideoData]:
    data_list = []
    try:
        with open(path, "r", encoding="utf8") as f:
            for line in f:
                line = line.strip()
                l_list = line.split(",")

                if line.startswith("#"):
                    continue

                if len(l_list) == 10:
                    data = VideoData(int(l_list[0]), int(l_list[1]), int(l_list[2]), int(l_list[3]), int(l_list[4]),
                                     int(l_list[5]))
                    data_list.append(data)
                else:
                    logger.warning(f"Invalid data in {data_list}: {line}")
        data_list.sort(key=attrgetter("frame"))
        logger.info(f"Read data {path} , found {len(data_list)} lines")
        return data_list
    except IOError as e:
        logger.error("Unable to read data: " + path)
        logger.error(e)
        return []
