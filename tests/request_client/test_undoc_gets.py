import pytest

from symbiosis_api_client import HttpxRequestClient, models


@pytest.fixture
def client():
    clnt = HttpxRequestClient()
    assert clnt.health_check() is True
    yield clnt
    clnt.close()


def test_client_get_swap_configs(client):
    swap_config = client.get_swap_configs()
    assert isinstance(swap_config, models.SwapConfigsResponseSchema)
    assert len(swap_config.root) > 20


def test_get_swap_tiers(client):
    swap_tiers = client.get_swap_tiers()
    assert isinstance(swap_tiers, models.SwapDiscountTiersResponseSchema)
    assert len(swap_tiers.root) > 0


def test_get_swap_chains(client):
    chains = client.get_swap_chains()
    assert isinstance(chains, models.SwapChainsResponseSchema)
    assert len(chains.root) > 0
