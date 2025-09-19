# Requirements Compliance Table

This document maps project requirements to implementation components, files, and current status. It helps track what is implemented, where it lives, and any known gaps.

Format: Requirement | Implementing Component / File(s) | Status | Notes

---

Requirement: Calculate MVRV (market cap, realized value, MVRV ratio)
- Implementing Component / File(s): `mvrv_calculator.py`, `solana.py`
- Status: Implemented
- Notes: `MVRVCalculator.calculate_mvrv()` computes `market_cap` (price * circulating supply), `realized_value` (placeholder 85% of market cap), and `mvrv_ratio` with division-by-zero guard.

Requirement: Persist hourly metrics to a database
- Implementing Component / File(s): `database.py`, `database_setup.py`, `run_once.py`, `scheduler.py`
- Status: Implemented
- Notes: `database.py` provides `store_hourly_data()` and `get_hourly_data()`; `database_setup.py` creates `hourly_metrics` and `daily_metrics` tables. `run_once.py` verifies insertion; `scheduler.py` schedules hourly insertion.

Requirement: Serve data via an API
- Implementing Component / File(s): `api_server.py`, `api.py` (sample)
- Status: Implemented (Flask server)
- Notes: Flask server exposes `GET /api/mvrv/latest` and `GET /api/mvrv/hourly`. A FastAPI sample exists in `api.py` but is not the primary server.

Requirement: Provide a dashboard visualization
- Implementing Component / File(s): `api_server.py` (dashboard route), Chart.js (client-side CDN)
- Status: Implemented (basic)
- Notes: `/dashboard` fetches `/api/mvrv/hourly` and plots the MVRV ratio for the last 24 points. Can be extended to support additional series and interactions.

Requirement: Configurable DB credentials and environment-aware config
- Implementing Component / File(s): `database.py`, `.env` support (via `python-dotenv`), `Dev.env` sample
- Status: Implemented (defaults + env overrides)
- Notes: `database.py` reads `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS` from environment. Replace defaults in production.

Requirement: Robust error handling for DB and external calls
- Implementing Component / File(s): `database.py`, `solana.py`, `scheduler.py`
- Status: Partially implemented
- Notes: `database.py` handles exceptions, rollbacks and cursor cleanup. `solana.py` returns fallback price on errors. Improve logging and add retry/backoff for network/DB failures.

Requirement: One-shot runner to validate pipeline
- Implementing Component / File(s): `run_once.py`
- Status: Implemented
- Notes: Calculates and attempts to store one row; prints results.

Requirement: Deployment/run instructions
- Implementing Component / File(s): `README.md`, `database_setup.py`
- Status: Implemented
- Notes: README includes venv setup, DB setup, running scheduler and API server.

Requirement: Tests (unit / integration)
- Implementing Component / File(s): None currently
- Status: Not implemented
- Notes: Recommend adding unit tests for `MVRVCalculator` and integration tests for DB/API.

Requirement: Secure handling of secrets
- Implementing Component / File(s): `.env` support, README guidance
- Status: Partially implemented
- Notes: `.env` supported; repo still contains default placeholder password — remove before publishing.

Requirement: Use a single consistent API framework
- Implementing Component / File(s): `api_server.py` (Flask) and `api.py` (FastAPI sample)
- Status: Multiple frameworks present
- Notes: Choose one (Flask or FastAPI) and remove the other to reduce confusion.

---

Summary status: Core functionality implemented (calculation, storage, serving, dashboard). Short-term improvements: add tests, improve error handling/retries, finalize secrets handling, and pick a single API framework. Longer-term improvements include accurate realized-cap computation and improved visualizations.
