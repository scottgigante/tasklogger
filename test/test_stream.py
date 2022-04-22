import numpy as np
import os
import sys
import tasklogger

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
