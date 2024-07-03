import finnhub
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')
finnhub_client = finnhub.Client(api_key=api_key)


def test_finnhub_api(symbol):
    quote_data = finnhub_client.quote(symbol)
    financials_data = finnhub_client.company_basic_financials(symbol, 'all')
    
    # Convert JSON responses to DataFrames
    df_quote = pd.DataFrame([quote_data])
    df_financials = pd.DataFrame(financials_data['metric'].items(), columns=['Metric', 'Value'])
    df_financials.insert(0, 'Symbol', symbol)
    
    # Write to file
    with open('test_results.txt', 'a') as f:
        f.write(f"Symbol: {symbol}\n\n")
        
        f.write("Real-time Quote Data:\n")
        f.write(df_quote.to_string(index=False) + "\n\n")
        
        f.write(f"{symbol} Basic Financials:\n")
        f.write(df_financials.to_string(index=False, header=True) + "\n\n")

if __name__ == "__main__":
    test_finnhub_api(symbol='AAPL')