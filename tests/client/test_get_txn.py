import pytest

from symbiosis_api_client import SymbiosisApiClient, models


@pytest.fixture
def client():
    c = SymbiosisApiClient()
    yield c
    c.close()


def test_get_txn(client):
    txn_hash = "0xe514ea90e4bdb3947a41497aef4e03eec2210a964518ef1657a5ec09676c7435"
    txn = client.get_txn_status(chain_name="Ethereum", txn_hash=txn_hash)
    import json

    jsondata = txn.model_dump(exclude_none=True, by_alias=True)
    with open("123-2.json", "w") as f:
        f.write(json.dumps(jsondata, indent=4))
    assert isinstance(txn, models.TxResponseSchema)
    assert txn.status.text == "Success"
