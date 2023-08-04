# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
from typing import Dict, List, Union
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class ImageShape(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_IMAGE
    ]
    KEY_NAME = "imageshape"
    N_CYCLE = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.width: Dict = {"min": None, "max": None, "mean": 0, "sum": 0}
        self.height: Dict = {"min": None, "max": None, "mean": 0, "sum": 0}
        self.channel: Dict = {"min": None, "max": None, "mean": 0, "sum": 0}
        # self.value: Dict = {"min": None, "max": None, "mean": 0, "sum": 0}

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        img_shape = val.shape
        channel = 1
        if len(img_shape) != 2:
            channel = img_shape[2]
        self.width = self._calc_dict(img_shape[0], self.width)
        self.height = self._calc_dict(img_shape[1], self.height)
        self.channel = self._calc_dict(channel, self.channel)
        # self.value = self._calc_val_dict(val, self.value)

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        self.width = self._calc_global(workers_meta_list, 'width')
        self.height = self._calc_global(workers_meta_list, 'height')
        self.channel = self._calc_global(workers_meta_list, 'channel')

        self.width["mean"] = self.width["sum"] / self.num_instances
        self.height["mean"] = self.height["sum"] / self.num_instances
        self.channel["mean"] = self.channel["sum"] / self.num_instances

    def local_to_dict(self) -> Dict:
        rst: dict = {
            self.KEY_NAME: {
                "width": self.width, "height": self.height, "channel": self.channel,
                # "sum": self.value.get("sum"), "mean": self.value.get("mean"),
                # "max": self.value.get("max"), "min": self.value.get("min")
            }
        }
        return rst

    def global_to_dict(self) -> Dict:
        return self.local_to_dict()

    def _calc_global(self, workers_meta_list: List, key: str) -> Dict:
        global_sum = 0
        global_min = float('inf')
        global_max = float('-inf')

        for meta_statistics in workers_meta_list:
            imageshape_dict = meta_statistics.get("statistics", {}).get(self.KEY_NAME)

            global_sum += imageshape_dict.get(key).get("sum")
            global_min = min(imageshape_dict.get(key).get("min"), global_min)
            global_max = max(imageshape_dict.get(key).get("max"), global_max)

        return {"sum": global_sum, "min": global_min, "max": global_max, "mean": 0}

    @staticmethod
    def _calc_dict(val: int, data_dict) -> Dict:
        if data_dict.get("min") is None:
            data_dict["min"] = val
            data_dict["max"] = val
        else:
            if data_dict["min"] < val:
                data_dict["min"] = val
            if data_dict["max"] > val:
                data_dict["max"] = val
        data_dict["sum"] += val

        return data_dict

    # @staticmethod
    # def _calc_val_dict(image_arr: np.array, data_dict) -> Dict:
    #     im_shape: tuple = image_arr.shape
    #     n_pixel: int = int(np.prod(im_shape))
    #     data_dict["sum"] = int(np.sum(image_arr))
    #     data_dict["mean"] = data_dict["sum"] / n_pixel
    #     data_dict["max"] = int(np.max(image_arr))
    #     data_dict["min"] = int(np.min(image_arr))
    #
    #     return data_dict
