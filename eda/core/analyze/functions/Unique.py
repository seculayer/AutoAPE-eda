# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
from typing import Dict, List, Union
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Unique(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_INT,
        Constants.FIELD_TYPE_STRING
    ]
    KEY_NAME = "unique"
    N_CYCLE = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.unique_dict: Dict = dict()
        self.unique_count: int = 0
        self._is_category: bool = True

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        for meta_statistics in workers_meta_list:
            local_unique = meta_statistics.get("statistics", {}).get(self.KEY_NAME, {}).get(self.KEY_NAME, {})
            for _key in local_unique.keys():
                if self.unique_dict.__contains__(_key):
                    self.unique_dict[_key] += local_unique[_key]
                else:
                    self.unique_dict[_key] = local_unique[_key]
        self.unique_count = len(self.unique_dict)

        self._check_category()

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        if self._is_category:
            if not self.unique_dict.__contains__(val):
                self.unique_dict[val] = 1
                self.unique_count += 1
            else:
                self.unique_dict[val] += 1

            self._check_category()

    def local_to_dict(self) -> Dict:
        if self._is_category:
            return {
                self.KEY_NAME: {
                    self.KEY_NAME: self.unique_dict,
                    "unique_count": self.unique_count
                }
            }
        return {}

    def global_to_dict(self) -> Dict:
        if self._is_category:
            return {
                self.KEY_NAME: {
                    self.KEY_NAME: self.unique_dict,
                    "unique_count": self.unique_count
                }
            }
        else:
            return {}

    def __str__(self):
        return str(self.unique_dict)

    def _check_category(self) -> None:
        if self.unique_count / self.num_instances > 0.4:
            self._is_category = False

    def is_category(self):
        return self._is_category
