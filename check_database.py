import psycopg2

def check_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="Vishnu_24"
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT datname FROM pg_database WHERE datname = 'solana_mvrv'")
        result = cursor.fetchone()
        
        if result:
            print("✅ Database 'solana_mvrv' exists!")
        else:
            print("❌ Database 'solana_mvrv' does NOT exist!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

check_database()