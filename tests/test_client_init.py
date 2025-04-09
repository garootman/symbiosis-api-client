import pytest

from symbiosis_api_client import SymbiosisClient


@pytest.fixture
def client():
    clnt = SymbiosisClient()
    yield clnt
    clnt.close()


def test_client_init_mainnet():
    client = SymbiosisClient()
    assert client.client.headers["accept"] == "application/json"
    assert client.client.headers["Content-Type"] == "application/json"
    client.close()


def test_client_health(client):
    assert client.health_check() is True
    client.close()


def test_bad_request(client):
    assert client.health_check() is True
    req = client.client.get(client.base_url + "v1/bad_request")
    assert req.status_code == 404
