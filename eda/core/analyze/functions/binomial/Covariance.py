from typing import Dict, List, Union
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Covariance(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_INT,
        Constants.FIELD_TYPE_FLOAT
    ]
    KEY_NAME = "covariance"
    N_CYCLE = 2
    DATASET_META_RST_TYPE = Constants.DATASET_META_RST_TYPE_ALL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rst_val = None

    def global_calc(self, workers_meta_list: List[List[Dict]], comparison_idx=None) -> None:
        worker_sum = 0
        for meta_statistics in workers_meta_list[0]:
            try:
                covariance_list = meta_statistics.get("statistics", {})[self.KEY_NAME]
                worker_sum += covariance_list[comparison_idx]
            except Exception as e:
                raise e

        self.rst_val = worker_sum / self.num_instances

    def local_calc(self, val: Union[str, np.array], meta_statistics: List[Dict], comparison_idx=None) -> None:
        if self.rst_val is None:
            self.rst_val = 0

        self.rst_val += (float(val[0]) - meta_statistics[0].get("average")) * (float(val[1]) - meta_statistics[1].get("average"))

    def local_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.rst_val
        }

    def global_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.rst_val
        }
