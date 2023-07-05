from typing import Dict, List, Union
import math
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Variance(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_INT,
        Constants.FIELD_TYPE_FLOAT
    ]
    KEY_NAME = "variance"
    N_CYCLE = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.diff = 0
        self.variance = None
        self.local_exec_flag = False

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        for meta_statistics in workers_meta_list:
            try:
                statistics = meta_statistics.get("statistics", {})
                if not statistics.__contains__("diff"):
                    self.diff = None
                    break
                self.diff += statistics.get("diff")
            except Exception as e:
                raise e

        if self.diff is not None:
            self.variance = self.diff / self.num_instances

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        if meta_statistics.__contains__("average"):
            self.diff += math.pow((float(val) - meta_statistics["average"]), 2)
        else:
            self.diff = None

    def local_to_dict(self) -> Dict:
        if self.diff is not None:
            return {
                "diff": self.diff
            }
        else:
            return {}

    def global_to_dict(self) -> Dict:
        if self.variance is None:
            return {}
        else:
            return {
                self.KEY_NAME: self.variance,
                "std_dev": float(math.sqrt(self.variance))
            }
