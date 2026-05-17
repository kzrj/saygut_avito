# MicroAvito

Маркетплейс на внутренних монетах: FastAPI (DDD) + MongoDB + React + Zustand.

## Запуск

```bash
cp .env.example .env
docker compose up --build
```

- Web: http://localhost:8081
- API health: http://localhost:8081/api/health

## Dev-режим фронта (HMR)

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up backend mongodb frontend-dev
```

Фронт: http://localhost:5173 (прокси `/api` → backend)

## MVP-сценарий

1. Регистрация → кошелёк → dev-начисление монет
2. Создать и опубликовать объявление (списание listing fee)
3. Каталог → карточка объявления
4. Пополнение через mock ЮMoney
5. Реферальная ссылка `/register?ref=CODE` → бонус после первой публикации реферала

## Структура

- `backend/app/domain` — сущности и порты
- `backend/app/application` — use cases
- `backend/app/infrastructure` — MongoDB, JWT, платежи
- `backend/app/presentation/api/v1` — REST
- `frontend/src/api` — HTTP-слой
- `frontend/src/store` — Zustand
