# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.

from datetime import datetime
from typing import Union, Dict, List
import numpy as np

from eda.common.Constants import Constants
from eda.core.analyze.FunctionsAbstract import FunctionsAbstract


class Date(FunctionsAbstract):
    AVAILABLE_DTYPE_LIST = [
        Constants.FIELD_TYPE_DATE
    ]
    KEY_NAME = "date"
    N_CYCLE = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.start: Union[datetime, None] = None
        self.end: Union[datetime, None] = None
        self.date_format_list = ["%Y%m%d%H%M%S", "%Y%m%d%H%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
        self.date_format_idx = None

    def global_calc(self, workers_meta_list: List[Dict]) -> None:
        _start = None
        _end = None
        for meta_statistics in workers_meta_list:
            try:
                statistics = meta_statistics.get("statistics", {})
                if not statistics.__contains__(self.KEY_NAME):
                    break
                _start = statistics.get(self.KEY_NAME).get("start")
                _end = statistics.get(self.KEY_NAME).get("end")
            except Exception as e:
                raise e

            if self.start is None and self.end is None:
                self.start = _start
                self.end = _end
            elif self.start is not None and self.start > _start:
                self.start = _start
            elif self.end is not None and self.end < _end:
                self.end = _end

    def local_calc(self, val: Union[str, np.array], meta_statistics: Dict) -> None:
        rst = None

        for idx, date_format in enumerate(self.date_format_list):
            try:
                rst = datetime.strptime(val, date_format)
                self.date_format_idx = idx
                break
            except ValueError:
                continue

        if self.date_format_idx is not None:
            if self.start is None and self.end is None:
                self.start = rst
                self.end = rst
            elif self.start is not None and self.start > rst:
                self.start = rst
            elif self.end is not None and self.end < rst:
                self.end = rst

    def local_to_dict(self) -> Dict:
        _start = None if not self.start else self.start.strftime(self.date_format_list[self.date_format_idx])
        _end = None if not self.end else self.end.strftime(self.date_format_list[self.date_format_idx])

        return {
            self.KEY_NAME: {
                "start": _start,
                "end": _end
            }
        }

    def global_to_dict(self) -> Dict:
        if self.start is None or self.end is None:
            return {}
        else:
            return {
                self.KEY_NAME: {
                    "start": self.start,
                    "end": self.end
                }
            }
