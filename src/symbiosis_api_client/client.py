import logging

import httpx

# from . import models as models
from . import models as models

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

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    @property
    def base_url(self):
        # if self.testnet:
        #    return "https://api.testnet.symbiosis.finance/crosschain/"
        return "https://api.symbiosis.finance/crosschain/"

    def health_check(self, raise_exception: bool = False) -> bool:
        # use self.client to check the health of the API
        response = self.client.get(self.base_url + "health-check")
        if response.is_success:
            logger.info("Symbiosis API is healthy.")
            return True
        else:
            msg = (
                f"Symbiosis API is not healthy.{response.status_code} - {response.text}"
            )
            logger.error(msg)
            if raise_exception:
                response.raise_for_status()
            return False

    def __get_raise_validate(
        self, url: str, model: models.BaseModel
    ) -> models.BaseModel:
        """Generic method to get data from the API and validate it against a model."""
        response = self.client.get(url)
        response.raise_for_status()
        return model.model_validate(response.json())

    def get_chains(self) -> models.ChainsResponseSchema:
        """Returns the chains available for swapping."""
        response = self.client.get(self.base_url + "v1/chains")
        response.raise_for_status()
        return models.ChainsResponseSchema.model_validate(response.json())

    def get_tokens(self) -> models.TokensResponseSchema:
        """Returns the tokens available for swapping."""
        response = self.client.get(self.base_url + "v1/tokens")
        response.raise_for_status()
        return models.TokensResponseSchema.model_validate(response.json())

    def get_direct_routes(self) -> list[models.DirectRoutesResponseItem]:
        """Returns the direct routes for all tokens."""
        response = self.client.get(self.base_url + "/v1/direct-routes")
        response.raise_for_status()
        return models.DirectRoutesResponse.model_validate(response.json())

    def get_fees(self) -> models.FeesResponseSchema:
        """Returns the current fees for all tokens."""
        response = self.client.get(self.base_url + "/v1/fees")
        response.raise_for_status()
        return models.FeesResponseSchema.model_validate(response.json())

    def get_swap_limits(self) -> models.SwapLimitsResponseSchema:
        """Returns the swap limits for all tokens."""
        response = self.client.get(self.base_url + "/v1/swap-limits")
        response.raise_for_status()
        return models.SwapLimitsResponseSchema.model_validate(response.json())

    def get_stucked(
        self, payload: models.StuckedRequestSchema
    ) -> models.StuckedResponseSchema:
        """Returns a list of stuck cross-chain operations associated with the specified address."""
        response = self.client.get(self.base_url + f"/v1/stucked/{payload.address}")
        response.raise_for_status()
        return models.StuckedResponseSchema.model_validate(response.json())

    def get_transaction(self, payload: models.Tx12) -> models.TxResponseSchema:
        """Returns the operation by its transaction hash."""
        response = self.client.get(
            self.base_url + f"/v1/tx/{payload.chainId}/{payload.transactionHash}"
        )
        response.raise_for_status()
        return models.TxResponseSchema.model_validate(response.json())


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
