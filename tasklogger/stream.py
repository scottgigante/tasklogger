from __future__ import absolute_import, print_function
from builtins import bytes
import sys
import os
from . import utils


class RSafeStream(object):
    """File stream that plays nice with reticulate and IPython

    R's reticulate package inadvertently captures stderr and stdout
    This class writes directly to stderr/out to avoid this. However,
    writing directly to stdout and stderr causes problems for Jupyter
    notebooks.

    TODO: Accept a filename or file handle as a stream

    Parameters
    ----------
    stream: ['stderr', 'stdout'], optional (default: "stdout")
        File stream to which logs are printed
    """

    def __init__(self, stream="stdout"):
        if stream not in ['stderr', 'stdout']:
            raise ValueError("Expected stream in ['stderr', 'stdout']. "
                             "Got {}".format(stream))
        self.stream = stream
        self.stream_handle = sys.stdout if stream == "stdout" else sys.stderr
        if utils.in_ipynb():
            self.write = self.write_ipython
        else:
            self.write = self.write_r_safe

    def write_ipython(self, msg):
        print(msg, end='', file=self.stream_handle)

    def write_r_safe(self, msg):
        try:
            os.write(1 if self.stream == "stdout" else 2, bytes(msg, 'utf8'))
        except OSError as e:
            if str(e) == "[Errno 9] Bad file descriptor":
                # weird windows 7 error
                print(msg, end='')
            else:
                raise e

    def flush(self):
        try:
            self.stream_handle.flush()
        except AttributeError:
            if sys is None or self.stream_handle is None:
                pass
            else:
                raise
