<a name="Начало"></a>

## Derbit Client

Клиент для криптобиржи Deribit

[![Derbit Client Lint annd Tests](https://img.shields.io/github/actions/workflow/status/dmsnback/derbit_client/main.yml?branch=main&style=flat-square&label=Derbit_Client%20Lint)](https://github.com/dmsnback/derbit_client/actions/workflows/main.yml)
[![Derbit Client Docker Dev](https://img.shields.io/github/actions/workflow/status/dmsnback/derbit_client/main.yml?branch=dev&style=flat-square&label=Derbit_Client%20Docker%20Dev)](https://github.com/dmsnback/derbit_client/actions/workflows/main.yml)
[![Derbit Client Docker Prod](https://img.shields.io/github/actions/workflow/status/dmsnback/derbit_client/main.yml?branch=main&style=flat-square&label=Derbit_Client%20Docker%20Prod)](https://github.com/dmsnback/derbit_client/actions/workflows/main.yml)


- [Описание](#Описание)
- [Технологии](#Технологии)
- [Тестирование](#Тестирование)
- [Таблица эндпоинтов](#Таблица)
- [Шаблон заполнения .env-файла](#Шаблон)
- [Запуск проекта на локальной машине](#Запуск)
- [Автор](#Автор)

<a name="Описание"></a>

### Описание

Асинхронный клиент для криптобиржи Deribit.
Сервис периодически получает ```index price``` BTC_USD и ETH_USD,
сохраняет данные в базу тикер валюты, текущую цену и время в ```UNIX timestamp```.

Приложение написано с использованием **асинхронного FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Celery** и **Redis**.

В проекте настроен **CI/CD pipeline** с использованием **GitHub Actions**:

```md
- Автоматическая проверка кода (black, isort, flake8)
- Запуск unit-тестов (`pytest`)
- Сборка Docker-образа
- Публикация образа в **Docker Hub** при пуше в соответствующие ветки
```

```md
Проект адаптирован для использования **PostgreSQL** и развёртывания в контейнерах **Docker**.
```

> [Вернуться в начало](#Начало)

<a name="Технологии"></a>

### Технологии

[![Python](https://img.shields.io/badge/Python-1000?style=for-the-badge&logo=python&logoColor=ffffff&labelColor=000000&color=000000)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-1000?style=for-the-badge&logo=fastapi&logoColor=ffffff&labelColor=000000&color=000000)](https://fastapi.tiangolo.com)
[![Celery](https://img.shields.io/badge/Celery-1000?style=for-the-badge&logo=celery&logoColor=ffffff&labelColor=000000&color=000000)](https://docs.celeryq.dev/en/stable/index.html)
[![Redis](https://img.shields.io/badge/Redis-1000?style=for-the-badge&logo=redis&logoColor=ffffff&labelColor=000000&color=000000)](https://redis-docs.ru)
[![aiohttp](https://img.shields.io/badge/aiohttp-1000?style=for-the-badge&logo=aiohttp&logoColor=ffffff&labelColor=000000&color=000000)](https://github.com/aio-libs/aiohttp?ysclid=mkqid6e88x702921033)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1000?style=for-the-badge&logo=sqlalchemy&logoColor=ffffff&labelColor=000000&color=000000)](https://www.sqlalchemy.org)
[![Pydantic](https://img.shields.io/badge/Pydantic_V2-1000?style=for-the-badge&logo=Pydantic&logoColor=ffffff&labelColor=000000&color=000000)](https://docs.pydantic.dev/latest/)
[![Docker](https://img.shields.io/badge/Docker-1000?style=for-the-badge&logo=docker&logoColor=ffffff&labelColor=000000&color=000000)](https://www.docker.com)
[![Postgres](https://img.shields.io/badge/Postgres-1000?style=for-the-badge&logo=postgresql&logoColor=ffffff&labelColor=000000&color=000000)](https://www.postgresql.org)
[![Pytest](https://img.shields.io/badge/Pytest-1000?style=for-the-badge&logo=pytest&logoColor=ffffff&labelColor=000000&color=000000)](https://docs.pytest.org/en/stable/index.htmlc)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=ffffff&labelColor=000000&color=000000)](https://github.com/features/actions)

> [Вернуться в начало](#Начало)

<a name="Тестирование"></a>

### Тестирование

В проекте реализованы **unit-тесты** с использованием `pytest` и `pytest-asyncio`.

- Тестируется CRUD-логика работы с ценами
- Асинхронные операции с базой данных
- Для тестов используется изолированная база данных (SQLite)

Запуск тестов локально:

```python
pytest -v
```

> [Вернуться в начало](#Начало)

<a name="Таблица"></a>

### Таблица эндпоинтов

**Prices**

|Метод|URL|Описание|
|:-:|:-:|:-:|
|GET|/all/{ticker}|Получение всех сохраненных данных по указанной валюте|
|GET|/latest/{ticker}|Получение последней цены валюты|
|GET|/filter_by_date/{ticker}|Получение цены валюты с фильтром по дате|

> [Вернуться в начало](#Начало)

<a name="Шаблон"></a>

### Шаблон заполнения .env-файла

> `env.example` с дефолтнными значениями расположен в корневой папке

```python
POSTGRES_DB = derbit_db # Имя базы дданнных
POSTGRES_USER = postgres # Имя юзера PostgreSQL
POSTGRES_PASSWORD = yourpassword # Пароль юзера PostgreSQL
DATABASE_URL = postgresql+asyncpg://postgres:yourpassword@db:5432/derbit_db  # Указываем адрес БД
```

> [Вернуться в начало](#Начало)

<a name="Запуск"></a>

### Запуск проекта на локальной машине

- Склонируйте репозиторий

```python
git clone git@github.com:dmsnback/derbit_client.git
```

- Запускаем проект в **Docker**

```python
make all
```

- Документация к API станет доступна по адресу:

[http://localhost:8000/docs/](http://localhost:8000/docs/)

> [Вернуться в начало](#Начало)

<a name="Автор"></a>

### Автор

- [Титенков Дмитрий](https://github.com/dmsnback)

> [Вернуться в начало](#Начало)
