from typing import Dict, List, Union
import re
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Word(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_STRING
    ]
    KEY_NAME = "word"
    N_CYCLE = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.word_dict: Dict = dict()
        self.tokenizer = BasicTokenizer()

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        for meta_statistics in workers_meta_list:
            try:
                local_word: Dict = meta_statistics.get("statistics", {})[self.KEY_NAME]
            except Exception as e:
                raise e

            if len(self.word_dict) == 0:
                self.word_dict = local_word
            else:
                for _key in local_word.keys():
                    if self.word_dict.__contains__(_key):
                        self.word_dict[_key] += local_word[_key]
                    else:
                        self.word_dict[_key] = local_word[_key]

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        word_list = self.tokenizer.tokenize(val)

        for word in word_list:
            if not self.word_dict.__contains__(word):
                self.word_dict[word] = 1
            else:
                self.word_dict[word] += 1

    def local_to_dict(self) -> Dict:
        return {self.KEY_NAME: self.word_dict}

    def global_to_dict(self) -> Dict:
        return {
            self.KEY_NAME: self.word_dict
        }


class BasicTokenizer(object):
    def tokenize(self, value: str) -> List[str]:
        data = value.lower()
        key_set = list(set(re.findall(r'[^a-zA-z0-9]|[_]', data)))
        for key in key_set:
            if key != " ":
                data = data.replace(str(key), ' ' + str(key) + ' ').replace("  ", " ")
        data = data.strip()
        data = data.split(" ")
        return data
