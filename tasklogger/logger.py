from __future__ import absolute_import, print_function
from builtins import super
import logging
import time
from . import stream


class TaskLogger(object):
    """
    Class which deals with timing and logging tasks
    """

    def __init__(self, name="TaskLogger", level=1,
                 min_runtime=0.01, *args, **kwargs):
        self.tasks = {}
        self.name = name
        self.min_runtime = min_runtime
        if hasattr(self.logger, "tasklogger"):
            raise RuntimeError("TaskLogger {0} already exists. Please set "
                               "`name` to be unique or use "
                               "`tasklogger.get_tasklogger(logger={0})".format(
                                   name))
        self.set_level(level)
        super().__init__(*args, **kwargs)

    @property
    def logger(self):
        try:
            return self._logger
        except AttributeError:
            self._logger = self.get_logger()
            self.level = self._logger.level
            return self._logger

    def get_logger(self):
        return logging.getLogger(self.name)

    def set_level(self, level=1):
        """Set up logging

        Parameters
        ----------

        level : `int` or `bool` (optional, default: 1)
            If False or 0, prints WARNING and higher messages.
            If True or 1, prints INFO and higher messages.
            If 2 or higher, prints all messages.
        """
        if level is True or level == 1:
            level = logging.INFO
            level_name = "INFO"
        elif level is False or level <= 0:
            level = logging.WARNING
            level_name = "WARNING"
        elif level >= 2:
            level = logging.DEBUG
            level_name = "DEBUG"

        if not self.logger.handlers:
            self.logger.tasklogger = self
            self.logger.propagate = False
            handler = logging.StreamHandler(stream=stream.RSafeStdErr())
            handler.setFormatter(logging.Formatter(fmt='%(message)s'))
            self.logger.addHandler(handler)

        if level != self.logger.level:
            self.level = level
            self.logger.setLevel(level)
            self.debug("Set {} logging to {}".format(
                self.name, level_name))

    def debug(self, msg):
        """
        Convenience function to log a message to the default Logger
        """
        self.logger.debug(msg)

    def info(self, msg):
        """
        Convenience function to log a message to the default Logger
        """
        self.logger.info(msg)

    def warning(self, msg):
        """
        Convenience function to log a message to the default Logger
        """
        self.logger.warning(msg)

    def error(self, msg):
        """
        Convenience function to log a message to the default Logger
        """
        self.logger.error(msg)

    def critical(self, msg):
        """
        Convenience function to log a message to the default Logger
        """
        self.logger.critical(msg)

    def start_task(self, task):
        self.tasks[task] = time.time()
        self.info("Calculating {}...".format(task))

    def complete_task(self, task):
        try:
            runtime = time.time() - self.tasks[task]
            if runtime >= self.min_runtime:
                self.info("Calculated {} in {:.2f} seconds.".format(
                    task, runtime))
            del self.tasks[task]
        except KeyError:
            self.info("Calculated {}.".format(task))
