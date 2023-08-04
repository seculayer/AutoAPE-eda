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
				ku_diff_sum += meta_statistics.get("statistics", {})["ku_diff"]
			except Exception as e:
				raise e

		if ku_diff_sum is not None:
			self.kurtosis = ku_diff_sum / self.num_instances - 3

	def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
		try:
			self.ku_diff += math.pow((float(val) - meta_statistics["average"]) / meta_statistics["std_dev"], 4)
		except Exception as e:
			raise e

	def local_to_dict(self) -> Dict:
		return {
			"ku_diff": self.ku_diff
		}

	def global_to_dict(self) -> Dict:
		return {
			self.KEY_NAME: self.kurtosis
		}

