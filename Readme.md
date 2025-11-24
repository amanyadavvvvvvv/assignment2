# Stock Correlation Analysis Script README

## Overview
This Python script analyzes the historical correlation between two stocks—Maharashtra Scooters Limited (MAHSCOOTER.NS) and Bajaj Holdings & Investment Limited (BAJAJHLDNG.NS)—using Yahoo Finance data from the past five years.

It automatically:  
- Fetches daily closing price data for the specified stocks using the `yfinance` package.  
- Calculates and displays their correlation matrix and coefficient.

## Prerequisites
- Python 3.8+
- `yfinance` library
- `pandas` library

Install dependencies if necessary:
```bash
pip install yfinance pandas
```

## How to Use
1. Clone or download the script to your local machine.
2. Open a terminal, navigate to the script directory.
3. Run the script with:
```bash
python main.py
```
4. The script will fetch 5-year closing price data for the two stocks and display:
   - First few rows of fetched data
   - Correlation matrix
   - Correlation coefficient between Maharashtra Scooters and Bajaj Holdings

## Script Details
- **fetch_stock_data(tickers, period)**:  Collects closing price data from Yahoo Finance. Handles error cases where data is not found for the provided tickers.
- **calculate_correlation(data, tickers)**:  Calculates the correlation matrix and extracts the correlation coefficient between the two provided tickers.
- **main()**:  Coordinates data fetching and analysis, prints output.

## Customization
- To analyze different stocks, change the ticker symbols in the `tickers` list.
- The `period` parameter can be adjusted (e.g., '1y', '6mo', 'max') for different timeframes.

## Notes
- If no data is retrieved, ensure the ticker symbols are correct and supported by Yahoo Finance.
- For more than two stocks, the script will compute pairwise correlations.

## Error Handling
The script provides informative error and warning messages for:
- Invalid/unsupported ticker symbols.
- Empty data returns.
- Calculation errors due to insufficient data.

## License
This script is provided for educational and analytical use. Modify as needed for your environment or research.