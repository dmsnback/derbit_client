from pydantic import BaseModel, Field


class PriceBaseSchema(BaseModel):
    id: int
    ticker: str = Field(..., description="Название тикета('BTC_USD', 'ETH_USD')")
    price: int
    timestamp: int


class PriceReadSchema(PriceBaseSchema):
    pass
