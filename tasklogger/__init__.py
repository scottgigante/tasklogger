from .logger import TaskLogger
from .api import *
from .version import __version__

import time
try:
    time.process_time
except AttributeError:
    # Python 2.7 monkey patch
    time.process_time = time.clock
