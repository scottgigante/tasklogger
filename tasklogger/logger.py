from . import stream
from deprecated.sphinx import deprecated

import contextlib
import logging
import time


def _get_logger(name):
    return logging.getLogger(name)


def _tasklogger_exists(logger):
    """Check if a `logging.Logger` already has an associated TaskLogger"""
    return hasattr(logger, "tasklogger")


def _increment_name(name, increment=1):
    new_name = "{}_{}".format(name, increment)
    if not _tasklogger_exists(_get_logger(new_name)):
        return new_name
    else:
        return _increment_name(name, increment=increment + 1)


class TaskLogger(object):
    """Class which deals with timing and logging tasks

    Parameters
    ----------
    name : `str`, optional (default: "TaskLogger")
        Name used to retrieve the unique TaskLogger
    level : `int` or `bool`, optional (default: 1)
        Integer logging level.
        If < -2, prints no messages.
        If False or >= -2, prints CRITICAL messages.
        If False or >= -1, prints ERROR messages.
        If False or >= 0, prints WARNING messages.
        If True or >= 1, prints INFO messages.
        If >= 2, prints all messages.
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
    if_exists : {"error", "ignore", "increment"}, optional (default: "error")
        Behavior if a TaskLogger named `name` already exists. If "error", raises a
        RuntimeError (as in `logging`). If "ignore", returns a new TaskLogger
        attached to the `logging.Logger` attached to the existing
        TaskLogger of the same name. If "increment", creates a new TaskLogger with
        `name` incremented by an integer.

    Properties
    ----------
    logger : `logging.Logger`
        Python logging class used to print log messages
    """

    def __init__(
        self,
        name="TaskLogger",
        level=1,
        timer="wall",
        stream="stdout",
        min_runtime=0.01,
        indent=2,
        if_exists="error",
        **kwargs,
    ):
        self.tasks = {}
        self.name = name
        self.min_runtime = min_runtime
        self.stream = stream
        self.indent = indent
        if _tasklogger_exists(self.logger):
            if if_exists == "error":
                raise RuntimeError(
                    "TaskLogger {0} already exists. Please set "
                    "`name` to be unique or set `if_exists` to "
                    '"ignore" or "increment"'.format(name)
                )
            elif if_exists == "increment":
                del self._logger
                self.name = _increment_name(self.name)
                assert not _tasklogger_exists(self.logger)
            elif if_exists == "ignore":
                pass
            else:
                raise ValueError(
                    'Expected `if_exists` in "error", "ignore", "increment".'
                    " Got {}".format(if_exists)
                )
        self.set_level(level)
        self.set_timer(timer)

    @property
    def logger(self):
        try:
            return self._logger
        except AttributeError:
            self._logger = _get_logger(self.name)
            self.level = self._logger.level
            return self._logger

    def set_level(self, level=1):
        """Set the logging level

        Parameters
        ----------
        level : `int` or `bool` (optional, default: 1)
            If < -2, prints no messages.
            If False or >= -2, prints CRITICAL messages.
            If False or >= -1, prints ERROR messages.
            If False or >= 0, prints WARNING messages.
            If True or >= 1, prints INFO messages.
            If >= 2, prints all messages.

        Returns
        -------
        self
        """

        if isinstance(level,bool):
            if level:
                level = logging.INFO
                level_name = "INFO"
            else:
                level = logging.WARNING
                level_name = "WARNING"
        else:
            if level >= 2:
                level = logging.DEBUG
                level_name = "DEBUG"
            elif level >= 1:
                level = True
                return self.set_level(level)
            elif level >= 0:
                level = False
                return self.set_level(level)
            elif level >= -1:
                level = logging.ERROR
                level_name = "ERROR"
            elif level >= -2:
                level = logging.CRITICAL
                level_name = "CRITICAL"
            else:
                level = logging.IGNORE
                level_name = "IGNORE"

        if not self.logger.handlers:
            self.logger.tasklogger = self
            self.logger.propagate = False
            handler = logging.StreamHandler(
                stream=stream.RSafeStream(stream=self.stream)
            )
            handler.setFormatter(logging.Formatter(fmt="%(message)s"))
            self.logger.addHandler(handler)

        if level != self.logger.level:
            self.level = level
            self.logger.setLevel(level)
            self.log_debug("Set {} logging to {}".format(self.name, level_name))

        return self

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
            timer = time.process_time
        elif not callable(timer):
            raise ValueError(
                "Expected timer to be 'wall', 'cpu', or a callable. "
                "Got {}".format(timer)
            )
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
        """Log a message"""
        if self.indent > 0:
            msg = len(self.tasks) * self.indent * " " + msg
        return log_fn(msg)

    @deprecated(version="1.1.0", reason="Use TaskLogger.log_debug instead")
    def debug(self, msg):
        return self.log_debug(msg)

    def log_debug(self, msg):
        """Log a DEBUG message

        Convenience function to log a message to the default Logger

        Parameters
        ----------
        msg : str
            Message to be logged
        """
        self._log(self.logger.debug, msg)

    @deprecated(version="1.1.0", reason="Use TaskLogger.log_info instead")
    def info(self, msg):
        return self.log_info(msg)

    def log_info(self, msg):
        """Log an INFO message

        Convenience function to log a message to the default Logger

        Parameters
        ----------
        msg : str
            Message to be logged
        """
        self._log(self.logger.info, msg)

    @deprecated(version="1.1.0", reason="Use TaskLogger.log_warning instead")
    def warning(self, msg):
        return self.log_warning(msg)

    def log_warning(self, msg):
        """Log a WARNING message

        Convenience function to log a message to the default Logger

        Parameters
        ----------
        msg : str
            Message to be logged
        """
        self._log(self.logger.warning, msg)

    @deprecated(version="1.1.0", reason="Use TaskLogger.log_error instead")
    def error(self, msg):
        return self.log_error(msg)

    def log_error(self, msg):
        """Log an ERROR message

        Convenience function to log a message to the default Logger

        Parameters
        ----------
        msg : str
            Message to be logged
        """
        self._log(self.logger.error, msg)

    @deprecated(version="1.1.0", reason="Use TaskLogger.log_critical instead")
    def critical(self, msg):
        return self.log_critical(msg)

    def log_critical(self, msg):
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
        self.log_info("Calculating {}...".format(task))
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
                self.log_info("Calculated {} in {:.2f} seconds.".format(task, runtime))
            return runtime
        except KeyError:
            self.log_info("Calculated {}.".format(task))

    @deprecated(version="1.1.0", reason="Use TaskLogger.log_task instead")
    def task(self, task):
        return self.log_task(task)

    @contextlib.contextmanager
    def log_task(self, task):
        """Context manager for logging a task

        Times the action within the context frame

        Parameters
        ----------
        task : str
            Name of the task to be started

        Examples
        --------
        >>> import tasklogger
        >>> import time
        >>> logger = tasklogger.TaskLogger()
        >>> with logger.log_task('test'):
        ...     time.sleep(1)
        Calculating test...
        Calculated test in 1.00 seconds.
        """
        try:
            yield self.start_task(task)
        finally:
            self.complete_task(task)
