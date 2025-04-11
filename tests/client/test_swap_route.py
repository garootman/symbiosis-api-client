import pytest

from symbiosis_api_client import SymbiosisApiClient, models


@pytest.fixture
def client():
    c = SymbiosisApiClient()
    yield c
    c.close()


@pytest.fixture
def routes_list():
    return [
        (
            {
                "chain_from": "Ethereum",
                "token_from": "USDT",
                "chain_to": "Tron",
                "token_to": "USDT",
                "amount": 100,
                "slippage": 200,
                "sender": "0x40d3eE6c444E374c56f8f0d9480DF40f2B6E6aEd",
                "recipient": "0x40d3eE6c444E374c56f8f0d9480DF40f2B6E6aEd",
            },
            {
                "chain_from": "Ethereum",
            },
        ),
    ]


def test_check_lookup_route(routes_list, client):
    for rr in routes_list:
        route_dict, _ = rr
        swap = client.create_swap(**route_dict)
        assert isinstance(swap, models.SwapResponseSchema)
