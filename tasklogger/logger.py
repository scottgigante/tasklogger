from __future__ import absolute_import, print_function
from builtins import super
import logging
import time
from . import stream


class TaskLogger(object):
    """Class which deals with timing and logging tasks

    Parameters
    ----------
    name : `str`, optional (default: "TaskLogger")
        Name used to retrieve the unique TaskLogger
    level : `int` or `bool`, optional (default: 1)
        Integer logging level.
        Interchangeable with `logging.WARNING` (0, False),
        `logging.INFO` (1, True) and `logging.DEBUG` (2).
    timer : {'wall', 'cpu', or callable}, optional (default 'wall')
        Timer function used to measure task running times.
        'wall' uses `time.time`, 'cpu' uses `time.process_time`
    stream: ['stderr', 'stdout'], optional (default: "stdout")
        File stream to which logs are printed
    min_runtime : float, optional (default: 0.01)
        Time below which a completion message is not printed
    indent : int, optional (default: 2)
        number of spaces by which to indent based on the
        number of tasks currently running

    Properties
    ----------
    logger : `logging.Logger`
        Python logging class used to print log messages
    """

    def __init__(self, name="TaskLogger", level=1,
                 timer="wall", stream="stdout",
                 min_runtime=0.01, indent=2, **kwargs):
        self.tasks = {}
        self.name = name
        self.min_runtime = min_runtime
        self.stream = stream
        self.indent = indent
        if hasattr(self.logger, "tasklogger"):
            raise RuntimeError("TaskLogger {0} already exists. Please set "
                               "`name` to be unique or use "
                               "`tasklogger.get_tasklogger(logger={0})".format(
                                   name))
        self.set_level(level)
        self.set_timer(timer)

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
        """Set the logging level

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
            handler = logging.StreamHandler(
                stream=stream.RSafeStream(stream=self.stream))
            handler.setFormatter(logging.Formatter(fmt='%(message)s'))
            self.logger.addHandler(handler)

        if level != self.logger.level:
            self.level = level
            self.logger.setLevel(level)
            self.debug("Set {} logging to {}".format(
                self.name, level_name))

    def set_timer(self, timer="wall"):
        """Set the timer function

        Parameters
        ----------
        timer : {'wall', 'cpu', or callable}
                Timer function used to measure task running times.
                'wall' uses `time.time`, 'cpu' uses `time.process_time`

        Returns
        -------
        self
        """
        if timer == "wall":
            timer = time.time
        elif timer == "cpu":
            try:
                timer = time.process_time
            except AttributeError:
                raise RuntimeError(
                    "Python2.7 on Windows does not offer a CPU time function. "
                    "Please upgrade to Python >= 3.5.")
        self.timer = timer
        return self

    def set_indent(self, indent=2):
        """Set the indent size

        Parameters
        ----------
        indent : int, optional (default: 2)
            number of spaces by which to indent based on the
            number of tasks currently running

        Returns
        -------
        self
        """
        self.indent = indent
        return self

    def _log(self, log_fn, msg):
        """Log a message
        """
        if self.indent > 0:
            msg = len(self.tasks) * self.indent * ' ' + msg
        return log_fn(msg)

    def debug(self, msg):
        """Log a DEBUG message

        Convenience function to log a message to the default Logger

        Parameters
        ----------
        msg : str
            Message to be logged
        """
        self._log(self.logger.debug, msg)

    def info(self, msg):
        """Log an INFO message

        Convenience function to log a message to the default Logger

        Parameters
        ----------
        msg : str
            Message to be logged
        """
        self._log(self.logger.info, msg)

    def warning(self, msg):
        """Log a WARNING message

        Convenience function to log a message to the default Logger

        Parameters
        ----------
        msg : str
            Message to be logged
        """
        self._log(self.logger.warning, msg)

    def error(self, msg):
        """Log an ERROR message

        Convenience function to log a message to the default Logger

        Parameters
        ----------
        msg : str
            Message to be logged
        """
        self._log(self.logger.error, msg)

    def critical(self, msg):
        """Log a CRITICAL message

        Convenience function to log a message to the default Logger

        Parameters
        ----------
        msg : str
            Message to be logged
        """
        self._log(self.logger.critical, msg)

    def start_task(self, task):
        """Begin logging of a task

        Stores the time this task was started in order to return
        time lapsed when `complete_task` is called.

        Parameters
        ----------
        task : str
            Name of the task to be started
        """
        self.info("Calculating {}...".format(task))
        self.tasks[task] = self.timer()

    def complete_task(self, task):
        """Complete logging of a task

        Returns the time lapsed since `start_task` was called

        Parameters
        ----------
        task : str
            Name of the task to be started

        Returns
        -------
        time : float
            The time lapsed between task start and completion
        """
        try:
            runtime = self.timer() - self.tasks[task]
            del self.tasks[task]
            if runtime >= self.min_runtime:
                self.info("Calculated {} in {:.2f} seconds.".format(
                    task, runtime))
            return runtime
        except KeyError:
            self.info("Calculated {}.".format(task))
