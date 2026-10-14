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

---

# Step 2.5 — Alembic (schema migrations)

**What**: migration tool by the SQLAlchemy author. Model changes in Python don't touch the DB —
Alembic turns model-diff into versioned `upgrade()` / `downgrade()` files. `create_all()` builds
missing tables only; it can't ALTER existing ones — real projects need migrations.

**Why we need it**: adding a column to `models/*.py` updates Python, not Postgres. Without a
migration, prod DB and code drift apart silently. Manual `ALTER TABLE` doesn't get versioned,
doesn't roll back cleanly, and doesn't reach your co-dev's machine.

**Init**: `alembic init migrations` → creates `migrations/` (`env.py`, `versions/`) + `alembic.ini`.

**Wire-up (three things Alembic needs to know)**:
- **Which DB** → `env.py` reads URL from `get_settings()`, not `alembic.ini` (keeps secrets out of git)
- **Which models** → import `Base` + every model file, else their tables are invisible to autogenerate
- **Async engine** → `async_engine_from_config(...)` + `connection.run_sync(do_run_migrations)`
  because our engine is async and Alembic's API is sync; Alembic runs the sync migration inside
  an async connection via `run_sync`

**The two commands**: `alembic revision --autogenerate -m "msg"` (writes a file, hits nothing) →
`alembic upgrade head` (applies it). Never skip *reading* the generated file — autogenerate gets
it right ~90%, but renames / type changes / index / constraint semantics are known misses.

**Rollback**: `alembic downgrade -1` runs the previous revision's `downgrade()`. Warn: any column
dropped = data lost; back up before downgrading prod.

**Inspect state**: `alembic current` (which rev DB sits at) · `alembic history` (every rev) ·
`alembic check` (dry-run diff model vs DB, no file written — proves env.py wiring).

**Workflow order** — never skip a step:
1. edit model → 2. `alembic revision --autogenerate` → 3. **read the file** →
4. `alembic upgrade head` → 5. verify in DB (Table Viewer or `SELECT FROM pg_tables`).

**Key takeaway** — models = intent, migrations = applied history. In prod you run migrations
as a deploy step, not on every app start.
