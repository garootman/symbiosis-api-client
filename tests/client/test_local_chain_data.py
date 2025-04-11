from symbiosis_api_client.check_latest_commit import check_latest_commit
from symbiosis_api_client.load_static_chain_data import (
    load_static_chains,
    models_static,
)

# import pytest


def test_latest_commit():
    """Test that the latest commit in mainnet.ts is the same as the one in the repo."""
    assert check_latest_commit() is True


def test_load_static_chains():
    """Test that the static chains are loaded correctly."""
    data = load_static_chains()
    assert isinstance(data, models_static.StaticConfigModel)
