import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    try:
        print("Setting up database...")
        
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",  
            user="postgres",
            password="Vishnu_24" 
        )
        
        conn.autocommit = True 
        cursor = conn.cursor()
        
        # Create database 
        try:
            cursor.execute("CREATE DATABASE solana_mvrv")
            print("Database 'solana_mvrv' created successfully!")
        except psycopg2.errors.DuplicateDatabase:
            print("Database 'solana_mvrv' already exists!")
        
        cursor.close()
        conn.close()
        
        conn = psycopg2.connect(
            host="localhost",
            database="solana_mvrv",
            user="postgres",
            password="Vishnu_24"
        )
        
        cursor = conn.cursor()
        
        # Create hourly metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hourly_metrics (
                id SERIAL PRIMARY KEY,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                market_cap NUMERIC,
                realized_value NUMERIC,
                mvrv_ratio NUMERIC,
                circulating_supply NUMERIC,
                sol_price NUMERIC
            )
        """)
        print("Table 'hourly_metrics' created successfully!")
        
        # Create daily metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_metrics (
                id SERIAL PRIMARY KEY,
                date DATE UNIQUE,
                avg_market_cap NUMERIC,
                avg_realized_value NUMERIC,
                avg_mvrv_ratio NUMERIC,
                total_volume NUMERIC
            )
        """)
        print("Table 'daily_metrics' created successfully!")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("Please check:")
        print("1. Is PostgreSQL running?")
        print("2. Did you use the correct password?")
        print("3. Did you install PostgreSQL properly?")

if __name__ == "__main__":
    setup_database()