from typing import Dict, List, Union
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract

class MinLength(FunctionsAbstract):
	AVAILABLE_DTYPE_LIST = [
		Constants.FIELD_TYPE_STRING
	]
	KEY_NAME = "minlength"
	N_CYCLE = 1

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.rst_val = float('inf')

	def global_calc(self, workers_meta_list: List[Dict]) -> None:
		for meta_statistics in workers_meta_list:
			try:
				statistics = meta_statistics.get("statistics", {})
				if not statistics.__contains__(self.KEY_NAME):
					break
				local_min = statistics.get(self.KEY_NAME)
			except Exception as e:
				raise e

			if self.rst_val > local_min:
				self.rst_val = local_min

	def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
		if self.rst_val > int(len(val)):
			self.rst_val = int(len(val))

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
