# SÖYLE — Smart Communication

Backend AAC-платформы для общения с помощью визуальных карточек.
На этом этапе реализована базовая инфраструктура без бизнес-функций.
Стек: Python 3.12, FastAPI, Uvicorn, PostgreSQL 17, SQLAlchemy 2.x
(asyncpg), Alembic, Pydantic v2 и pydantic-settings, Pytest и HTTPX.

## Docker Compose

Команды для PowerShell из корня проекта:

```powershell
Copy-Item backend/.env.example backend/.env
code backend/.env
```

В `.env` замените демонстрационный `POSTGRES_PASSWORD` и пароль в
`DATABASE_URL` на одинаковый собственный пароль. Специальные символы пароля
в URL нужно кодировать в percent-encoding. Хост для Compose — `db`.
Файл `.env` исключён из Git. Не копируйте его повторно поверх своих настроек.
`CORS_ORIGINS` задаётся JSON-массивом разрешённых frontend-адресов.
Переменные окружения процесса имеют приоритет над `.env` при локальном запуске.

```powershell
docker compose up --build -d
docker compose ps
docker compose exec backend alembic upgrade head
Start-Process http://localhost:8000/docs
Invoke-RestMethod http://localhost:8000/
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/health/db
docker compose exec backend python -m pytest
```

Ожидаемые ответы: `/` → `{"message":"SÖYLE API"}`, `/health` →
`{"status":"ok"}`, `/health/db` → `{"status":"ok","database":"connected"}`.
При недоступной БД последний маршрут возвращает HTTP 503 без внутренних деталей.
`/health` не обращается к БД. Swagger UI: http://localhost:8000/docs,
OpenAPI: http://localhost:8000/openapi.json.

БД не публикует порт на хост, данные сохраняются в именованном volume.
Миграции выполняются вручную, приложение не создаёт таблицы при старте.
Смена переменных PostgreSQL не меняет учётные данные уже созданной БД в volume.

## Локальный запуск на Windows

Установите Python 3.12 и отдельный PostgreSQL 17 на `localhost:5432`.
Создайте в PostgreSQL базу и пользователя, соответствующих `.env`.
Если Compose уже работает, остановите его, чтобы освободить порт API:

```powershell
docker compose stop
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# Если .env ещё не создан:
if (!(Test-Path .env)) { Copy-Item .env.example .env }
code .env
```

В `DATABASE_URL` замените хост `db` на `localhost`, укажите данные локальной БД.
Для возврата к Compose снова используйте хост `db`. Настройки считываются из
`backend/.env`; `DATABASE_URL` обязателен. `DEBUG=false` оставляет внутренние
ошибки скрытыми, `APP_ENV` обозначает окружение.

```powershell
alembic upgrade head
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

В другом терминале PowerShell из корня проекта:

```powershell
Invoke-RestMethod http://localhost:8000/
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/health/db
cd backend
.\.venv\Scripts\python.exe -m pytest
```

Тесты подменяют сессии БД и не подключаются к PostgreSQL. Проверяют ответы
маршрутов, успешную проверку БД и ошибки подключения/таймаут без раскрытия деталей.

## Будущие миграции

Добавляйте ORM-модели на основе `app.database.Base` и импортируйте их в
`alembic/env.py`, чтобы они появились в `Base.metadata`.
Из `backend` с активным окружением:

```powershell
alembic revision --autogenerate -m "describe schema change"
alembic upgrade head
```

Начальная миграция `0001` пустая; Alembic создаёт только служебную таблицу версии.
Для Docker команды выполняются через `docker compose exec backend` из корня.
