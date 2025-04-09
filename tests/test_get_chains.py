import pytest

from symbiosis_api_client import SymbiosisClient
from symbiosis_api_client.models import ChainsResponseSchemaItem


@pytest.fixture
def client():
    clnt = SymbiosisClient()
    yield clnt
    clnt.close()


def test_client_get_chains(client):
    assert client.health_check() is True
    assert client.chains == []
    chains = client.get_chains()
    assert isinstance(chains, list)
    assert len(chains) > 30
    assert all(isinstance(chain, ChainsResponseSchemaItem) for chain in chains)
    assert client.chains == chains
