import logging

from sqlalchemy import desc, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prices import Price

logger = logging.getLogger(__name__)


class CRUDPrice:
    async def save_price(
        self, session: AsyncSession, ticker: str, price: float, timestamp: int
    ):
        try:
            new_price = session.add(
                Price(ticker=ticker, price=price, timestamp=timestamp)
            )
            await session.flush()
            await session.commit()
            logger.info(f"Получение данных по валюте {ticker}")
            return new_price
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении данных по валюте {ticker}: {e}")
            raise

    async def get_all(self, ticker: str, session: AsyncSession):
        try:
            query = select(Price).where(Price.ticker == ticker)
            result = await session.execute(query)
            prices = result.scalars().all()
            logger.info(f"Получение всех сохраненных данных по валюте: {ticker}")
            return prices
        except SQLAlchemyError as e:
            logger.error(
                f"Ошибка при получении всех сохраненных данных по валюте {ticker}: {e}"
            )
            raise

    async def get_latest(sellf, ticker: str, session: AsyncSession):
        try:
            query = (
                select(Price)
                .where(Price.ticker == ticker)
                .order_by(desc(Price.timestamp))
                .limit(1)
            )
            result = await session.execute(query)
            price = result.scalar_one_or_none()
            logger.info(f"Получение последней цены валюты: {ticker}")
            return price
        except SQLAlchemyError as e:
            logger.error(f"Ошибка получении последней цены валюты {ticker}: {e}")
            raise

    async def get_by_date(
        self, ticker: str, start: int | None, end: int | None, session: AsyncSession
    ):
        try:
            query = select(Price).where(Price.ticker == ticker)
            if start:
                query = query.where(Price.timestamp >= start)
            if end:
                query = query.where(Price.timestamp <= start)
            result = await session.execute(query)
            prices = result.scalars().all()
            logger.info(f"Получение цены валюты {ticker} с фильтром по дате")
            return prices
        except SQLAlchemyError as e:
            logger.error(
                f"Ошибка при получении цены валюты {ticker} с фильтром по дате: {e}"
            )
            raise
