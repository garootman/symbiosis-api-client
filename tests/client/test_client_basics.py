import pytest

from symbiosis_api_client import SymbiosisApiClient, models


@pytest.fixture
def client():
    client = SymbiosisApiClient()
    yield client
    client.close()


def test_load_markets(client):
    client.laod_chains()
    assert client.chains
    assert isinstance(client.chains, list)
    assert all(
        isinstance(chain, models.ChainsResponseSchemaItem) for chain in client.chains
    )


def test_load_tokens(client):
    client.laod_tokens()
    assert client.tokens
    assert isinstance(client.tokens, list)
    assert all(
        isinstance(token, models.TokensResponseSchemaItem) for token in client.tokens
    )


def test_load_direct_routes(client):
    client.load_direct_routes()
    assert client.direct_routes
    assert isinstance(client.direct_routes, list)
    assert all(
        isinstance(route, models.DirectRoutesResponseItem)
        for route in client.direct_routes
    )


def test_load_fees(client):
    client.load_fees()
    assert client.fees
    assert isinstance(client.fees, list)
    assert all(isinstance(fee, models.FeesResponseItem) for fee in client.fees)


def test_load_swap_limits(client):
    client.load_swap_limits()
    assert client.swap_limits
    assert isinstance(client.swap_limits, list)
    assert all(
        isinstance(limit, models.SwapLimitsResponseSchemaItem)
        for limit in client.swap_limits
    )


def test_load_swap_durations(client):
    client.load_swap_durations()
    assert client.swap_durations
    assert isinstance(client.swap_durations, list)
    assert all(
        isinstance(duration, models.SwapDurationsResponseSchemaItem)
        for duration in client.swap_durations
    )
