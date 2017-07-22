import pytest
from speedtest_sendtest.speedtest_exceptions import SpeedtestNoSpeedsError, SpeedtestAttemptsExceededError
from speedtest_sendtest import sendtest

#def test_make_yesterday(monkeypatch):

#   speedtest_sendtest.speedtest_sendtest.datetime.today()


def test_throw_FileNotFoundError(tmpdir, monkeypatch):
    test_requester = sendtest.TextBeltRequest()
    monkeypatch.setenv('HOME', tmpdir.mkdir('home'))
    with pytest.raises(FileNotFoundError):
        test_requester.make_average()

def test_throw_SpeedtestNoSpeedsError(tmpdir, monkeypatch):
    test_requester = sendtest.TextBeltRequest()
    monkeypatch.setenv('HOME', tmpdir.mkdir('home'))
    open(tmpdir.join("sendtest_log", "r+")
    with pytest.raises(SpeedtestNoSpeedsError):
        test_requester.make_average()

#def test_make_average_file():


def test_regex():
    test_regex = "Download: 23.99 Mbit/s"
