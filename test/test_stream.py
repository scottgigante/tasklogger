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


def test_invalid_stream_str():
    np.testing.assert_raises(
        ValueError, tasklogger.TaskLogger, 'Input stream is neither "stdout", "stderr", or a file-like', stream="invalid"
    )

def test_invalid_stream_str():
    class InvalidStream:
        pass
    np.testing.assert_raises(
        ValueError, tasklogger.TaskLogger, 'does not possess write() and flush() methods required of stream objects', stream=InvalidStream()
    )

def test_invalid_stream_noflush():
    class InvalidStream:
        def write(self):
            pass
    np.testing.assert_raises(
        ValueError, tasklogger.TaskLogger, 'does not possess flush() method required of stream objects', stream=InvalidStream()
    )

def test_invalid_stream_nowrite():
    class InvalidStream:
        def flush(self):
            pass
    np.testing.assert_raises(
        ValueError, tasklogger.TaskLogger, 'does not possess write() method required of stream objects', stream=InvalidStream()
    )
