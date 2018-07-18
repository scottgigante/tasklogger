from __future__ import absolute_import, print_function
import sys
import os
from . import utils


class RSafeStdErr(object):
    """
    R's reticulate package inadvertently captures stderr and stdout
    This class writes directly to stderr to avoid this.
    """

    def __init__(self):
        if utils.in_ipynb():
            self.write = self.write_ipython
        else:
            self.write = self.write_r_safe

    def write_ipython(self, msg):
        print(msg, end='', file=sys.stdout)

    def write_r_safe(self, msg):
        try:
            os.write(1, bytes(msg, 'utf8'))
        except OSError as e:
            if str(e) == "[Errno 9] Bad file descriptor":
                # weird windows 7 error
                print(msg, end='')
            else:
                raise

    def flush(self):
        sys.stdout.flush()
