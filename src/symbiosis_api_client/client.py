import logging
from datetime import timedelta
from typing import Optional

import httpx

from . import models as models
from .limiter import SyncRateLimitedTransport

logger = logging.getLogger(__name__)

API_BASE_URL = "https://api.symbiosis.finance/crosschain/"


class SymbiosisClient:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SymbiosisClient, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        base_url: str = API_BASE_URL,
        httpx_client: Optional[httpx.Client] = None,
        timeout: float = 10.0,
    ) -> None:
        """Initialize the SymbiosisAPI client, singleton + rate limiting."""

        if not httpx_client:
            transport = SyncRateLimitedTransport.create(
                rate=1, period=timedelta(seconds=1)
            )
            httpx_client = httpx.Client(
                base_url=base_url,
                transport=transport,
                timeout=timeout,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                },
            )
        self.client = httpx_client

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def health_check(self, raise_exception: bool = False) -> bool:
        # use self.client to check the health of the API
        response = self.client.get("/health-check")
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

    def get_chains(self) -> models.ChainsResponseSchema:
        """Returns the chains available for swapping."""
        response = self.client.get("/v1/chains")
        response.raise_for_status()
        return models.ChainsResponseSchema.model_validate(response.json())

    def get_tokens(self) -> models.TokensResponseSchema:
        """Returns the tokens available for swapping."""
        response = self.client.get("/v1/tokens")
        response.raise_for_status()
        return models.TokensResponseSchema.model_validate(response.json())

    def get_direct_routes(self) -> models.DirectRoutesResponse:
        """Returns the direct routes for all tokens."""
        response = self.client.get("/v1/direct-routes")
        response.raise_for_status()
        return models.DirectRoutesResponse.model_validate(response.json())

    def get_fees(self) -> models.FeesResponseSchema:
        """Returns the current fees for all tokens."""
        response = self.client.get("/v1/fees")
        response.raise_for_status()
        return models.FeesResponseSchema.model_validate(response.json())

    def get_swap_limits(self) -> models.SwapLimitsResponseSchema:
        """Returns the swap limits for all tokens."""
        response = self.client.get("/v1/swap-limits")
        response.raise_for_status()
        return models.SwapLimitsResponseSchema.model_validate(response.json())

    def get_swap_durations(self) -> models.SwapDurationsResponseSchema:
        """Returns the swap limits for all tokens."""
        response = self.client.get("/v1/swap-durations")
        response.raise_for_status()
        return models.SwapDurationsResponseSchema.model_validate(response.json())

    def get_stucked(
        self, payload: models.StuckedRequestSchema
    ) -> models.StuckedResponseSchema:
        """Returns a list of stuck cross-chain operations associated with the specified address."""
        response = self.client.get(f"/v1/stucked/{payload.address}")
        response.raise_for_status()
        return models.StuckedResponseSchema.model_validate(response.json())

    def get_transaction(self, payload: models.Tx12) -> models.TxResponseSchema:
        """Returns the operation by its transaction hash."""
        response = self.client.get(
            f"/v1/tx/{payload.chainId}/{payload.transactionHash}"
        )
        response.raise_for_status()
        return models.TxResponseSchema.model_validate(response.json())

    def post_swap(
        self,
        payload: models.SwapRequestSchema,
    ) -> models.SwapResponseSchema:
        """Performs a cross-chain swap using the Symbiosis Finance API.

        :param payload: The payload containing the swap details.
        :return: The response from the Symbiosis Finance API.
        """

        payload_dump = payload.model_dump(exclude_none=True)
        response = self.client.post("/v1/swap", json=payload_dump)
        response.raise_for_status()
        return models.SwapResponseSchema.model_validate(response.json())

    def post_revert(
        self, payload: models.RevertRequestSchema
    ) -> models.RevertResponseSchema:
        """Returns calldata required to revert a stuck cross-chain operation.

        Data includes: swapping, bridging, zapping, interchain communicating.
        If a cross-operation gets stuck, Symbiosis automatically reverts such swaps.

        :param payload: The payload containing the revert details.
        :return: The response from the Symbiosis Finance API.
        """
        payload_dump = payload.model_dump(exclude_none=True)
        response = self.client.post("/v1/revert", json=payload_dump)
        response.raise_for_status()
        return models.RevertResponseSchema.model_validate(response.json())

    # TODO: Batch TX
    # TODO: Zapping
