import logging
from datetime import datetime

import httpx

from . import models as models
from .model_list_adapter import TypeAdapter, list_adapter

logger = logging.getLogger(__name__)


class SymbiosisClient:
    def __init__(self, timeout: float = 10.0) -> None:
        """Initialize the SymbiosisAPI client."""
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        self.chains: list = []
        self.tokens: list = []
        self.direct_routes: list = []
        self.fees: list = []
        self.fees_updated_at: int = 0
        self.swap_limits: list = []

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    @property
    def base_url(self):
        # if self.testnet:
        #    return "https://api.testnet.symbiosis.finance/crosschain/"
        return "https://api.symbiosis.finance/crosschain/"

    @property
    def fees_age_seconds(self) -> int:
        return int(datetime.now().timestamp()) - self.fees_updated_at

    def health_check(self, raise_exception: bool = False) -> bool:
        # use self.client to check the health of the API
        response = self.client.get(self.base_url + "health-check")
        if response.status_code == 200:
            logger.info("Symbiosis API is healthy.")
            return True
        else:
            msg = (
                f"Symbiosis API is not healthy.{response.status_code} - {response.text}"
            )
            logger.error(msg)
            if raise_exception:
                raise Exception(msg)
            return False

    def get_chains(self) -> list[models.ChainsResponseItem]:
        """Returns the chains available for swapping."""
        response = self.client.get(self.base_url + "v1/chains")
        if not response.is_success:
            msg = f"Error fetching chains: {response.status_code}, {response.text}"
            logger.error(msg)
            return []
        self.chains = list_adapter(response.json(), models.ChainsResponseItem)
        logger.info(f"Fetched {len(self.chains)} chains.")
        return self.chains

    def get_tokens(self) -> list[models.TokensResponseItem]:
        """Returns the tokens available for swapping."""

        response = self.client.get(self.base_url + "v1/tokens")
        if not response.is_success:
            msg = f"Error fetching tokens: {response.status_code}, {response.text}"
            logger.error(msg)
            return []
        self.tokens = list_adapter(response.json(), models.TokensResponseItem)
        logger.info(f"Fetched {len(self.tokens)} tokens.")
        return self.tokens

    def get_direct_routes(self) -> list[models.DirectRoutesResponseItem]:
        """Returns the direct routes for all tokens."""

        response = self.client.get(self.base_url + "/v1/direct-routes")
        if not response.is_success:
            msg = f"Error fetching routes: {response.status_code}, {response.text}"
            logger.error(msg)
            return []
        self.direct_routes = list_adapter(
            response.json(), models.DirectRoutesResponseItem
        )
        logger.info(f"Fetched {len(self.direct_routes)} direct routes.")
        return self.direct_routes

    def get_fees(self) -> list[models.FeesResponseItem]:
        """Returns the current fees for all tokens."""

        response = self.client.get(self.base_url + "/v1/fees")
        if not response.is_success:
            msg = f"Error fetching fees: {response.status_code}, {response.text}"
            logger.error(msg)
            return []
        self.fees = list_adapter(
            response.json().get("fees", []), models.FeesResponseItem
        )
        self.fees_updated_at = int(response.json().get("updatedAt", 0)) // 1000
        logger.info(f"Fetched {len(self.fees)} fees.")
        return self.fees

    def get_swap_limits(self) -> list[models.SwapLimitsResponseItem]:
        """Returns the swap limits for all tokens."""

        response = self.client.get(self.base_url + "/v1/swap-limits")
        if not response.is_success:
            msg = f"Error fetching swap limits: {response.status_code}, {response.text}"
            logger.error(msg)
            return []
        self.swap_limits = list_adapter(response.json(), models.SwapLimitsResponseItem)
        logger.info(f"Fetched {len(self.swap_limits)} swap limits.")
        return self.swap_limits

    def get_stucked(self, address: str) -> list[models.StuckedResponseItem]:
        """Returns a list of stuck cross-chain operations associated with the specified address."""
        response = self.client.get(self.base_url + f"/v1/stucked/{address}")
        if not response.is_success:
            msg = f"Error fetching stucked operations: {response.status_code}, {response.text}"
            logger.error(msg)
            return []
        return list_adapter(response.json(), models.StuckedResponseItem)

    def get_transaction(
        self, chain_id: str, txhash: str
    ) -> models.TxResponseSchema | None:
        """Returns the operation by its transaction hash."""
        response = self.client.get(self.base_url + f"/v1/tx/{chain_id}/{txhash}")
        if not response.is_success:
            msg = f"Error fetching transaction: {response.status_code}, {response.text}"
            logger.error(msg)
            return None
        adapter = TypeAdapter(models.TxResponseSchema)
        return adapter.validate_python(response.json())


"""


    def __swap_tokens(
        self,
        from_chain_id,
        to_chain_id,
        from_token_address,
        to_token_address,
        amount,
        from_address,
        to_address,
    ):

        Perform a cross-chain token swap using the Symbiosis Finance API.

        A General Workflow for Performing a Swap Using the Symbiosis API:
            Call /v1/chains to get a list of available blockchain networks.
            Call /v1/swap-limits to verify swap limits (the minimum and maximum allowed swap amounts).
            Call /v1/swap to get the calldata (payload) needed to execute the swap through Symbiosis protocol.
            If the source token is not a native gas token (e.g., ERC-20 tokens on EVM chains), approve the smart contract to spend the user's tokens.
            Sign the calldata obtained in Step 3 using the wallet. Submit the transaction to the source blockchain.
            Since network conditions constantly change, calldata must be regenerated periodically (e.g., every 30 seconds) to ensure it remains valid before execution.
            Call /v1/tx/{chainID}/{txHash} to monitor the progress of the swap. This endpoint provides real-time status updates for cross-chain operations

        :param api_url: The base URL of the Symbiosis Finance API.
        :param from_chain_id: The chain ID of the source blockchain.
        :param to_chain_id: The chain ID of the destination blockchain.
        :param from_token_address: The token address on the source blockchain.
        :param to_token_address: The token address on the destination blockchain.
        :param amount: The amount of tokens to swap.
        :param from_address: The wallet address initiating the swap.
        :param to_address: The wallet address receiving the swapped tokens.

        :return: The response from the Symbiosis Finance API.
        endpoint = "/v1/swap"
        url = self.base_url + endpoint
        payload = {
            "fromChainId": from_chain_id,
            "toChainId": to_chain_id,
            "fromTokenAddress": from_token_address,
            "toTokenAddress": to_token_address,
            "amount": amount,
            "from": from_address,
            "to": to_address,
        }

        try:
            with httpx.Client() as client:
                response = client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            return {"error": str(e)}
"""
