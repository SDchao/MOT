import json
from typing import Dict


class ReidContainer(object):
    info: Dict[str, list] = {}

    def __init__(self, info_path):
        info = json.load(open(info_path, "r", encoding="utf8"))
        reids = info["reids"]
        for reid_info in reids:
            self.info[reid_info["name"]] = reid_info["list"]

    def get_reid(self, last_index, raw_id, new_index):
        for (name, id_list) in self.info.items():
            if id_list[last_index] == raw_id:
                return id_list[new_index]

        return -1
