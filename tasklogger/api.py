from . import logger

import logging


def get_tasklogger(name="TaskLogger"):
    """Get a TaskLogger object

    Parameters
    ----------
    logger : str, optional (default: "TaskLogger")
        Unique name of the logger to retrieve

    Returns
    -------
    logger : TaskLogger
    """
    try:
        return logging.getLogger(name).tasklogger
    except AttributeError:
        return logger.TaskLogger(name)


def log_start(task, logger="TaskLogger"):
    """Begin logging of a task

    Convenience function to log a task in the default
    TaskLogger

    Parameters
    ----------
    task : str
        Name of the task to be started
    logger : str, optional (default: "TaskLogger")
        Unique name of the logger to retrieve

    Returns
    -------
    logger : TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.start_task(task)
    return tasklogger


def log_complete(task, logger="TaskLogger"):
    """Complete logging of a task

    Convenience function to log a task in the default
    TaskLogger

    Parameters
    ----------
    task : str
        Name of the task to be started
    logger : str, optional (default: "TaskLogger")
        Unique name of the logger to retrieve

    Returns
    -------
    time : float
        The time lapsed between task start and completion
    """
    tasklogger = get_tasklogger(logger)
    return tasklogger.complete_task(task)


def log_task(task, logger="TaskLogger"):
    """Context manager for logging a task

    Times the action within the context frame

    Parameters
    ----------
    task : str
        Name of the task to be started
    logger : str, optional (default: "TaskLogger")
        Unique name of the logger to retrieve

    Examples
    --------
    >>> import tasklogger
    >>> import time
    >>> with tasklogger.log_task('test'):
    ...     time.sleep(1)
    Calculating test...
    Calculated test in 1.00 seconds.
    """
    tasklogger = get_tasklogger(logger)
    return tasklogger.log_task(task)


def log_debug(msg, logger="TaskLogger"):
    """Log a DEBUG message

    Convenience function to log a message to the default Logger

    Parameters
    ----------
    msg : str
        Message to be logged
    logger : str, optional (default: "TaskLogger")
        Unique name of the logger to retrieve

    Returns
    -------
    logger : TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.log_debug(msg)
    return tasklogger


def log_info(msg, logger="TaskLogger"):
    """Log an INFO message

    Convenience function to log a message to the default Logger

    Parameters
    ----------
    msg : str
        Message to be logged
    logger : str, optional (default: "TaskLogger")
        Unique name of the logger to retrieve

    Returns
    -------
    logger : TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.log_info(msg)
    return tasklogger


def log_warning(msg, logger="TaskLogger"):
    """Log a WARNING message

    Convenience function to log a message to the default Logger

    Parameters
    ----------
    msg : str
        Message to be logged
    logger : str, optional (default: "TaskLogger")
        Unique name of the logger to retrieve

    Returns
    -------
    logger : TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.log_warning(msg)
    return tasklogger


def log_error(msg, logger="TaskLogger"):
    """Log an ERROR message

    Convenience function to log a message to the default Logger

    Parameters
    ----------
    msg : str
        Message to be logged
    logger : str, optional (default: "TaskLogger")
        Unique name of the logger to retrieve

    Returns
    -------
    logger : TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.log_error(msg)
    return tasklogger


def log_critical(msg, logger="TaskLogger"):
    """Log a CRITICAL message

    Convenience function to log a message to the default Logger

    Parameters
    ----------
    msg : str
        Message to be logged
    name : `str`, optional (default: "TaskLogger")
        Name used to retrieve the unique TaskLogger

    Returns
    -------
    logger : TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.log_critical(msg)
    return tasklogger


def set_level(level=1, logger="TaskLogger"):
    """Set the logging level

    Convenience function to set the logging level

    Parameters
    ----------
    level : `int` or `bool` (optional, default: 1)
        If False or 0, prints WARNING and higher messages.
        If True or 1, prints INFO and higher messages.
        If 2 or higher, prints all messages.

    Returns
    -------
    logger : TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.set_level(level)
    return tasklogger


def set_timer(timer="wall", logger="TaskLogger"):
    """Set the timer function

    Convenience function to set the task timer

    Parameters
    ----------
    timer : {'wall', 'cpu', or callable}, optional, default='wall'
            Timer function used to measure task running times.
            'wall' uses `time.time`, 'cpu' uses `time.process_time`

    Returns
    -------
    logger : TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.set_timer(timer)
    return tasklogger


def set_indent(indent=2, logger="TaskLogger"):
    """Set the indent function

    Convenience function to set the indent size

    Parameters
    ----------
    indent : int, optional (default: 2)
        number of spaces by which to indent based on the
        number of tasks currently running`

    Returns
    -------
    logger : TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.set_indent(indent)
    return tasklogger
