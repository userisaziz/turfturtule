# turfturtule

## Backend (FastAPI)

The backend is a Python [FastAPI](https://fastapi.tiangolo.com/) application located in `backend/`.

### Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | Web framework — routing, request validation, OpenAPI docs |
| `uvicorn[standard]` | ASGI server to run the app; `[standard]` adds `httptools`/`uvloop` for performance |
| `pydantic` | Data validation and settings via type hints (schemas, requests, responses) |
| `pydantic-settings` | Typed configuration loaded from environment variables |
| `sqlalchemy` | ORM / database layer (powers `backend/core/database.py`) |
| `asyncpg` | Async PostgreSQL driver for SQLAlchemy |
| `python-dotenv` | Load `.env` file during local development |
| `httpx` | Async HTTP client — used for tests and outbound requests |

### Requirements

- Python **3.11+**

### Installation

Dependencies are declared in `backend/pyproject.toml` (the project manifest).

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"   # editable install: project + core deps + dev tools (pytest, ruff, httpx)
```

For a production (non-editable) install, use `pip install .` instead.

### Running the server

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `/docs`.
