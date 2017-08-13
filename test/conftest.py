from speedtest_sendtest import sendtest
import pytest


@pytest.fixture(scope="function")
def create_TextBeltRequest_object():
    test_request = sendtest.TextBeltRequest()
    yield
