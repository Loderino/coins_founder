from pydantic import BaseModel, Field

class CoinInfo(BaseModel):
    """Request model for sales endpoint."""
    sources: list[str]
    title: str
    country: str
    currency: str
    nominal: str
    year: int
    is_regular: bool
    mintmark: str = Field(default=None)
    material: str = Field(default=None)