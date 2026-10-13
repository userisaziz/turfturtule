"""Turfturtule backend — FastAPI application entrypoint."""

from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_settings
from core.database import get_db

def create_app()-> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Turfturtule API",
        version="0.1.0",
    )
    
    
    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok", "env": settings.env}
    @app.get("/db-check")
    async def db_check(db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
        result = await db.execute(text("SELECT version()"))
        return {"db": result.scalar().split()[0]}
    
    return app
    


app = create_app()
