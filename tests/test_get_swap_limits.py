import pytest

from symbiosis_api_client import SymbiosisClient
from symbiosis_api_client.models import SwapLimitsItem


@pytest.fixture
def client():
    clnt = SymbiosisClient()
    yield clnt
    clnt.close()


def test_client_get_chains(client):
    assert client.health_check() is True
    assert client.swap_limits == []
    limits = client.get_swap_limits()
    assert isinstance(limits, list)
    assert len(limits) > 100
    assert client.swap_limits == limits
    assert all(isinstance(limit, SwapLimitsItem) for limit in limits)
