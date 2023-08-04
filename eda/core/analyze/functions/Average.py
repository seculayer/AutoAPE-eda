from typing import Dict, List, Union
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Average(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_INT,
        Constants.FIELD_TYPE_FLOAT
    ]
    KEY_NAME = "average"
    N_CYCLE = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rst_val = None

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        worker_sum = 0
        for meta_statistics in workers_meta_list:
            try:
                worker_sum += meta_statistics.get("statistics", {})["sum"]
            except Exception as e:
                raise e

        if worker_sum is not None:
            self.rst_val = worker_sum / self.num_instances

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        pass

    def local_to_dict(self) -> Dict:
        return {}

    def global_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.rst_val
        }
