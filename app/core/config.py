from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Клиент для криптобиржи Deribit"
    description: str = (
        "Клиент каждую минуту забирает с биржи текущую цену btc_usd и eth_usd (index price валюты) после чего сохраняет в базу данных тикер валюты, текущую цену и время в UNIX timestamp"
    )
    database_url: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
