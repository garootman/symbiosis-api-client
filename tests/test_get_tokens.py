import pytest

from symbiosis_api_client import SymbiosisClient
from symbiosis_api_client.models import TokensResponseSchemaItem


@pytest.fixture
def client():
    clnt = SymbiosisClient()
    yield clnt
    clnt.close()


def test_client_get_tokens(client):
    assert client.health_check() is True
    assert client.tokens == []
    tokens = client.get_tokens()
    assert isinstance(tokens, list)
    assert len(tokens) > 30
    assert all(isinstance(token, TokensResponseSchemaItem) for token in tokens)
    assert client.tokens == tokens
