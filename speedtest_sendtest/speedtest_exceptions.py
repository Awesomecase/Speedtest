#!/usr/bin/env python3
"""
Exceptions for speedtest_send_test
SpeedtestSenderException: base class
SpeedtestNoSpeedsException: can't find any speeds in speedtest.log
"""
class SpeedtestSenderError(Exception):
    """Base class for all exceptions in speedtest_exceptions"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class SpeedtestNoSpeedsError(SpeedtestSenderError):
    """
    Inherits from SpeedtestSenderException, No speeds in file.
    """
    def __init__(self, *args, **kwargs):
        SpeedtestSenderError.__init__(self, *args, **kwargs)

class SpeedtestAttemptsExceededError(SpeedtestSenderError):
    """
    Inherits from SpeedtestSenderException. Attempts for sending excceded
    """
    def __init__(self, *args, **kwargs):
        SpeedtestSenderError.__init__(self, *args, **kwargs)
