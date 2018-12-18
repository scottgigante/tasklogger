from .logger import TaskLogger
from .api import *
from .version import __version__

import platform
import time
try:
    time.process_time
except AttributeError:
    # Python 2.7 monkey patch
    if platform.system() != "Windows":
        # windows time.clock is wall time
        time.process_time = time.clock
