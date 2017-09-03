"""
Tests for speedtest_sendtest
"""
import pytest
import requests_mock

from speedtest_sendtest.speedtest_exceptions import SpeedtestNoSpeedsError
from speedtest_sendtest import sendtest


def test_throw_FileNotFoundError(tmpdir, monkeypatch, TextBeltRequest_object):
    """
    Tests if make_average throws a FileNotFoundError
    """
    monkeypatch.setenv('HOME', tmpdir.mkdir('home'))
    TextBeltRequest_object.speedtest_log = sendtest.os.path.expanduser(
        "~/speedtest.log")
    with pytest.raises(FileNotFoundError):
        TextBeltRequest_object.make_average()


def test_throw_SpeedtestNoSpeedsError(TextBeltRequest_object, tmpdir,
                                      monkeypatch):
    """
    test's if make_average throws a SpeedtestNoSpeedsError
    """
    home = tmpdir.mkdir('home')
    monkeypatch.setenv('HOME', home)
    TextBeltRequest_object.speedtest_log = home.join("speedtest_log")
    with open(TextBeltRequest_object.speedtest_log, "x"):
        with pytest.raises(SpeedtestNoSpeedsError):
            TextBeltRequest_object.make_average()


def test_make_average_regex(TextBeltRequest_object):
    test_phrase = r"Download: 23.99 Mbit/s"
    search = TextBeltRequest_object.download_regex.search(test_phrase)
    assert float(search.group(1)) == 23.99


def test_speedtest_log_regex(TextBeltRequest_object, tmpdir):
    test_speedtest_log = tmpdir.join("speedtest.log")
    test_speedtest_log.write("Download: 23.99 Mbit/s")
    TextBeltRequest_object.speedtest_log = test_speedtest_log
    test_average_speed = TextBeltRequest_object.make_average()
    assert float(test_average_speed) == 23.99


def test_make_average(TextBeltRequest_object, tmpdir):
    test_speedtest_log = tmpdir.join("speedtest.log")
    test_speedtest_log.write("Download: 23.99 Mbit/s\nDownload: 28.23 Mbit/s")
    TextBeltRequest_object.speedtest_log = test_speedtest_log
    test_average_speed = TextBeltRequest_object.make_average()
    assert test_average_speed == 26.11


def test_raises_HTTPError(TextBeltRequest_object, mocker):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "https://textbelt.com/text",
            json={
                'quotaRemaining': 79,
                'success': True,
                'textId': '3831502760844259'
            },
            status_code=400)

        mocker.path.object(sendtest.TextBeltRequest, 'make_request', autospec=Truereturn_value=24)
        with pytest.raises(sendtest.requests.HTTPError):
            TextBeltRequest_object.make_request()


#def test_requests_check(TextBeltRequest_object):
