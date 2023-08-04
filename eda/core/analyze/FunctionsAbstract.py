# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2023 AI Service Model Team, R&D Center.
from typing import Dict, List, Union
import numpy as np


class FunctionsAbstract(object):
    AVAILABLE_DTYPE_LIST = list()
    KEY_NAME = None
    N_CYCLE = 1

    def __init__(self, **kwargs):
        self.num_instances: int = kwargs["num_instances"]

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        raise NotImplementedError

    def local_calc(self, val: Union[str, np.array], meta_func: Dict) -> None:
        raise NotImplementedError

    def local_to_dict(self) -> Dict:
        raise NotImplementedError

    def global_to_dict(self) -> Dict:
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self.local_to_dict())

    @classmethod
    def get_available_dtype_list(cls):
        return cls.AVAILABLE_DTYPE_LIST

    @classmethod
    def get_key(cls) -> str:
        return cls.KEY_NAME

    @classmethod
    def get_n_cycle(cls) -> int:
        return cls.N_CYCLE
