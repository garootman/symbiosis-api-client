import logging
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

"(^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$)*(^0x[a-fA-F0-9]{40}$)*"


def to_number(value) -> Decimal | None:
    try:
        return Decimal(str(value))
    except Exception:
        return None


class ChainsResponseItem(BaseModel):
    id: int
    name: str
    explorer: str
    icon: str | None = None


class TokensResponseItem(BaseModel):
    symbol: str
    icon: str | None = None
    address: str
    chainId: int
    decimals: int


class DirectRoutesResponseItem(BaseModel):
    originChainId: int
    originToken: str
    destinationChainId: int
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


class SwapLimitsResponseItem(BaseModel):
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


class TokenAmount(BaseModel):
    address: str
    chainId: int
    chainIdFrom: int | None = None
    decimals: int
    symbol: str
    icon: str | None = None
    amount: int

    @field_validator("amount", mode="before")
    @classmethod
    def check_amount(cls, v):
        num = to_number(v)
        if num is None:
            raise ValueError(f"Amount {v} is not a number")
        return int(num)


class StuckedResponseItem(BaseModel):
    hash: str
    chainId: int
    createdAt: str
    tokenAmount: TokenAmount


class Status(BaseModel):
    code: float
    text: str


class Tx11(BaseModel):
    hash: str
    chainId: int
    tokenAmount: TokenAmount | None = None
    time: str
    address: str


class TxIn(BaseModel):
    hash: str
    chainId: int
    tokenAmount: TokenAmount
    time: str
    address: str


class TransitTokenSent(BaseModel):
    address: str
    chainId: int
    chainIdFrom: int | None = None
    decimals: int
    symbol: str
    icon: str | None = None
    amount: int

    @field_validator("amount", mode="before")
    @classmethod
    def check_amount(cls, v):
        num = to_number(v)
        if num is None:
            raise ValueError(f"Amount {v} is not a number")
        return int(num)


class TxResponseSchema(BaseModel):
    status: Status
    tx: Tx11 | None = None
    txIn: TxIn | None = None
    transitTokenSent: TransitTokenSent | None = None


class TokenOut(BaseModel):
    address: str
    chainId: int
    chainIdFrom: int | None = None
    decimals: int
    symbol: str | None = None
    icon: str | None = None


class MiddlewareCall(BaseModel):
    address: str
    data: str
    offset: float


class RevertableAddress(BaseModel):
    chainId: int
    address: str


class SwapRequestSchema(BaseModel):
    tokenAmountIn: TokenAmount
    tokenOut: TokenOut
    from_: str = Field(..., alias="from")

    to: str
    slippage: int
    middlewareCall: MiddlewareCall | None = None
    revertableAddresses: list[RevertableAddress] | None = None
    selectMode: str | None = None
    partnerAddress: str | None = None
    refundAddress: str | None = None
