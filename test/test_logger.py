import tasklogger
import time
import numpy as np
import logging


def test_tasks():
    logger = tasklogger.TaskLogger("test_tasks")
    logger.start_task("test")
    assert time.time() - logger.tasks['test'] < 0.01
    time.sleep(logger.min_runtime)
    logger.complete_task("test")
    assert 'test' not in logger.tasks


def test_log():
    logger = tasklogger.TaskLogger("test_log")
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')


def test_level():
    logger = tasklogger.TaskLogger("test_level")
    logger.set_level(2)
    assert logger.level == logging.DEBUG
    assert logger.logger.level == logging.DEBUG


def test_duplicate():
    logger = tasklogger.TaskLogger("test_duplicate")
    np.testing.assert_raises(RuntimeError, tasklogger.TaskLogger,
                             "test_duplicate")
    logger2 = tasklogger.TaskLogger("test_no_duplicate")
    assert logger.logger is not logger2.logger
