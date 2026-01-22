import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.crud.price_crud import CRUDPrice
from app.models.prices import Base

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

crud_price = CRUDPrice()


@pytest.fixture
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session_local:
        yield session_local

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_save_price(session):
    """Тест сохранения в БД"""
    price = await crud_price.save_price(
        session, ticker="BTC_USD", price=5000.00, timestamp=100
    )
    assert price.ticker == "BTC_USD"
    assert price.price == 5000.00
    assert price.timestamp == 100


@pytest.mark.asyncio
async def test_get_all(session):
    """Тест получеения всех записей и работы пагинации"""
    for i in range(5):
        await crud_price.save_price(
            session, ticker="BTC_USD", price=5000.00 + i, timestamp=100 + i
        )

    prices = await crud_price.get_all(
        "BTC_USD", session=session, size=3, offset=0
    )
    assert len(prices) == 3


@pytest.mark.asyncio
async def test_get_latest(session):
    """Тест получения последней цены."""
    await crud_price.save_price(
        session, ticker="BTC_USD", price=6000.00, timestamp=500
    )
    latest_price = await crud_price.get_latest("BTC_USD", session=session)
    assert latest_price.ticker == "BTC_USD"
    assert latest_price.price == 6000.00
    assert latest_price.timestamp == 500


@pytest.mark.asyncio
async def test_get_by_date(session):
    """Тест получения цены с фильтрацией по дате, ValueError когда start > end"""
    await crud_price.save_price(
        session, ticker="BTC_USD", price=6000.00, timestamp=700
    )
    await crud_price.save_price(
        session, ticker="BTC_USD", price=5000.00, timestamp=800
    )
    await crud_price.save_price(
        session, ticker="BTC_USD", price=4000.00, timestamp=900
    )

    prices = await crud_price.get_by_date(
        "BTC_USD", size=3, offset=0, start=750, end=900, session=session
    )
    assert len(prices) == 2

    for price in prices:
        assert 750 <= price.timestamp <= 900

    with pytest.raises(ValueError):
        await crud_price.get_by_date(
            "BTC_USD", size=3, offset=0, start=900, end=750, session=session
        )
