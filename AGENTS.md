# Agent Instructions — agent-test-project

Python FastAPI project with a calculator core and a live currency-conversion service.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run dev server (hot-reload)
uvicorn src.main:app --reload

# Run tests
pytest

# Lint / format (also runs automatically via pre-commit)
ruff check src tests --fix
ruff format src tests
```

Pre-commit hooks (`ruff` lint + format) run on every commit and **must pass**. If a commit is rejected, re-stage the auto-fixed files and commit again.

## Architecture

```
src/
  calculator.py        # Pure math functions — no I/O, no framework imports
  models.py            # Pydantic request/response models
  services/
    exchange_rate.py   # ExchangeRateService — isolates the Frankfurter API call
  main.py              # FastAPI app; routes stay thin (model → service → response)
tests/
  test_calculator.py   # pytest; use pytest-asyncio for async service tests
```

**Layer rules:**
- `calculator.py` stays framework-agnostic and pure — business logic only.
- Services isolate all external I/O so they can be injected/mocked in tests.
- `models.py` owns all Pydantic schemas; routes import from there, not inline.
- FastAPI routes map HTTP ↔ domain errors: `ZeroDivisionError` → 400, `ExchangeRateError` → 502, Pydantic validation → 422 (automatic).

## Key Conventions

- **Type hints** on all function signatures; use `Union[int, float]` (aliased as `Number`) for numeric arguments in `calculator.py`.
- **Input validation** via `_validate_numeric()` in `calculator.py`; raises `TypeError` for non-numeric args.
- **Async services**: `ExchangeRateService.get_rate()` and `.convert()` are `async`; currency codes are normalised to uppercase inside the service.
- **External API**: [Frankfurter](https://api.frankfurter.dev) — free, no API key required. Base URL is `FRANKFURTER_BASE_URL` constant in `exchange_rate.py`.
- **Commit style**: Conventional Commits — `feat:`, `fix:`, `chore:`, `test:`, etc.
- **Never commit directly to `main`** — always branch first.

## Custom Agents

| Agent file | Purpose |
|---|---|
| `.github/agents/code-implementer.agent.md` | Small, scoped code changes → branch → commit → push |
| `.github/agents/full-flow.agend.md` | Full dev loop with automatic handoff to pr-creator |
| `.github/agents/pr-creator.agend.md` | Opens a PR from the current branch into main |
| `.github/agents/pr-review-assistant.agent.md` | Pre-human code review pass |
| `.github/agents/code-finalizer.agend.md` | Runs validation, stages, and commits finished work |
