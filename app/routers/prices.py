from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.price_crud import CRUDPrice
from app.schemas.prices import PriceReadSchema

crud_price = CRUDPrice()

price_router = APIRouter(
    prefix="/prices",
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
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
) -> list[PriceReadSchema]:
    ticker = ticker.upper()
    offset = (page - 1) * size
    prices = await crud_price.get_all(ticker, size, offset, session)
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
    ticker = ticker.upper()
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
    - start: Начальная дата в формате timestamp
    - end: Конечная дата в формате timestamp
    """
)
async def get_by_date(
    ticker: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
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
        ticker = ticker.upper()
        offset = (page - 1) * size
        prices = await crud_price.get_by_date(ticker, size, offset, session, start, end)
        if not prices:
            raise HTTPException(status_code=404, detail="Данные не найдены")
        return prices
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
