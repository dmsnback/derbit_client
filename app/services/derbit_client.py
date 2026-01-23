import aiohttp


class DerbitClient:
    BASE_URL = "https://test.deribit.com/api/v2/public"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_index_price(self, ticker: str) -> float:
        """Получает index price для указаного тикера (btc_usd или eth_usd)"""
        url = f"{self.BASE_URL}/get_index_price"
        params = {"index_name": ticker.lower()}
        async with self.session.get(url=url, params=params) as response:
            data = await response.json()
            return data["result"]["index_price"]

    async def close(self):
        await self.session.close()
