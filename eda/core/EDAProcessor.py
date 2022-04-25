from eda.common.Common import Common


class EDAProcessorChief(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, key, task_idx):
        self.key = key
        self.task_idx = task_idx

    def run(self):
        pass


class EDAProcessorWorker(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, key, task_idx):
        self.key = key
        self.task_idx = task_idx

    def run(self):
        pass
