from pydantic import BaseModel


class PriceBaseSchema(BaseModel):
    id: int
    ticker: str
    price: float
    timestamp: int


class PriceReadSchema(PriceBaseSchema):
    pass
