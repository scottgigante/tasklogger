==========
tasklogger
==========

.. image:: https://img.shields.io/pypi/v/tasklogger.svg
    :target: https://pypi.org/project/tasklogger/
    :alt: Latest PyPi version
.. image:: https://api.travis-ci.com/scottgigante/tasklogger.svg?branch=master
    :target: https://travis-ci.com/scottgigante/tasklogger
    :alt: Travis CI Build
.. image:: https://coveralls.io/repos/github/scottgigante/tasklogger/badge.svg?branch=master
    :target: https://coveralls.io/github/scottgigante/tasklogger?branch=master
    :alt: Coverage Status
.. image:: https://img.shields.io/twitter/follow/scottgigante.svg?style=social&label=Follow
    :target: https://twitter.com/scottgigante
    :alt: Twitter
.. image:: https://img.shields.io/github/stars/scottgigante/tasklogger.svg?style=social&label=Stars
    :target: https://github.com/scottgigante/tasklogger/
    :alt: GitHub stars

An extension to the core python logging library for logging the beginning and completion of tasks and subtasks.

Installation
------------

tasklogger is available on `pip`. Install by running the following in a terminal::

    pip install --user tasklogger

Usage example
-------------

Use `tasklogger` for all your logging needs - receive timed updates mid-computation using `tasklogger.log_start` and `tasklogger.log_complete`::

    >>> import tasklogger
    >>> import time
    >>> tasklogger.log_start("Supertask")
    Calculating Supertask...
    >>> time.sleep(1)
    >>> tasklogger.log_start("Subtask")
    Calculating Subtask...
    >>> time.sleep(1)
    >>> tasklogger.log_complete("Subtask")
    Calculated Subtask in 1.01 seconds.
    >>> time.sleep(1)
    >>> tasklogger.log_complete("Supertask")
    Calculated Supertask in 3.02 seconds.
    >>> tasklogger.log_info("Log some stuff that doesn't need timing")
    Log some stuff that doesn't need timing
    >>> tasklogger.log_debug("Log some stuff that normally isn't needed")
    >>> tasklogger.set_level(2)
    Set TaskLogger logging to DEBUG
    >>> tasklogger.log_debug("Log some stuff that normally isn't needed")
    Log some stuff that normally isn't needed
