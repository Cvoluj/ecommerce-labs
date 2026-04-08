import asyncio
import contextlib
import signal
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from db import ping_db, close_db, run_migrations
from logger import get_logger

logger = get_logger(__name__)


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    run_migrations()
    logger.info("Application startup complete.")

    yield

    logger.info("Starting graceful shutdown...")
    logger.info("Closing database connections...")
    close_db()
    logger.info("Shutdown complete.")


app = FastAPI(title="E-Commerce API", lifespan=lifespan)


@app.get("/health")
def health_check():
    if ping_db():
        return {"status": "ok", "database": "connected"}
    return JSONResponse(
        status_code=503,
        content={"status": "unavailable", "database": "unreachable"},
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        timeout_graceful_shutdown=30,
        log_config=None,
    )