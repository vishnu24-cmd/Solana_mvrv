from fastapi import FastAPI
import psycopg2
from datetime import datetime, timedelta

app = FastAPI()

def get_db_connection():
    return psycopg2.connect("dbname=your_db user=your_user password=Vishnu_24")

@app.get("/mvrv/{period}")
def get_mvrv(period: str): # e.g., period = "daily" or "hourly"
    conn = get_db_connection()
    cur = conn.cursor()
    # Query the last 7 days of data for the requested period
    query = "SELECT timestamp, market_cap_usd, realized_cap_usd, mvrv_ratio FROM mvrv_ratio WHERE calculation_type = %s AND timestamp > %s ORDER BY timestamp;"
    cur.execute(query, (period, datetime.now() - timedelta(days=7)))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": data}