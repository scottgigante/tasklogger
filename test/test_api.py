import tasklogger
import time
import logging


def test_get_logger():
    logger = tasklogger.get_tasklogger()
    logger2 = tasklogger.get_tasklogger()
    assert logger is logger2
    logger2 = tasklogger.get_tasklogger("test")
    assert logger is not logger2


def test_tasks():
    logger = tasklogger.log_start("test")
    assert time.time() - logger.tasks['test'] < 0.01
    time.sleep(logger.min_runtime)
    tasklogger.log_complete("test")
    assert 'test' not in logger.tasks


def test_log():
    tasklogger.log_debug('debug')
    tasklogger.log_info('info')
    tasklogger.log_warning('warning')
    tasklogger.log_error('error')
    tasklogger.log_critical('critical')


def test_level():
    logger = tasklogger.set_level(2)
    assert logger.level == logging.DEBUG
    assert logger.logger.level == logging.DEBUG
