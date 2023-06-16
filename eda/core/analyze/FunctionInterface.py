from typing import List, Dict, Union
import os

import eda.core.analyze.functions
from eda.common.Common import Common
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract
from eda.core.analyze.functions.Word import Word
from pycmmn.tools.DynamicClassLoader import DynamicClassLoader


class FunctionInterface(object):
    LOGGER = Common.LOGGER.getLogger()

    @staticmethod
    def get_func_name_list() -> List:
        pkg_path = os.path.dirname(eda.core.analyze.functions.__file__)
        file_list = os.listdir(pkg_path)
        rst_list = list()
        for file in file_list:
            if "__" in file:
                continue
            elif ".py" in file:
                file = file.replace(".py", "")
            rst_list.append(file)
        return rst_list

    @staticmethod
    def get_func_cls_list(func_name_list) -> List:
        rst_list = list()

        for func_name in func_name_list:
            func_cls = DynamicClassLoader.load_multi_packages(
                packages=["eda.core.analyze.functions"],
                class_nm=func_name,
                logger=FunctionInterface.LOGGER
            )
            rst_list.append(func_cls)
        return rst_list

    @staticmethod
    def get_available_func_dict(func_cls_list: List[Union[FunctionsAbstract, Word]], dtype: str) -> Dict:
        rst_dict = dict()
        for func_cls in func_cls_list:
            if dtype in func_cls.get_available_dtype_list():
                rst_dict[func_cls.get_key()] = func_cls

        return rst_dict


if __name__ == '__main__':
    lst = FunctionInterface.get_func_name_list()
    print(lst)
    cls_lst = FunctionInterface.get_func_cls_list(lst)
    print(cls_lst)

