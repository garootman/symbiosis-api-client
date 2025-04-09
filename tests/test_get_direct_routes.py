import pytest

from symbiosis_api_client import SymbiosisClient
from symbiosis_api_client.models import DirectRoutesResponseItem


@pytest.fixture
def client():
    clnt = SymbiosisClient()
    yield clnt
    clnt.close()


def test_client_get_routes(client):
    assert client.health_check() is True
    assert client.direct_routes == []
    routes = client.get_direct_routes()
    assert isinstance(routes, list)
    assert len(routes) > 0
    assert client.direct_routes == routes
    assert all(isinstance(r, DirectRoutesResponseItem) for r in routes)
