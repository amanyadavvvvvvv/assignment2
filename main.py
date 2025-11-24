import yfinance as yf
import pandas as pd
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def fetch_stock_data(tickers, period="5y"):
    try:
        print(f"Fetching {period} data for: {', '.join(tickers)}")
        data = yf.download(tickers, period=period, progress=False)["Close"]
        
        # Check if data is empty
        if data.empty:
            print("Error: No data retrieved. Please check ticker symbols.")
            return None
        
        # Check if we got data for all tickers
        if isinstance(data, pd.Series):
            # Only one ticker returned data
            print(f"Warning: Data available for only one ticker")
        
        print("✓ Data fetched successfully\n")
        return data
        
    except Exception as e:
        print(f"Error fetching stock data: {str(e)}")
        return None

def calculate_correlation(data, tickers):
    try:
        # Calculate correlation matrix
        corr_matrix = data.corr()
        
        # Get correlation between the two stocks
        if len(tickers) >= 2 and corr_matrix.shape[0] >= 2:
            corr_value = corr_matrix.iloc[0, 1]
        else:
            print("Warning: Cannot calculate correlation - insufficient data")
            corr_value = None
        
        return corr_matrix, corr_value
        
    except Exception as e:
        print(f"Error calculating correlation: {str(e)}")
        return None, None

def main():
    """Main execution function"""
    try:
        # List of stocks
        tickers = ["MAHSCOOTER.NS", "BAJAJHLDNG.NS"]
        
        # Fetch stock data
        data = fetch_stock_data(tickers, period="5y")
        
        if data is None:
            print("\nFailed to fetch stock data. Exiting.")
            return
        
        # Display first few rows
        print("Stock Data (Closing Prices):")
        print(data.head())
        
        # Calculate correlation
        corr_matrix, corr_value = calculate_correlation(data, tickers)
        
        if corr_matrix is None:
            print("\nFailed to calculate correlation. Exiting.")
            return
        
        # Display correlation matrix
        print("\nCorrelation Matrix:")
        print(corr_matrix)
        
        # Display correlation coefficient
        if corr_value is not None:
            print(f"\nCorrelation Coefficient between {tickers[0]} and {tickers[1]}: {corr_value:.4f}")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error in main execution: {str(e)}")

if __name__ == "__main__":
    main()