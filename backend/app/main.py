import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.database import engine, get_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="AAC communication platform backend",
    debug=settings.DEBUG,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": settings.APP_NAME}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db", responses={503: {"description": "Database unavailable"}})
async def database_health(db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        async with asyncio.timeout(5):
            await db.execute(text("SELECT 1"))
    except Exception:
        # Driver errors vary; never expose connection details to the client.
        return JSONResponse(
            status_code=503,
            content={"status": "error", "database": "unavailable",
                     "message": "Database is temporarily unavailable"},
        )
    return {"status": "ok", "database": "connected"}
