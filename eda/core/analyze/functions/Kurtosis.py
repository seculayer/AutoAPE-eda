from typing import Dict, List, Union
import numpy as np
import math

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Kurtosis(FunctionsAbstract):
	AVAILABLE_DTYPE_LIST = [
		Constants.FIELD_TYPE_INT,
		Constants.FIELD_TYPE_FLOAT
	]
	KEY_NAME = "kurtosis"
	N_CYCLE = 3

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.ku_diff = 0
		self.kurtosis = None

	def global_calc(self, workers_meta_list: List[Dict]) -> None:
		ku_diff_sum = 0
		for meta_statistics in workers_meta_list:
			try:
				statistics = meta_statistics.get("statistics", {})
				if not statistics.__contains__("ku_diff"):
					ku_diff_sum = None
					break
				ku_diff_sum += statistics.get("ku_diff")
			except Exception as e:
				raise e

		if ku_diff_sum is not None:
			self.kurtosis = ku_diff_sum / self.num_instances - 3

	def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
		if meta_statistics.__contains__("average") and meta_statistics.__contains__("std_dev"):
			self.ku_diff += math.pow((float(val) - meta_statistics["average"]) / meta_statistics["std_dev"], 4)
		else:
			self.ku_diff = None

	def local_to_dict(self) -> Dict:
		if self.ku_diff is not None:
			return {
				"ku_diff": self.ku_diff
			}
		else:
			return {}

	def global_to_dict(self) -> Dict:
		if self.kurtosis is None:
			return {}
		else:
			return {
				self.KEY_NAME: self.kurtosis
			}

