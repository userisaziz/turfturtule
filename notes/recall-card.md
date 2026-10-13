# Step 1 — Short Notes

**config.py** → created `Settings` class inheriting `BaseSettings`, with
`model_config = SettingsConfigDict(env_file=".env", extra="ignore", hide_input_in_errors=True)`.
Fields: `env`, `debug=False`, `database_url: SecretStr` (no default = required, fails at startup).
`get_settings()` wrapped in `@lru_cache` → config built once, cached.

**database.py** → 2 main objects + 1 dependency:
- `engine = create_async_engine(settings.database_url.get_secret_value(), pool_pre_ping=True, echo=settings.debug)` — the connection pool; URL must carry `+asyncpg`
- `SessionLocal = async_sessionmaker(engine, expire_on_commit=False)` — session factory
- `async def get_db() -> AsyncGenerator[AsyncSession, None]` — FastAPI dependency: `yield` the session, `commit()` after, `rollback()+raise` on `BaseException`
- `class Base(DeclarativeBase)` — parent of all future models (Alembic reads `Base.metadata`)

**main.py** → app factory: `def create_app() -> FastAPI:` builds `app = FastAPI(...)`,
routes defined inside it (can use `settings`), module ends with `app = create_app()` for uvicorn.
Routes added: `/health` (returns `settings.env`, no DB) and `/db-check`
(`db: Annotated[AsyncSession, Depends(get_db)]` → `await db.execute(text("SELECT version()"))`).

**Connectivity check ladder** (bottom-up, each rung names its own culprit):
1. `lsof -i :5432` — is a server listening at all → else `Connection refused`
2. role/password/db-name — Postgres validates in order: server → role → password → database;
   the error text IS the diagnosis (`role does not exist` / `password authentication failed` / `database does not exist`)
3. engine connect + `SELECT 1` through our own stack — proves .env → SecretStr → asyncpg → greenlet chain
4. `curl /db-check` — proves get_db + Depends choreography inside the running app
