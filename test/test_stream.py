import numpy as np
import os
import sys
import tasklogger
import tasklogger.stream
import tasklogger.utils


def test_ipynb():
    def monkey_patch():
        return True

    temp = tasklogger.utils.in_ipynb
    tasklogger.utils.in_ipynb = monkey_patch
    logger = tasklogger.TaskLogger("ipynb")
    logger.log_info("ipynb")
    tasklogger.utils.in_ipynb = temp


def test_oserror():
    def monkey_patch(*args, **kwargs):
        raise OSError("[Errno 9] Bad file descriptor")

    temp = os.write
    os.write = monkey_patch
    logger = tasklogger.TaskLogger("oserror")
    logger.log_info("oserror")
    os.write = temp


def test_no_stdout():
    temp = sys.stdout
    sys.stdout = None
    logger = tasklogger.TaskLogger("no stdout")
    logger.log_info("no stdout")
    logger.logger.handlers[0].stream.flush()
    sys.stdout = temp


def test_stderr():
    temp = sys.stdout
    sys.stdout = None
    logger = tasklogger.TaskLogger("stderr", stream="stderr")
    logger.log_info("stderr")
    sys.stdout = temp


def test_invalid_stream():
    np.testing.assert_raises(
        ValueError, tasklogger.TaskLogger, "invalid stream", stream="invalid"
    )
