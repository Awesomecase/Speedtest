#!/usr/bin/env python3
"""
Exceptions for speedtest_send_test
SpeedtestSenderException: base class
SpeedtestNoSpeedsException: can't find any speeds in speedtest.log
SpeedtestAttemptsExceededError: retry attempts exceeded
"""


class SpeedtestSenderError(Exception):
    """Base class for all exceptions in speedtest_exceptions"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class SpeedtestNoSpeedsError(SpeedtestSenderError):
    """
    No speeds in speedtest.log.
    """

    def __init__(self, *args, **kwargs):
        SpeedtestSenderError.__init__(self, *args, **kwargs)


class SpeedtestAttemptsExceededError(SpeedtestSenderError):
    """
    Attempts for sending exceeded
    """

    def __init__(self, *args, **kwargs):
        SpeedtestSenderError.__init__(self, *args, **kwargs)
