from symbiosis_api_client.check_latest_commit import check_latest_commit

# import pytest


def test_latest_commit():
    """Test that the latest commit in mainnet.ts is the same as the one in the repo."""
    assert check_latest_commit() is True
