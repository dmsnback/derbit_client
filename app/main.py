import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_session
from app.core.logging import setup_logging
from app.crud.price_crud import CRUDPrice
from app.services.derbit_client import DerbitClient

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Приложение derbitclient запущено")
    yield
    logger.info("Приложение derbitclient остановлено")


app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    lifespan=lifespan,
)

crud_price = CRUDPrice()


@app.get("/debug_price")
async def debug_price(ticker: str):
    client = DerbitClient()
    price = await client.get_index_price(ticker)
    return {"ticker": ticker, "price": price}


@app.get("/all/{ticker}")
async def get_all(ticker: str, session: AsyncSession = Depends(get_session)):
    prices = await crud_price.get_all(ticker, session)
    return prices


@app.get("/latest/{ticker}")
async def get_latest(
    ticker: str, session: AsyncSession = Depends(get_session)
):
    prices = await crud_price.get_latest(ticker, session)
    return prices


@app.get("/filter_by_date/{ticker}")
async def get_by_date(
    ticker: str,
    start: int | None,
    end: int | None,
    session: AsyncSession = Depends(get_session),
):
    prices = await crud_price.get_by_date(ticker, start, end, session)
    return prices


@app.post("/test_add")
async def test_add(session: AsyncSession = Depends(get_session)):
    try:
        await crud_price.save_price(session, "BTC_EUR", 45000.0, 180)
        return {"ok": "True"}
    except Exception as e:
        raise e
