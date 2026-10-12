"""Turfturtule backend — FastAPI application entrypoint."""

from fastapi import FastAPI

from core.config import settings

app = FastAPI(
    title="Turfturtule API",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict:
    """Liveness check — used by load balancers, monitors, and to verify local setup."""
    return {"status": "ok", "env": settings.env}
