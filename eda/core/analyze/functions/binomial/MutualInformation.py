from typing import Dict, List, Union
import math

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class MutualInformation(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_INT,
        Constants.FIELD_TYPE_FLOAT
    ]
    KEY_NAME = "mutual_information"
    N_CYCLE = 1
    DATASET_META_RST_TYPE = Constants.DATASET_META_RST_TYPE_LABEL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unique_dict: Dict = dict()
        self.rst_val = None

    def global_calc(self, workers_meta_list: List[List[Dict]], comparison_idx=None) -> None:
        """
        :param workers_meta_list: List[List[Dict]]
                    2(values count) ┘   └ worker cnt
        :param comparison_idx:
        :return:
        """

        col1_meta_list = workers_meta_list[0]
        col2_meta_list = workers_meta_list[1]

        for meta_statistics in col1_meta_list:
            try:
                unique_list = meta_statistics.get("statistics", {})[self.KEY_NAME]
                joint_unique = unique_list[comparison_idx]

                for i in range(3):
                    if not self.unique_dict.__contains__(f"val_{i}"):
                        self.unique_dict[f"val_{i}"] = dict()
                    for _key, _val in joint_unique[f"val_{i}"].items():
                        if self.unique_dict[f"val_{i}"].__contains__(_key):
                            self.unique_dict[f"val_{i}"][_key] += _val
                        else:
                            self.unique_dict[f"val_{i}"][_key] = _val
            except Exception as e:
                raise e

        entropy_list: List[float] = list()
        for i in range(3):
            entropy_list.append(self._calc_entropy(f"val_{i}"))

        self.rst_val = entropy_list[0] + entropy_list[1] - entropy_list[2]

    def local_calc(self, val: List, meta_statistics: List[Dict], comparison_idx=None) -> None:
        val.append(str(tuple(val)))
        for i in range(3):
            if not self.unique_dict.__contains__(f"val_{i}"):
                self.unique_dict[f"val_{i}"] = dict()
            self._make_local_dict(f"val_{i}", val[i])

    def local_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.unique_dict
        }

    def global_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.rst_val
        }

    def _make_local_dict(self, key, val: float) -> None:
        if not self.unique_dict[key].__contains__(val):
            self.unique_dict[key][val] = 1
        else:
            self.unique_dict[key][val] += 1

    def _calc_entropy(self, _key) -> float:
        entropy = 0.0
        for _count in self.unique_dict[_key].values():
            probability = _count / self.num_instances
            entropy -= probability * math.log2(probability)

        return entropy
