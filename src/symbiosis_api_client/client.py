import logging
from datetime import datetime

import httpx

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
            logger.error(
                f"Symbiosis API is not healthy. Status code: {response.status_code}"
            )
            if raise_exception:
                raise Exception("Symbiosis API is not healthy.")
            return False

    def get_chains(self) -> list[models.ChainsResponseSchemaItem]:
        response = self.client.get(self.base_url + "v1/chains")
        if not response.is_success:
            msg = f"Error fetching chains: {response.status_code}, {response.text}"
            logger.error(msg)
            return []
        # convert to pydantic model of ChainsResponseSchema
        chains = []
        chains_list = response.json()
        if not chains_list:
            logger.error("Chains list is empty.")
            return []
        if not isinstance(chains_list, list):
            logger.error("Chains list is not a list.")
            return []
        for chain in response.json():
            chain_model = models.ChainsResponseSchemaItem(**chain)
            chains.append(chain_model)
        logger.info(f"Fetched {len(chains)} chains.")
        self.chains = chains
        return chains

    def get_tokens(self) -> list[models.TokensResponseSchemaItem]:
        response = self.client.get(self.base_url + "v1/tokens")

        if not response.is_success:
            msg = f"Error fetching tokens: {response.status_code}, {response.text}"
            logger.error(msg)
            return []
        tokens = response.json()
        if not tokens:
            logger.error("Tokens list is empty.")
            return []
        if not isinstance(tokens, list):
            logger.error("Tokens list is not a list.")
            return []
        tokens_list = []
        for token in tokens:
            token_model = models.TokensResponseSchemaItem(**token)
            tokens_list.append(token_model)
        logger.info(f"Fetched {len(tokens_list)} tokens.")
        self.tokens = tokens_list
        return tokens_list

    def get_direct_routes(self) -> list:
        # get direct routes from the API
        response = self.client.get(self.base_url + "/v1/direct-routes")
        if not response.is_success:
            msg = (
                f"Error fetching direct routes: {response.status_code}, {response.text}"
            )
            logger.error(msg)
            return []
        routes = response.json()
        if not routes:
            logger.error("Routes list is empty.")
            return []
        if not isinstance(routes, list):
            logger.error("Routes list is not a list.")
            return []
        routes_list = []
        for route in routes:
            route_model = models.DirectRoutesResponseItem(**route)
            routes_list.append(route_model)

        self.direct_routes = routes_list
        logger.info(f"Fetched {len(routes_list)} direct routes.")
        return routes_list

    def get_fees(self) -> list:
        response = self.client.get(self.base_url + "/v1/fees")
        if not response.is_success:
            msg = f"Error fetching fees: {response.status_code}, {response.text}"
            logger.error(msg)
            return []
        fees = response.json()
        if not fees:
            logger.error("Fees object is empty.")
            return []
        fees_list = fees.get("fees", [])
        if not fees_list:
            logger.error("Fees list is empty.")
            return []
        if not isinstance(fees_list, list):
            logger.error("Fees list is not a list.")
            return []
        save_list = []
        for fee in fees_list:
            fee_model = models.FeesResponseItem(**fee)
            save_list.append(fee_model)
        self.fees_updated_at = int(fees.get("updatedAt", 0)) // 1000
        self.fees = save_list
        logger.info(f"Fetched {len(save_list)} fees.")
        # convert to pydantic model of FeesResponseSchema
        return save_list

    def get_swap_limits(self):
        response = self.client.get(self.base_url + "/v1/swap-limits")
        if not response.is_success:
            msg = f"Error fetching swap limits: {response.status_code}, {response.text}"
            logger.error(msg)
            return {}
        limit_list = response.json()
        if not limit_list:
            logger.error("Swap limits list is empty.")
            return {}
        if not isinstance(limit_list, list):
            logger.error("Swap limits list is not a list.")
            return {}
        return_list = []
        for limit in limit_list:
            limit_model = models.SwapLimitsItem(**limit)
            return_list.append(limit_model)
        self.swap_limits = return_list
        return return_list


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
