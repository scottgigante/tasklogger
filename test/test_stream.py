import tasklogger.stream
import tasklogger.utils
import tasklogger
import os


def test_ipynb():
    def monkey_patch():
        return True
    temp = tasklogger.utils.in_ipynb
    tasklogger.utils.in_ipynb = monkey_patch
    logger = tasklogger.TaskLogger("ipynb")
    logger.info("ipynb")
    tasklogger.utils.in_ipynb = temp


def test_oserror():
    def monkey_patch(*args, **kwargs):
        raise OSError("[Errno 9] Bad file descriptor")
    temp = os.write
    os.write = monkey_patch
    logger = tasklogger.TaskLogger("oserror")
    logger.info("oserror")
    os.write = temp
