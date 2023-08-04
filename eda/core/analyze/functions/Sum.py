from typing import Dict, List, Union
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Sum(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_INT,
        Constants.FIELD_TYPE_FLOAT
    ]
    KEY_NAME = "sum"
    N_CYCLE = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rst_val = 0

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        for meta_statistics in workers_meta_list:
            try:
                self.rst_val += meta_statistics.get("statistics", {})[self.KEY_NAME]
            except Exception as e:
                raise e

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        self.rst_val += float(val)

    def local_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.rst_val
        }

    def global_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.rst_val
        }
