from pydantic import BaseModel

# from typing import Any ,Optional


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
