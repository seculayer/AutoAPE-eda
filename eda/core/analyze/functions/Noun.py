# -*- coding: utf-8 -*-
# Author : JunHyuck Kim
# e-mail : junhyuck.kim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import Dict, List, Union
import numpy as np
import nltk

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract
from eda.core.analyze.functions.Word import BasicTokenizer


class Noun(FunctionsAbstract):
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
        Constants.FIELD_TYPE_STRING
    ]
    KEY_NAME = "noun"
    N_CYCLE = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """
            self.word_dict : dict
                결과 값
            self.word_list : list
                분류된 명사 
            self.tokenizer : Word.py 안에 BasicTokenizer 클래스 호출
        """
        self.word_dict: Dict = dict()
        self.word_list: List = list()
        self.tokenizer = BasicTokenizer()

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        """
            Global 수식을 통해 결과를 도출하는 함수, 결과는 self(인스턴스) 변수에 저장
        :param workers_meta_list: list
            worker 들의 meta 데이터(local 계산 결과 등) 정보가 들어 있는 List
        :return: None
        """
        for meta_statistics in workers_meta_list:
            try:
                local_word: Dict = meta_statistics.get("statistics", {})[self.KEY_NAME]
                if self.word_dict.get('noun') is None:
                    self.word_dict['noun'] = []
                    self.word_dict['noun'].extend(local_word)
                else:
                    self.word_dict['noun'].extend(local_word)
            except Exception as e:
                raise e

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        """
           Local 수식을 통해 결과를 도출하는 함수, 결과는 self(인스턴스) 변수에 저장
       :param val: Union[str, np.array]
           입력 데이터셋 중 한 라인의 특정 컬럼에 해당하는 데이터
       :param meta_statistics: dict
           이전 Cycle의 Global 계산 결과가 포함된 dict 변수, 필요시 참조해서 local 계산에 사용
       :return: None
       """
        word_list = self.tokenizer.tokenize(val)
        tokens_tag = nltk.pos_tag(word_list)
        noun_list: List = list()
        append = noun_list.append
        list(map(lambda n: append(n[0]) if n[0] not in noun_list else None, filter(lambda x: 'NN' in x[1], tokens_tag)))
        # list(map(lambda n : noun_list.append([0]) if n[0] not in noun_list else None, filter(lambda x : 'NN' in x[1], tokens_tag)))

        # for word, pos in tokens_tag:
        #     if 'NN' in pos:
        #         if word not in noun_list:
        #             noun_list.append(word)
        self.word_list.extend(noun_list)

    def local_to_dict(self) -> Dict:
        """
            결과가 저장된 self(인스턴스) 변수들을 dict에 key를 이용하여 저장 후 반환
            해당 함수는 local 계산 결과를 반환할 때 사용
        :return: dict
        """
        return {
            self.KEY_NAME: self.word_list
        }

    def global_to_dict(self) -> Dict:
        """
            결과가 저장된 self(인스턴스) 변수들을 dict에 key를 이용하여 저장 후 반환
            해당 함수는 global 계산 결과를 반환할 때 사용
        :return: dict
        """
        return {
            self.KEY_NAME: self.word_dict['noun']
        }
