"""Business logic for the Symbiosis API client."""

import logging

from .request_client import HttpxRequestClient, httpx, models

logger = logging.getLogger("SymbiosisAPIClient")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class SymbiosisApiClient:
    """Symbiosis API client for interacting with the Symbiosis API."""

    def __init__(
        self,
        base_url: str | None = None,
        httpx_client: httpx.Client | None = None,
        timeout: float = 10.0,
    ) -> None:
        """Initialize the Symbiosis API client."""
        self._hrc = HttpxRequestClient(
            base_url=base_url,
            httpx_client=httpx_client,
            timeout=timeout,
        )
        self._hrc.health_check(raise_exception=True)
        self.chains: list[models.ChainsResponseSchemaItem] = []
        self.tokens: list[models.TokensResponseSchemaItem] = []
        self.direct_routes: list[models.DirectRoutesResponseItem] = []
        self.fees: list[models.FeesResponseItem] = []
        self.swap_limits: list[models.SwapLimitsResponseSchemaItem] = []
        self.swap_durations: list[models.SwapDurationsResponseSchemaItem] = []

    def laod_chains(self) -> list[models.ChainsResponseSchemaItem]:
        response = self._hrc.get_chains()
        self.chains = response.root
        return self.chains

    def laod_tokens(self) -> list[models.TokensResponseSchemaItem]:
        response = self._hrc.get_tokens()
        self.tokens = response.root
        return self.tokens

    def load_direct_routes(self) -> list[models.DirectRoutesResponseItem]:
        response = self._hrc.get_direct_routes()
        self.direct_routes = response.root
        return self.direct_routes

    def load_fees(self) -> list[models.FeesResponseItem]:
        response = self._hrc.get_fees()
        self.fees = response.fees
        # self._fees_updated_at = response.updatedAt
        return self.fees

    def load_swap_limits(self) -> list[models.SwapLimitsResponseSchemaItem]:
        response = self._hrc.get_swap_limits()
        self.swap_limits = response.root
        return self.swap_limits

    def load_swap_durations(self) -> list[models.SwapDurationsResponseSchemaItem]:
        response = self._hrc.get_swap_durations()
        self.swap_durations = response.root
        return self.swap_durations

    def close(self) -> None:
        """Close the HTTP client."""
        self._hrc.close()
