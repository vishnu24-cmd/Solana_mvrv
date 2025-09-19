import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "solana_mvrv")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "Vishnu_24")


class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            print("Database connected successfully!")
        except Exception as e:
            print(f"Database connection error: {e}")
            self.conn = None

    def store_hourly_data(self, data):
        if not self.conn:
            print("No database connection")
            return False

        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO hourly_metrics 
                (market_cap, realized_value, mvrv_ratio, circulating_supply, sol_price)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    data.get('market_cap'),
                    data.get('realized_value'),
                    data.get('mvrv_ratio'),
                    data.get('circulating_supply'),
                    data.get('sol_price')
                ),
            )
            self.conn.commit()
            print("Data stored successfully!")
            return True
        except Exception as e:
            print(f"Error storing data: {e}")
            try:
                if self.conn:
                    self.conn.rollback()
            except:
                pass
            return False
        finally:
            if cursor:
                cursor.close()

    def get_hourly_data(self, hours=24):
        if not self.conn:
            return []

        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM hourly_metrics ORDER BY time DESC LIMIT %s", (hours,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")