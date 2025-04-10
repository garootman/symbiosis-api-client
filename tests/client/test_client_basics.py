import pytest

from symbiosis_api_client import SymbiosisApiClient, models


@pytest.fixture
def client():
    c = SymbiosisApiClient()
    yield c
    c.close()


def test_load_chains(client):
    assert client._chains == []
    chains = client._load_chains()
    assert len(chains) > 40
    assert isinstance(chains, list)
    assert all(
        isinstance(chain, models.ChainsResponseSchemaItem) for chain in client._chains
    )
    assert client._chains == chains
    assert client.chains == chains


def test_load_tokens(client):
    assert client._tokens == []
    tokens = client._load_tokens()
    assert len(tokens) > 100
    assert isinstance(tokens, list)
    assert all(
        isinstance(token, models.TokensResponseSchemaItem) for token in client._tokens
    )
    assert client._tokens == tokens
    assert client.tokens == tokens


def test_load_routes(client):
    assert client._routes == []
    routes = client._load_routes()
    assert len(routes) > 2500
    assert isinstance(routes, list)
    assert all(
        isinstance(route, models.DirectRoutesResponseItem) for route in client._routes
    )
    assert client._routes == routes
    assert client.routes == routes


def test_load_fees(client):
    assert client._fees == []
    fees = client._load_fees()
    assert len(fees) > 80
    assert isinstance(fees, list)
    assert all(isinstance(fee, models.FeesResponseItem) for fee in client._fees)
    assert client._fees == fees
    assert client.fees == fees


def test_load_swap_limits(client):
    assert client._swap_limits == []
    swap_limits = client._load_swap_limits()
    assert len(swap_limits) > 20
    assert isinstance(swap_limits, list)
    assert all(
        isinstance(limit, models.SwapLimitsResponseSchemaItem)
        for limit in client._swap_limits
    )
    assert client._swap_limits == swap_limits
    assert client.swap_limits == swap_limits


def test_load_swap_durations(client):
    assert client._swap_durations == []
    swap_durations = client._load_swap_durations()
    assert len(swap_durations) > 20
    assert isinstance(swap_durations, list)
    assert all(
        isinstance(duration, models.SwapDurationsResponseSchemaItem)
        for duration in client._swap_durations
    )
    assert client._swap_durations == swap_durations
    assert client.swap_durations == swap_durations
