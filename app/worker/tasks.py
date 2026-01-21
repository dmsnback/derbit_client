import asyncio
import logging
import time
from contextlib import asynccontextmanager

import aiohttp

from app.celery_app import app
from app.core.database import get_session
from app.crud.price_crud import CRUDPrice
from app.services.derbit_client import DerbitClient

logger = logging.getLogger(__name__)


@asynccontextmanager
async def get_db_session():
    async for session in get_session():
        yield session


@app.task
def fetch_prices():
    asyncio.run(run())


async def run():

    async with aiohttp.ClientSession() as http_session:
        crud_price = CRUDPrice()
        client = DerbitClient(http_session)

        async with get_db_session() as db_session:
            for ticker in ["btc_usd", "eth_usd"]:
                try:
                    price = await client.get_index_price(ticker)

                    await crud_price.save_price(
                        ticker=ticker.upper(),
                        price=price,
                        timestamp=int(time.time()),
                        session=db_session,
                    )
                    logger.info(f"Получение данных по валюте: {ticker.upper()}")
                except Exception as e:
                    logger.error(
                        f"Ошибка получения данных по валюте {ticker.upper()}: {e}"
                    )
