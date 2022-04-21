
from .api import *  # noqa
from .logger import TaskLogger
from .version import __version__

# patching in a new logging level beneath all others for total suppression
# see https://stackoverflow.com/a/55276759/1810940
# the logging level is called logging.IGNORE. messages passed to it will appear
# in all default log levels. 
# However, if the logging level is set to logging.IGNORE, all other messages
# are ignored.

import logging
from functools import partial, partialmethod
logging.IGNORE = 60
logging.addLevelName(logging.IGNORE, 'IGNORE')
logging.Logger.ignore = partialmethod(logging.Logger.log, logging.IGNORE)
logging.ignore = partial(logging.log, logging.IGNORE)


