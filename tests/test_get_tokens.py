import pytest

from symbiosis_api_client import SymbiosisClient
from symbiosis_api_client.models import TokensResponseSchemaItem


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


def test_client_get_tokens(mainnet_client):
    client = mainnet_client
    assert client.health_check() is True
    assert client.tokens == []
    tokens = client.get_tokens()
    assert isinstance(tokens, list)
    assert len(tokens) > 30
    assert all(isinstance(token, TokensResponseSchemaItem) for token in tokens)
    assert client.tokens == tokens
    for token in tokens:
        assert token.address is not None
        assert token.chainId is not None
        assert token.decimals is not None
        assert token.symbol is not None


def test_client_get_chains_testnet(testnet_client):
    client = testnet_client
    assert client.health_check() is True
    tokens = client.get_tokens()
    assert isinstance(tokens, list)
    # TODO: when testnet has tokens, apply tests for testnet
    # assert len(tokens) > 5
    # assert all(isinstance(token, TokensResponseSchemaItem) for token in tokens)
    # assert client.tokens == tokens
    # for token in tokens:
    #    assert token.address is not None
    #    assert token.chainId is not None
    #    assert token.decimals is not None
    #    assert token.symbol is not None
