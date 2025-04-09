from pydantic import BaseModel  # , Field


class ChainsResponseSchemaItem(BaseModel):
    id: float
    name: str
    explorer: str
    icon: str
