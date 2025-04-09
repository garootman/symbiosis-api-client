import pytest

from symbiosis_api_client import SymbiosisClient
from symbiosis_api_client.models import FeesResponseItem


@pytest.fixture
def client():
    clnt = SymbiosisClient()
    yield clnt
    clnt.close()


def test_client_get_fees(client):
    assert client.health_check() is True
    assert client.fees == []
    assert client.fees_updated_at == 0
    assert client.fees_age_seconds > 1700000000
    fees = client.get_fees()
    assert isinstance(fees, list)
    assert len(fees) > 80
    assert all(isinstance(fee, FeesResponseItem) for fee in fees)
    assert client.fees == fees
    assert client.fees_age_seconds < 600
