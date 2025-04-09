import logging
from decimal import Decimal

from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)


def to_number(value) -> Decimal | None:
    try:
        return Decimal(str(value))
    except Exception:
        return None


class ChainsResponseSchemaItem(BaseModel):
    id: float
    name: str
    explorer: str
    icon: str


class TokensResponseSchemaItem(BaseModel):
    symbol: str
    icon: str
    address: str
    chainId: int
    decimals: int


class DirectRoutesResponseItem(BaseModel):
    originChainId: float
    originToken: str
    destinationChainId: float
    destinationToken: str


class FeesResponseItem(BaseModel):
    chainId: int
    address: str
    symbol: str
    decimals: int
    value: int

    @field_validator("value", mode="before")
    @classmethod
    def check_value(cls, v):
        num = to_number(v)
        if num is None:
            raise ValueError(f"Value {v} is not a number")
        return int(num)


class SwapLimitsItem(BaseModel):
    chainId: int
    address: str
    min: int
    max: int
    decimals: int

    @field_validator("min", mode="before")
    @classmethod
    def check_min(cls, v):
        num = to_number(v)
        if num is None:
            raise ValueError(f"Min {v} is not a number")
        return int(num)

    @field_validator("max", mode="before")
    @classmethod
    def check_max(cls, v):
        num = to_number(v)
        if num is None:
            raise ValueError(f"Max {v} is not a number")
        return int(num)
