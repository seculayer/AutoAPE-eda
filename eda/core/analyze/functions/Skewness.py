#  -*- coding: utf-8 -*-
#  Author : Subin Lee
#  e-mail : subin.lee@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import Dict, List, Union
import math
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Skewness(FunctionsAbstract):
    """
        AVAILABLE_DTYPE_LIST : list
            사용 가능한 Field Type 추가, Constant 클래스 내에서 선택
        KEY_NAME : str
            결과값이 dict 변수에 저장될때 사용할 key
        N_CYCLE : int
            해당 function의 결과가 나오기 까지 반복해야 하는 Cycle 수
            global 계산과 local 계산 한 세트가 1 cycle
    """
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_INT,
        Constants.FIELD_TYPE_FLOAT
    ]
    KEY_NAME = "skewness"
    N_CYCLE = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """
            self.skew_diff : Any
                Local 수식을 통해 도출된 값 
            self.skewness : Any
                결과 값
        """
        self.skew_diff = 0
        self.skewness = None

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        """
        Global 수식을 통해 결과를 도출하는 함수, 결과는 self.skewness 변수에 저장
        :param workers_meta_list: list
            worker 들의 meta 데이터(local 계산 결과 등) 정보가 들어 있는 List
        :return: None
        """
        worker_sum = 0
        for meta_statistics in workers_meta_list:
            try:
                statistics = meta_statistics.get("statistics", {})
                if not statistics.__contains__("skew_diff"):
                    worker_sum = None
                    break
                worker_sum += statistics.get("skew_diff")
            except Exception as e:
                raise e

        if worker_sum is not None:
            self.skewness = worker_sum / self.num_instances

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        """
        Local 수식을 통해 결과를 도출하는 함수, 결과는 self.skew_diff 변수에 저장
        :param val: Union[str, np.array]
            입력 데이터셋 중 한 라인의 특정 컬럼에 해당하는 데이터
        :param meta_statistics: dict
            이전 Cycle의 Global 계산 결과가 포함된 dict 변수(local 계산에 사용)
        :return: None
        """
        if "average" in meta_statistics and "std_dev" in meta_statistics:
            self.skew_diff += math.pow((float(val) - meta_statistics["average"]) / meta_statistics["std_dev"], 3)
        else:
            self.skew_diff = None

    def local_to_dict(self) -> Dict:
        """
        Local 계산 결과를 반환하는 함수
        Local 계산 결과가 저장된 self.skew_diff 변수들을 "skew_diff"라는 key와 dict 형태로 저장 후 반환
        :return: dict
        """
        if self.skew_diff is None:
            return {}
        else:
            return {
                "skew_diff": self.skew_diff
            }

    def global_to_dict(self) -> Dict:
        """
        Global 계산 결과가 저장된 self.skewness 변수를 self.KEY_NAME 변수와 dict 형태로 저장 후 반환
        :return: dict
        """
        if self.skewness is None:
            return {}
        else:
            return {
                self.KEY_NAME: self.skewness
            }
