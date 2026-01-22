import asyncio
import logging
import time

import aiohttp

from app.celery_app import app
from app.core.session import get_session
from app.crud.price_crud import CRUDPrice
from app.services.derbit_client import DerbitClient

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def fetch_prices():
    asyncio.get_event_loop().run_until_complete(run())


async def run():
    async with aiohttp.ClientSession() as http_session:
        crud_price = CRUDPrice()
        client = DerbitClient(http_session)

        async for db_session in get_session():
            for ticker in ["btc_usd", "eth_usd"]:
                try:
                    price = await client.get_index_price(ticker)

                    await crud_price.save_price(
                        ticker=ticker.upper(),
                        price=price,
                        timestamp=int(time.time()),
                        session=db_session,
                    )
                    logger.info(
                        f"Получение данных по валюте: {ticker.upper()}"
                    )
                except Exception as e:
                    logger.error(
                        f"Ошибка получения данных по валюте {ticker.upper()}: {e}"
                    )
