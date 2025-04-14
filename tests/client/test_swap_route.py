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
        # Eth USDT -> BSC USDT
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
                "raise_exception": True,
            },
            {
                "some_field_to_check": "its_value",
            },
        ),
        # Eth USDT -> TON USDT
        (
            {
                "chain_from": "Ethereum",
                "token_from": "USDT",
                "chain_to": "TON",
                "token_to": "USDT",
                "amount": 100,
                "slippage": 200,
                "sender": "0x40d3eE6c444E374c56f8f0d9480DF40f2B6E6aEd",
                "recipient": "UQD9qA1MlNDFAM-oVAFPERJlmeOF6Dl6BLI3EtS4BopVC3Ci",
                "raise_exception": True,
            },
            {
                "some_field_to_check": "its_value",
            },
        ),
    ]


correct_request_eth_usdt_ton_usdt = {
    "tokenAmountIn": {
        "chainId": 1,
        "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # it is a mainnet address for Ethereum: USDT
        "symbol": "USDT",
        "decimals": 6,
        "amount": "2500000000",
    },
    "tokenOut": {
        "chainId": 85918,
        "address": "0x9328Eb759596C38a25f59028B146Fecdc3621Dfe",  # it is a mainnet address for TON: USDT
        "symbol": "USDT",
        "decimals": 6,
    },
    "from": "0x40d3eE6c444E374c56f8f0d9480DF40f2B6E6aEd",
    "to": "UQD9qA1MlNDFAM-oVAFPERJlmeOF6Dl6BLI3EtS4BopVC3Ci",
    "slippage": 200,
    "selectMode": "best_return",
    "refundAddress": "",
}

current_request = {
    "tokenAmountIn": {
        "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "chainId": 1,
        "decimals": 6,
        "symbol": "USDT",
        "amount": "100000000",
    },
    "tokenOut": {
        "address": "",
        "decimals": 6,
        "symbol": "USDT",
    },
    "from": "0x40d3eE6c444E374c56f8f0d9480DF40f2B6E6aEd",
    "to": "UQD9qA1MlNDFAM-oVAFPERJlmeOF6Dl6BLI3EtS4BopVC3Ci",
    "slippage": 200,
    "selectMode": "best_return",
}


def test_check_lookup_route(routes_list, client):
    for rr in routes_list[:1]:
        route_dict, _ = rr
        swap = client.create_swap(**route_dict)
        assert isinstance(swap, models.SwapResponseSchema)
