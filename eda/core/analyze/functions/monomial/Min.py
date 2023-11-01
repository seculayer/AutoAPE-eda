from typing import Dict, List, Union
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Min(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_INT,
        Constants.FIELD_TYPE_FLOAT
    ]
    KEY_NAME = "min"
    N_CYCLE = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rst_val = float('inf')

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        for meta_statistics in workers_meta_list:
            try:
                local_min = meta_statistics.get("statistics", {})[self.KEY_NAME]
            except Exception as e:
                raise e

            if self.rst_val > local_min:
                self.rst_val = local_min

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        if self.rst_val > float(val):
            self.rst_val = float(val)

    def local_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.rst_val
        }

    def global_to_dict(self) -> Dict:
        if self.rst_val == float('inf'):
            return {}
        else:
            return {
                self.KEY_NAME: self.rst_val
            }
