# Solana MVRV System

This small project calculates a simplified MVRV ratio for Solana and stores hourly metrics in Postgres, and serves a simple dashboard.

Prereqs
- Python 3.10+ (project was tested on 3.11)
- PostgreSQL running locally

Quick start
1. Create a virtual environment and install deps:

```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure DB credentials (recommended: create a `.env` or edit `Dev.env`):

```
DB_HOST=localhost
DB_NAME=solana_mvrv
DB_USER=postgres
DB_PASS=YourPostgresPassword
```

3. Create database and tables:

```powershell
python database_setup.py
```

4. Run the scheduler (it will run once immediately and then every hour):

```powershell
python scheduler.py
```

5. Start the API server and open the dashboard:

```powershell
python api_server.py
# then open http://localhost:5000/dashboard
```

Troubleshooting
- If no data appears: ensure `scheduler.py` ran successfully and you see `Data stored successfully!` in its output. Check Postgres connection and credentials.
- Check `Dev.env` for sample env variables.

Next steps
- Replace simplified solana data fetchers with real RPC calls.
- Add authentication and pagination to API.
- Add unit tests and CI.
