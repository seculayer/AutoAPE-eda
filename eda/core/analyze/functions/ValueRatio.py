#  -*- coding: utf-8 -*-
#  Author : Subin Lee
#  e-mail : subin.lee@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import Dict, List, Union
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class ValueRatio(FunctionsAbstract):
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
        Constants.FIELD_TYPE_STRING
    ]
    KEY_NAME = "valueratio"
    N_CYCLE = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """
            self.unique_dict : dict
                "unique" 함수 값
            self.ratio_dict : dict
                결과 값
        """
        self.unique_dict: Dict = dict()
        self.ratio_dict: Dict = dict()

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        """
        Global 수식을 통해 결과를 도출하는 함수, 결과는 self.ratio_dict 변수에 저장
        :param workers_meta_list: list
            worker 들의 meta 데이터(local 계산 결과 등) 정보가 들어 있는 List
        :return: None
        """

        for meta_statistics in workers_meta_list:
            try:
                local_unique = meta_statistics.get("statistics", {})["unique"]["unique"]
            except Exception as e:
                raise e

            for _key in local_unique.keys():
                if self.unique_dict.__contains__(_key):
                    self.unique_dict[_key] += local_unique[_key]
                else:
                    self.unique_dict[_key] = local_unique[_key]

        for _key in self.unique_dict.keys():
            self.ratio_dict[_key] = round(self.unique_dict[_key] / self.num_instances, 2)

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        """
        Local 수식을 통해 결과를 도출하는 함수
        """
        pass

    def local_to_dict(self) -> Dict:
        """
        Local 계산 결과를 반환하는 함수
        """
        return {}

    def global_to_dict(self) -> Dict:
        """
        Global 계산 결과가 저장된 self.ratio_dict 변수를 self.KEY_NAME 변수와 dict 형태로 저장 후 반환
        :return: dict
        """
        return {
            self.KEY_NAME: self.ratio_dict
        }
