import pytest

# from dotenv import load_dotenv
# load_dotenv()
from symbiosis_api_client import SymbiosisClient, models


@pytest.fixture
def client():
    clnt = SymbiosisClient()
    yield clnt
    clnt.close()


@pytest.fixture
def txndata():
    txndata = [
        {
            "chain": 56,  # BNB
            "hash": "0x6bb1d7b4709c395da1579f7ce5a95fb01026044c72a46be538921e443a615bfd",
        },
        {
            "chain": 43114,  # avalanche
            "hash": "0x8028a927848e99de1c39a256ac0a562da5e17a57683fd0b11a9788787c441169",
        },
        {
            "chain": 137,  # polygon
            "hash": "0xb038fedfa8234409bdcc74d32a5ff35cd44628ab5afc82a64aadd97478e090f5",
        },
        {
            "chain": 42161,  # arbitrum
            "hash": "0x1e4037e0bcc6224b2a1c1af4f35e7d01a9909f04f39d49ce0ae06b8c1be87c6e",
        },
    ]
    txn_models = []
    for tx in txndata:
        txn_models.append(
            models.Tx12(
                chainId=tx["chain"],
                transactionHash=tx["hash"],
            )
        )
    return txn_models


def test_get_transaction(client, txndata):
    for txn in txndata:
        tnx_info = client.get_transaction(payload=txn)
        assert isinstance(tnx_info, models.TxResponseSchema)
        assert tnx_info.status.text.lower() == "success"
