import schedule
import time
from mvrv_calculator import MVRVCalculator
from database import Database

def hourly_job():
    print("Running hourly MVRV calculation...")
    
    calculator = MVRVCalculator()
    db = Database()
    
    try:
        # Calculate MVRV
        data = calculator.calculate_mvrv()
        
        # Store in database
        db.store_hourly_data(data)
        
        print(f"Stored data: {data}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

def main():
    # Run immediately
    hourly_job()
    
    # Schedule hourly runs
    schedule.every().hour.do(hourly_job)
    
    print("MVRV scheduler started. Press Ctrl+C to stop.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()