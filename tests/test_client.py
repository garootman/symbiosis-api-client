from symbiosis_api_client import SymbiosisClient


import pytest


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


def test_client_init_mainnet():
    client = SymbiosisClient(testnet=False)
    assert client.testnet is False
    assert client.client.headers["accept"] == "application/json"
    assert client.client.headers["Content-Type"] == "application/json"
    client.close()


def test_client_init_testnet():
    client = SymbiosisClient(testnet=True)
    assert client.testnet is True
    assert client.client.headers["accept"] == "application/json"
    assert client.client.headers["Content-Type"] == "application/json"
    client.close()


def test_client_health(mainnet_client):
    client = mainnet_client
    assert client.health_check() is True
    client.close()


def test_client_health_testnet(testnet_client):
    client = testnet_client
    assert client.health_check() is True
    client.close()
