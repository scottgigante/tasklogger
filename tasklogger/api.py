from __future__ import absolute_import, print_function
import logging
from . import logger


def get_tasklogger(name="TaskLogger"):
    try:
        return logging.getLogger(name).tasklogger
    except AttributeError:
        return logger.TaskLogger(name)


def log_start(task, logger="TaskLogger"):
    """
    Convenience function to log a task in the default
    TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.start_task(task)
    return tasklogger


def log_complete(task, logger="TaskLogger"):
    """
    Convenience function to log a task in the default
    TaskLogger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.complete_task(task)
    return tasklogger


def log_debug(msg, logger="TaskLogger"):
    """
    Convenience function to log a message to the default Logger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.debug(msg)
    return tasklogger


def log_info(msg, logger="TaskLogger"):
    """
    Convenience function to log a message to the default Logger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.info(msg)
    return tasklogger


def log_warning(msg, logger="TaskLogger"):
    """
    Convenience function to log a message to the default Logger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.warning(msg)
    return tasklogger


def log_error(msg, logger="TaskLogger"):
    """
    Convenience function to log a message to the default Logger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.error(msg)
    return tasklogger


def log_critical(msg, logger="TaskLogger"):
    """
    Convenience function to log a message to the default Logger
    """
    tasklogger = get_tasklogger(logger)
    tasklogger.critical(msg)
    return tasklogger


def set_level(level, logger="TaskLogger"):
    tasklogger = get_tasklogger(logger)
    tasklogger.set_level(level)
    return tasklogger
