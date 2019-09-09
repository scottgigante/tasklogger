from . import api


class Task(object):

    def __init__(self, name, logger="TaskLogger"):
        self.name = name
        self._logger_name = logger

    @property
    def logger(self):
        try:
            return self._logger
        except AttributeError:
            if isinstance(self._logger_name, str):
                self._logger = api.get_tasklogger(self._logger_name)
            else:
                self._logger = self._logger_name
            return self._logger

    def __enter__(self):
        self.logger.start_task(self.name)

    def __exit__(self, type, value, traceback):
        self.logger.complete_task(self.name)
