import yfinance as yf
import sqlite3
import logging
import os

# Configure logging to track successes and failures
logging.basicConfig(
    filename='logs/api_calls.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_and_store_stock(ticker):
    """
    Fetches historical data from Yahoo Finance and stores it in a SQLite database.
    """
    try:
        print(f"Attempting to fetch data for: {ticker}...")
        df = yf.download(ticker, period="1mo", interval="1d")
        
        if df.empty:
            logging.warning(f"No data found for ticker: {ticker}")
            print(f"⚠️ No data found for {ticker}.")
            return

        # Connect to SQLite database
        # Path matches your professional structure
        db_path = os.path.join("data", "raw", "finanzas.db")
        conn = sqlite3.connect(db_path)
        
        # Save data to SQL
        table_name = f"raw_{ticker.lower()}"
        df.to_sql(table_name, conn, if_exists="replace")
        conn.close()
        
        logging.info(f"Successfully stored {ticker} data in {table_name}")
        print(f"✅ Success! {ticker} data is now in the database.")

    except Exception as e:
        logging.error(f"Failed to process {ticker}: {str(e)}")
        print(f"❌ An error occurred. Check the logs for details.")

if __name__ == "__main__":
    fetch_and_store_stock("TSLA")