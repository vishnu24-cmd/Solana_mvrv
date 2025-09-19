import psycopg2

def check_tables():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="solana_mvrv",
            user="postgres",
            password="Vishnu_24"
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cursor.fetchall()
        
        if tables:
            print("✅ Tables found:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("❌ No tables found in the database!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

check_tables()