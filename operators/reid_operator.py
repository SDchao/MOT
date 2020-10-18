import json
from typing import Dict
import os

from operators.convertor import img_path_2_id, img_path_2_frame


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


def get_reid_dict(last_index, raw_id, last_frame, new_index, data_root):
    last_num = last_index + 1
    new_num = new_index + 1

    reid_dict = {}

    for interval_num in range(last_num, new_num):
        minimum_pos_dif = -1
        target_data_file = None
        data_root_path = os.path.join(data_root, f"image/reid_data/{interval_num}-{interval_num + 1}")
        data_all_list = os.listdir(data_root_path)
        for data_path in data_all_list:
            if img_path_2_id(data_path) == raw_id:
                now_pos = img_path_2_frame(data_path)
                now_dif = abs(now_pos - last_frame)
                if now_dif < minimum_pos_dif or minimum_pos_dif < 0:
                    minimum_pos_dif = now_dif
                    target_data_file = data_path
        if target_data_file:
            target_data_file = data_root_path + "/" + target_data_file
            reid_dict["origin"] = target_data_file
            try:
                with open(target_data_file, "r", encoding="utf8") as f:
                    content = f.read()
                reid_dict["list"] = content.split("\n")
                last_frame = img_path_2_frame(reid_dict["list"][0])
                raw_id = img_path_2_id(reid_dict["list"][0])
                print(f"Find new ID {raw_id}, based on {reid_dict['origin']}")
            except OSError:
                print(f"Cannot read {target_data_file}")
        else:
            reid_dict["origin"] = None
            reid_dict["list"] = []
            return reid_dict
    return reid_dict
