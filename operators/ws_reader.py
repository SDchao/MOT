import re
from typing import List, NamedTuple

from operators.motlogging import logger


class WsData(NamedTuple):
    victim: int
    follower: int
    prob: float = 1.0

    def __str__(self):
        return f"{self.victim}<-{self.follower},{self.prob}"


def read_ws(file_path: str) -> List[WsData]:
    ws_list = []
    try:
        with open(file_path, "r", encoding="utf8") as f:
            for line in f:
                line = line.strip()
                if not line or line[0] == "#":
                    continue

                l_list = re.split(r"<-|,", line)
                try:
                    if len(l_list) == 2:
                        ws_list.append(WsData(int(l_list[0]), int(l_list[1]), 1.0))
                    elif len(l_list) == 3:
                        ws_list.append(WsData(int(l_list[0]), int(l_list[1]), float(l_list[2])))
                    else:
                        raise ValueError
                except ValueError:
                    logger.error(f"Invalid data in {file_path}: {line}")
            logger.info(f"Read ws {file_path} , found {len(ws_list)} lines")
    except IOError as e:
        logger.error("Unable to read ws: " + file_path)
        logger.error(e)
        return []
    return ws_list
