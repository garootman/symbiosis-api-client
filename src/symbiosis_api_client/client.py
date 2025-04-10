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
    ) -> None:
        """Initialize the Symbiosis API client."""
        self._hrc = HttpxRequestClient(
            base_url=base_url,
            httpx_client=httpx_client,
        )
        self._hrc.health_check(raise_exception=True)

        self._chains: list[models.ChainsResponseSchemaItem] = []
        self._tokens: list[models.TokensResponseSchemaItem] = []
        self._routes: list[models.DirectRoutesResponseItem] = []
        self._fees: list[models.FeesResponseItem] = []
        self._swap_limits: list[models.SwapLimitsResponseSchemaItem] = []
        self._swap_durations: list[models.SwapDurationsResponseSchemaItem] = []
        self._swap_configs: list[models.SwapConfigsResponseItem] = []
        self._swap_tiers: list[models.SwapDiscountTiersResponseSchemaItem] = []
        self._swap_chains: list[int] = []

    @property
    def swap_chains(self) -> list[int]:
        """Return a list of chain IDs."""
        if not self._swap_chains:
            self._swap_chains = self._load_swap_chains()
        return self._swap_chains

    def _load_swap_chains(self) -> list[int]:
        response = self._hrc.get_swap_chains()
        self._swap_chains = response.root
        return self._swap_chains

    @property
    def swap_tiers(self) -> list[models.SwapDiscountTiersResponseSchemaItem]:
        if not self._swap_tiers:
            self._swap_tiers = self._load_swap_tiers()
        return self._swap_tiers

    def _load_swap_tiers(self) -> list[models.SwapDiscountTiersResponseSchemaItem]:
        response = self._hrc.get_swap_tiers()
        self._swap_tiers = response.root
        return self._swap_tiers

    @property
    def swap_configs(self) -> list[models.SwapConfigsResponseItem]:
        if not self._swap_configs:
            self._swap_configs = self._load_swap_configs()
        return self._swap_configs

    def _load_swap_configs(self) -> list[models.SwapConfigsResponseItem]:
        response = self._hrc.get_swap_configs()
        self._swap_configs = response.root
        return self._swap_configs

    @property
    def chains(self) -> list[models.ChainsResponseSchemaItem]:
        if not self._chains:
            self._chains = self._load_chains()
        return self._chains

    @property
    def chain_names(self) -> list[str]:
        """Return a list of chain names."""
        return [chain.name for chain in self.chains]

    def _load_chains(self) -> list[models.ChainsResponseSchemaItem]:
        response = self._hrc.get_chains()
        self._chains = response.root
        return self._chains

    @property
    def tokens(self) -> list[models.TokensResponseSchemaItem]:
        if not self._tokens:
            self._tokens = self._load_tokens()
        return self._tokens

    def _load_tokens(self) -> list[models.TokensResponseSchemaItem]:
        response = self._hrc.get_tokens()
        self._tokens = response.root
        return self.tokens

    @property
    def routes(self) -> list[models.DirectRoutesResponseItem]:
        if not self._routes:
            self._routes = self._load_routes()
        return self._routes

    def _load_routes(self) -> list[models.DirectRoutesResponseItem]:
        response = self._hrc.get_direct_routes()
        self._routes = response.root
        return self._routes

    @property
    def fees(self) -> list[models.FeesResponseItem]:
        if not self._fees:
            self._fees = self._load_fees()
        return self._fees

    def _load_fees(self) -> list[models.FeesResponseItem]:
        response = self._hrc.get_fees()
        self._fees = response.fees
        return self._fees

    @property
    def swap_limits(self) -> list[models.SwapLimitsResponseSchemaItem]:
        if not self._swap_limits:
            self._swap_limits = self._load_swap_limits()
        return self._swap_limits

    def _load_swap_limits(self) -> list[models.SwapLimitsResponseSchemaItem]:
        response = self._hrc.get_swap_limits()
        self._swap_limits = response.root
        return self._swap_limits

    @property
    def swap_durations(self) -> list[models.SwapDurationsResponseSchemaItem]:
        if not self._swap_durations:
            self._swap_durations = self._load_swap_durations()
        return self._swap_durations

    def _load_swap_durations(self) -> list[models.SwapDurationsResponseSchemaItem]:
        response = self._hrc.get_swap_durations()
        self._swap_durations = response.root
        return self._swap_durations

    def close(self) -> None:
        """Close the HTTP client."""
        self._hrc.close()

    def _lookup_chain(
        self, chain_name: str | None = None, chain_id: int | None = None
    ) -> models.ChainsResponseSchemaItem | None:
        if chain_name is None and chain_id is None:
            raise ValueError("Either chain_name or chain_id must be provided.")
        if chain_name is not None and chain_id is not None:
            raise ValueError("Only one of chain_name or chain_id must be provided.")
        if chain_name is not None:
            for item in self.chains:
                if item.name == chain_name:
                    return item
        if chain_id is not None:
            for item in self.chains:
                if item.id == chain_id:
                    return item
        return None

    def _lookup_token(
        self, symbol: str, chainId: int
    ) -> models.TokensResponseSchemaItem | None:
        chain = self._lookup_chain(chain_id=chainId)
        if chain is None:
            return None
        for item in self.tokens:
            if item.symbol == symbol and item.chainId == chain.id:
                return item
        return None

    def new_swap(
        self,
        from_chain: str,
        to_chain: str,
        from_token: str,
        to_token: str,
        amount: float,
        recipient: str,
    ):
        """Create a new swap."""

    pass
