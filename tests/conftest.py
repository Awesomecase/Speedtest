from speedtest_sendtest import sendtest
import pytest


@pytest.fixture(scope="function")
def TextBeltRequest_object():
    """Creates a test TextBeltRequest object"""
    test_request = sendtest.TextBeltRequest(
        start_request=False, delete_file=False)
    return test_request
