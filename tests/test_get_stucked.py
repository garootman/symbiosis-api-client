import pytest

from symbiosis_api_client import SymbiosisClient
from symbiosis_api_client.models import StuckedItem


@pytest.fixture
def client():
    clnt = SymbiosisClient()
    yield clnt
    clnt.close()


@pytest.fixture
def stuck_address():
    # Replace with a valid address for testing
    return "0x1234567890abcdef1234567890abcdef12345678"


def test_get_stucked(client, stuck_address):
    assert client.health_check() is True
    struck = client.get_stucked(stuck_address)
    assert isinstance(struck, list)
    assert all(isinstance(item, StuckedItem) for item in struck)
    # assert len(struck) > 0 # TODO: test when there is some stucked item
