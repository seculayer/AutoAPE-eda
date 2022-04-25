# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021-2022 AI Service Model Team, R&D Center.

from eda.common.Common import Common
from eda.common.Constants import Constants
from eda.core.EDAProcessor import EDAProcessorChief, EDAProcessorWorker


class EDARunner(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, key, job_type, task_idx):
        self.key: str = key
        self.task_idx: str = task_idx

        self.LOGGER.info(Constants.VERSION_MANAGER.print_version())
        if job_type == "Chief":
            self.processor = EDAProcessorChief(key, task_idx)
        else:  # job_type == "Worker"
            self.processor = EDAProcessorWorker(key, task_idx)

    def run(self) -> None:
        self.processor.run()


if __name__ == '__main__':
    import sys
    _key = sys.argv[1]
    _task_idx = sys.argv[2]
    _job_type = sys.argv[3]

    eda = EDARunner(_key, _job_type, _task_idx)

    eda.run()
