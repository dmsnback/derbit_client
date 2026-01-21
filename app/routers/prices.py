from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.price_crud import CRUDPrice
from app.schemas.prices import PriceReadSchema

crud_price = CRUDPrice()

price_router = APIRouter(
    tags=["Prices"],
)


@price_router.get(
    "/all/{ticker}",
    response_model=list[PriceReadSchema],
    summary="Получение всех сохраненных данных по указанной валюте",
    description="""
    Возвращает все записи цен для указанного тикера.

    Параметры:
    - ticker: Название тикера (BTC_USD, ETH_USD)
    """
)
async def get_all(
    ticker: str,
    session: AsyncSession = Depends(get_session)
) -> list[PriceReadSchema]:
    prices = await crud_price.get_all(ticker, session)
    try:
        if not prices:
            raise HTTPException(status_code=404, detail="Данные не найдены")
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")


@price_router.get(
    "/latest/{ticker}",
    response_model=PriceReadSchema,
    summary="Получение последней цены валюты",
    description="""
    Возвращает последнюю запись цены для указанного тикера.

    Параметры:
    - ticker: Название тикера (BTC_USD, ETH_USD)
    """
)
async def get_latest(
    ticker: str,
    session: AsyncSession = Depends(get_session)
) -> PriceReadSchema:
    prices = await crud_price.get_latest(ticker, session)
    try:
        if not prices:
            raise HTTPException(status_code=404, detail="Данные не найдены")
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")


@price_router.get(
    "/filter_by_date/{ticker}",
    response_model=list[PriceReadSchema],
    summary="Получение цены валюты с фильтром по дате",
    description="""
    Возвращает цены для указанного тикера с фильтрацией по дате.

    Параметры:
    - ticker: Название тикера (BTC_USD, ETH_USD)
    """
)
async def get_by_date(
    ticker: str,
    start: int | None = Query(
        default=None,
        description="Начальная дата в формате timestamp"
    ),
    end: int | None = Query(
        default=None,
        description="Конечная дата в формате timestamp"
    ),
    session: AsyncSession = Depends(get_session),
) -> list[PriceReadSchema]:
    try:
        prices = await crud_price.get_by_date(ticker, start, end, session)
        if not prices:
            raise HTTPException(status_code=404, detail="Данные не найдены")
        return prices
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
