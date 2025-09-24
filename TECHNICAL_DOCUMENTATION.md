# Solana MVRV System — Technical Documentation

Version: 1.0
Last updated: 2025-09-19

This document describes the architecture, data flow, algorithms, database schema, API surface, scheduler behavior, configuration, rationale for key design decisions, and next steps for the `solana-mvrv-system` project.

Table of contents
- Overview
- High-level architecture
- Components
  - MVRV Calculator
  - Data Fetcher (SolanaDataFetcher)
  - Database layer
  - Scheduler
  - API Server and Dashboard
- Data flow (step-by-step)
- Database schema
- Algorithms and calculations
- Configuration and environment
- Error handling and edge cases
- Rationale and design decisions
- Security considerations
- Testing and validation
- Running and deployment
- Next steps and improvements


## Overview

The `solana-mvrv-system` is a small Python-based pipeline that calculates a simplified MVRV ratio for Solana, stores hourly metrics in a PostgreSQL database, and exposes the results through a small API and a lightweight dashboard.

MVRV (Market Value to Realized Value) is calculated as market capitalization divided by realized capitalization (realized cap is simplified here). This project is intentionally minimal and contains placeholder data-fetching logic that would be replaced with real RPC and on-chain analytics in production.


## High-level architecture

The system is composed of these major parts:

- Scheduler: runs hourly (and once on start) to trigger calculation and storage.
- MVRV Calculator: computes `market_cap`, `realized_value` and `mvrv_ratio` using the Data Fetcher.
- SolanaDataFetcher: encapsulates external calls to fetch SOL price, supply and other on-chain data.
- Database: PostgreSQL tables `hourly_metrics` and `daily_metrics` persist computed metrics.
- API Server (Flask): exposes endpoints for latest and hourly historical metrics, and serves a dashboard using Chart.js.

ASCII Architecture diagram

```
+------------+      +----------------+      +-------------+      +-----------+
| Scheduler  | ---> | MVRV Calculator| ---> | Database    | <--- | API Server|
| (hourly)   |      | (calc module)  |      | (Postgres)  |      | (Flask)   |
+------------+      +----------------+      +-------------+      +-----------+
                             ^                                     |
                             |                                     v
                        +------------+                         Dashboard (Chart.js)
                        | SolanaData |                         /api/mvrv/hourly
                        | Fetcher    |                         /api/mvrv/latest
                        +------------+
```


## Components

### MVRV Calculator (`mvrv_calculator.py`)
- Responsibilities:
  - Coordinate retrieval of price and supply from `SolanaDataFetcher`.
  - Compute `market_cap = sol_price * circulating_supply`.
  - Compute `realized_value` by calling `SolanaDataFetcher.get_realized_value(market_cap)`.
  - Compute `mvrv_ratio = market_cap / realized_value` (guard against zero).
- Output: dictionary containing `market_cap`, `realized_value`, `mvrv_ratio`, `circulating_supply`, `sol_price`.

Algorithm is simplified and synchronous. Production would require batching, rate-limit handling, historical aggregation and more sophisticated realized cap logic.


### Data Fetcher (`solana.py`)
- Responsibilities (current placeholder implementation):
  - `get_sol_price()` — queries a simple HTTP endpoint and falls back to a default value.
  - `get_circulating_supply()` — returns an approximate constant (placeholder).
  - `get_realized_value(market_cap)` — returns `market_cap * 0.85` as a simplified realized cap.
- Note: This module is intentionally minimal and must be replaced with proper RPC or indexer-based logic to compute realized cap from on-chain UTXO/coin-age style metrics.


### Database Layer (`database.py`)
- Responsibilities:
  - Manage PostgreSQL connection.
  - Provide `store_hourly_data(data)` to insert a row into `hourly_metrics`.
  - Provide `get_hourly_data(hours)` to fetch last N rows ordered by time.
- Connection configuration uses environment variables: `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS` (defaults included for dev).
- Error handling: prints errors, rolls back on insert failure and ensures cursors are closed.


### Scheduler (`scheduler.py`)
- Uses Python `schedule` package to run `hourly_job()` immediately and every hour.
- `hourly_job()` orchestrates: instantiate calculator, instantiate DB connection, calculate, store, log, close DB.

Notes:
- Scheduler runs in the foreground; for production, run as a systemd/WIndows service or run under a process manager (supervisor, PM2, etc.).


### API Server and Dashboard (`api_server.py`)
- Flask-based API exposing:
  - `GET /api/mvrv/latest` — returns the most recent row.
  - `GET /api/mvrv/hourly` — returns the most recent 24 hourly rows.
  - `GET /dashboard` — serves a small HTML page using Chart.js to render the MVRV ratio for the last 24 rows.

- The API maps DB row indices to JSON fields carefully (table columns are `id(0), time(1), market_cap(2), realized_value(3), mvrv_ratio(4), circulating_supply(5), sol_price(6)`).


## Data flow (step-by-step)
1. Scheduler or manual run triggers the calculation.
2. `MVRVCalculator` requests `sol_price`, `circulating_supply` via `SolanaDataFetcher`.
3. `MVRVCalculator` computes `market_cap`, `realized_value`, and `mvrv_ratio`.
4. `Database.store_hourly_data()` inserts a new row into `hourly_metrics` with the computed values and timestamp.
5. API reads rows and returns JSON for clients/dashboard.
6. Dashboard fetches `/api/mvrv/hourly` and displays the `mvrv_ratio` series (Chart.js).


## Database schema

`hourly_metrics` (created in `database_setup.py`):
- `id` SERIAL PRIMARY KEY
- `time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `market_cap` NUMERIC
- `realized_value` NUMERIC
- `mvrv_ratio` NUMERIC
- `circulating_supply` NUMERIC
- `sol_price` NUMERIC

`daily_metrics` (skeleton):
- `id` SERIAL PRIMARY KEY
- `date` DATE UNIQUE
- `avg_market_cap` NUMERIC
- `avg_realized_value` NUMERIC
- `avg_mvrv_ratio` NUMERIC
- `total_volume` NUMERIC

Notes:
- `NUMERIC` used for financial precision. For performance, consider `DOUBLE PRECISION` if approximate floats are acceptable.


## Algorithms and calculations
- Market cap: `market_cap = sol_price * circulating_supply`.
- Realized value (placeholder): `realized_value = market_cap * 0.85`.
- MVRV ratio: `mvrv_ratio = market_cap / realized_value if realized_value > 0 else 0`.

Rationale: these are simplified placeholders so the system's pipeline, persistence, and serving logic can be validated. Real realized-cap computations require analysis of historical on-chain coin movement and UTXO-like cost-basis aggregation.


## Configuration and environment
- Environment variables (via `.env` / `Dev.env`):
  - `DB_HOST` (default `localhost`)
  - `DB_NAME` (default `solana_mvrv`)
  - `DB_USER` (default `postgres`)
  - `DB_PASS` (default `Vishnu_24` in repo — change this!)
- Python dependencies listed in `requirements.txt` (include Flask, psycopg2-binary, python-dotenv, requests, schedule, fastapi, uvicorn, etc.)


## Error handling and edge cases
- DB unavailable: `Database` prints connection error and methods return failure or empty list. The scheduler logs errors but continues.
- Missing or malformed API responses: `SolanaDataFetcher.get_sol_price()` returns a fallback price on exception.
- Division by zero for realized value: `mvrv_ratio` guarded to be 0 when `realized_value` is zero.
- Cursor and connection cleanup: `finally` clauses ensure cursors are closed and connections closed via `Database.close()`.


## Rationale and design decisions
- Simplicity first: The project is intentionally minimal to focus on demonstrating the pipeline rather than precise on-chain analytics.
- Modularity: Calculator, data fetcher, DB layer, scheduler and API are clearly separated to make replacements (e.g., proper data fetcher) straightforward.
- Environment configuration: Use `.env` for credentials to avoid hardcoding secrets in codebase.
- Use Postgres: durable store for time-series metrics; schema allows easy aggregation to daily metrics.
- Dashboard: lightweight HTML + Chart.js served from Flask for quick visualization without heavy frontend stack.


## Security considerations
- Do not commit real DB passwords to source control; replace `DB_PASS` default and use `.env` or secrets manager.
- Limit database user permissions to only what's necessary (avoid superuser in prod).
- If exposing the dashboard publicly, add authentication and HTTPS.


## Testing and validation
- Unit tests: none shipped; add tests for `MVRVCalculator` (happy path and edge cases), `database` methods (with a test DB), and API endpoints (integration tests using test client).
- Local validations performed: `run_once.py` verifies that calculated data can be stored in DB.


## Running and deployment
- Local dev: use `venv`, `pip install -r requirements.txt`, run `database_setup.py`, run `run_once.py` to verify, run `api_server.py` and `scheduler.py` as needed.
- Production: run scheduler under a process manager (systemd, Windows service, or Docker + cron-like runner). Run API server under a WSGI server (Gunicorn, uvicorn for FastAPI) behind a reverse proxy.


## Next steps and improvements
- Replace placeholder `SolanaDataFetcher` with a proper RPC/indexer-based data source (e.g., use Solana RPC + a historical indexer for realized cap calculation).
- Compute realized cap precisely using transaction history and coin cost basis, or outsource to an indexer that provides realized cap/time-series.
- Add tests and CI for linting, unit tests and integration tests.
- Improve dashboard: add multi-series, date range selection, caching, and paginated API.
- Consider moving to a time-series DB (TimescaleDB) for better performance and analytic queries.
- Add monitoring and metrics (Prometheus) to observe scheduler and API health.
