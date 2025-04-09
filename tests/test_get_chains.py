import pytest

from symbiosis_api_client import SymbiosisClient
from symbiosis_api_client.models import ChainsResponseSchemaItem


@pytest.fixture
def mainnet_client():
    client = SymbiosisClient(testnet=False)
    yield client
    client.close()


@pytest.fixture
def testnet_client():
    client = SymbiosisClient(testnet=True)
    yield client
    client.close()


def test_client_get_chains(mainnet_client):
    client = mainnet_client
    assert client.health_check() is True
    chains = client.get_chains()
    assert isinstance(chains, list)
    assert len(chains) > 30
    assert all(isinstance(chain, ChainsResponseSchemaItem) for chain in chains)
    assert client.chains == chains


def test_client_get_chains_testnet(testnet_client):
    client = testnet_client
    assert client.health_check() is True
    chains = client.get_chains()
    assert isinstance(chains, list)
    assert len(chains) > 5
    assert all(isinstance(chain, ChainsResponseSchemaItem) for chain in chains)
    assert client.chains == chains


def test_bad_request(mainnet_client):
    client = mainnet_client
    assert client.health_check() is True
    req = client.client.get(client.base_url + "v1/bad_request")
    assert req.status_code == 404
