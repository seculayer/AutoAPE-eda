from typing import Dict, List, Union
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class ClassName(FunctionsAbstract):
    """
        AVAILABLE_DTYPE_LIST : list
            사용 가능한 Field Type 추가, Constant 클래스 내에서 선택
            e.g.) Constants.FIELD_TYPE_INT
        KEY_NAME : str
            결과값이 dict 변수에 저장될때 사용할 key
        N_CYCLE : int
            해당 function의 결과가 나오기 까지 반복해야 하는 Cycle 수
            global 계산과 local 계산 한 세트가 1 cycle
            e.g.) Sum : 1, Max : 1, Min : 1, Average : 2
    """
    AVAILABLE_DTYPE_LIST = []
    KEY_NAME = ""
    N_CYCLE = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """
            self.rst_val : Any
                결과 값
            ※ 필요시 변수 추가
        """
        self.rst_val = None

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        """
            Global 수식을 통해 결과를 도출하는 함수, 결과는 self(인스턴스) 변수에 저장
        :param workers_meta_list: list
            worker 들의 meta 데이터(local 계산 결과 등) 정보가 들어 있는 List
        :return: None
        """

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        """
            Local 수식을 통해 결과를 도출하는 함수, 결과는 self(인스턴스) 변수에 저장
        :param val: Union[str, np.array]
            입력 데이터셋 중 한 라인의 특정 컬럼에 해당하는 데이터
        :param meta_statistics: dict
            이전 Cycle의 Global 계산 결과가 포함된 dict 변수, 필요시 참조해서 local 계산에 사용
        :return: None
        """

    def local_to_dict(self) -> Dict:
        """
            결과가 저장된 self(인스턴스) 변수들을 dict에 key를 이용하여 저장 후 반환
            해당 함수는 local 계산 결과를 반환할 때 사용
        :return: dict
        """
        return {}

    def global_to_dict(self) -> Dict:
        """
            결과가 저장된 self(인스턴스) 변수들을 dict에 key를 이용하여 저장 후 반환
            해당 함수는 global 계산 결과를 반환할 때 사용
        :return: dict
        """
        return {}
