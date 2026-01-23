all: build run-services migrate up

build:
	@echo "Сборка образов..."
	docker-compose build  

run-services:
	@echo "Запуск сервисов..."
	docker-compose up -d db redis backend

migrate:
	@echo "Применение миграций..."
	docker-compose exec backend alembic upgrade head

up:
	@echo "Запуск всех сервисов..."
	docker-compose up -d