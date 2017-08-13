"""
Tests for speedtest_sendtest
"""
import pytest

from speedtest_sendtest.speedtest_exceptions import SpeedtestNoSpeedsError
from speedtest_sendtest import sendtest


def test_throw_FileNotFoundError(tmpdir, monkeypatch):
    """
    Tests if make_average throws a FileNotFoundError
    """
    test_requester = sendtest.TextBeltRequest()
    monkeypatch.setenv('HOME', tmpdir.mkdir('home'))
    with pytest.raises(FileNotFoundError):
        test_requester.make_average()


def test_throw_SpeedtestNoSpeedsError(create_TextBeltRequest_object, tmpdir,
                                      monkeypatch):
    """
    test's if make_average throws a SpeedtestNoSpeedsError
    """
    home = tmpdir.mkdir('home')
    monkeypatch.setenv('HOME', home)
    test_request.speedtest_log = home.join("speedtest_log")
    with open(test_requester.speedtest_log, "x"):
        with pytest.raises(SpeedtestNoSpeedsError):
            test_requester.make_average()


#def test_make_average_file():


def test_make_average_regex(create_TextBeltRequest_object):
    test_phrase = r"Download: 23.99 Mbit/s"
    search = test_request.download_regex.search(test_phrase)
    assert search.group(1) == 23.99


def test_speedtest_log_regex(create_TextBeltRequest_object, tmpdir):
    test_speedtest_log = tmpdir.join("speedtest.log")
    test_speedtest_log.write("Download: 23.99 Mbit/s")
    test_request.speedtest_log = test_speedtest_log
    test_average_speed = test_request.make_average()
    assert test_average_speed == 23.99
