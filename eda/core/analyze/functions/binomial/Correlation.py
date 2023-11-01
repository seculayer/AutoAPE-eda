from typing import Dict, List, Union
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Correlation(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_INT,
        Constants.FIELD_TYPE_FLOAT
    ]
    KEY_NAME = "correlation"
    N_CYCLE = 3
    DATASET_META_RST_TYPE = Constants.DATASET_META_RST_TYPE_ALL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rst_val = None

    def global_calc(self, workers_meta_list: List[List[Dict]], comparison_idx=None) -> None:
        self.rst_val = 0
        #                    target_column_idx┐  ┌worker_idx
        meta_statistics_1 = workers_meta_list[0][0]
        self.rst_val = meta_statistics_1.get("statistics", {}).get(self.KEY_NAME)[comparison_idx]

    def local_calc(self, val: Union[str, np.array], meta_statistics: List[Dict], comparison_idx=None) -> None:
        if self.rst_val is None:
            self.rst_val = meta_statistics[0].get("covariance")[comparison_idx] / (meta_statistics[0].get("std_dev") * meta_statistics[1].get("std_dev"))

    def local_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.rst_val
        }

    def global_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.rst_val
        }
