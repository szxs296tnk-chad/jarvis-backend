from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import Config
from core.brain.orchestrator import Orchestrator
from api.routes import router, init_routes
from api.websocket import ws_router
from infrastructure.logger import setup_logger
from infrastructure.monitor import SystemMonitor

setup_logger()
logger = logging.getLogger("chad.main")

config = Config.load()
orchestrator = Orchestrator(config)
monitor = SystemMonitor()
history: list[dict] = []

init_routes(orchestrator, monitor, config.api_key, history)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("CHAD starting...")
    await orchestrator.initialize()
    logger.info("CHAD ready")
    yield
    logger.info("CHAD shutting down")


app = FastAPI(title="CHAD Backend", version="3.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(ws_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"response": "Error interno del sistema"},
    )
