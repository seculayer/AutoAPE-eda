# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from pycmmn.Singleton import Singleton
from pycmmn.utils.ConfUtils import ConfUtils
from pycmmn.utils.FileUtils import FileUtils
from pycmmn.tools.VersionManagement import VersionManagement

import os
os.chdir(FileUtils.get_realpath(__file__) + "/../../")


# class : Constants
class Constants(metaclass=Singleton):
    _working_dir = os.getcwd()
    try:
        VERSION_MANAGER = VersionManagement(app_path=_working_dir)
    except Exception as e:
        # DEFAULT
        VersionManagement.generate(
            version="1.0.0",
            app_path=_working_dir,
            module_nm="eda",
        )
        VERSION_MANAGER = VersionManagement(app_path=_working_dir)
    VERSION = VERSION_MANAGER.VERSION
    MODULE_NM = VERSION_MANAGER.MODULE_NM

    # DATASET FORMAT
    DATASET_FORMAT_TEXT = "1"
    DATASET_FORMAT_IMAGE = "2"
    DATASET_FORMAT_TABLE = "3"

    # FIELD TYPE
    FIELD_TYPE_NULL = "null"
    FIELD_TYPE_INT = "int"
    FIELD_TYPE_FLOAT = "float"
    FIELD_TYPE_STRING = "string"
    FIELD_TYPE_IMAGE = "image"
    FIELD_TYPE_DATE = "date"
    FIELD_TYPE_LIST = "list"

    JOB_TYPE_CHIEF = "chief"
    JOB_TYPE_WORKER = "worker"

    # FIELD TAG
    TAG_CATEGORY = "Categorical"

    DATASET_META_RST_TYPE_ALL = "1"
    DATASET_META_RST_TYPE_LABEL = "2"


if __name__ == '__main__':
    print(Constants.FIELD_TYPE_NULL)
