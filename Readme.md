# Stock Correlation Analysis Tool

## What It Does
This Python script analyzes the relationship between two stocks (Maharashtra Scooters and Bajaj Holdings) over the past 5 years. It pulls historical data, crunches the numbers, and generates detailed reports with charts.

The script automatically:

- Downloads 5 years of closing price data from Yahoo Finance

- Calculates correlation between the stocks

- Computes key statistics (mean, median, std deviation, min/max, current price)

- Exports everything to Excel with multiple sheets

- Creates 6 different visualization charts

- Saves all outputs with timestamps

## Requirements
- Python 3.8 or higher

- Required packages:

```bash

pip install yfinance pandas matplotlib seaborn openpyxl

```

## How to Run

1. Save the script as `main.py`

2. Open terminal and navigate to the script folder

3. Run:

```bash

python main.py

```

4. Check your folder for:

   - Excel file: `stock_analysis_YYYYMMDD_HHMMSS.xlsx`

   - Graph file: `stock_analysis_graphs_YYYYMMDD_HHMMSS.png`

## What You Get

### Excel File (4 Sheets)

1. **Stock Prices** - Daily closing prices for both stocks

2. **Correlation Matrix** - Shows how stocks move together

3. **Statistics** - Mean, median, std dev, min, max, current price

4. **Summary** - Data points, date range for analysis

### Graphs (6 Charts)

1. **Stock Prices Over Time** - Price movement comparison

2. **Normalized Performance** - Relative performance starting at base 100

3. **Correlation Heatmap** - Visual correlation strength

4. **Daily Returns Distribution** - Return frequency histograms

5. **Price Relationship Scatter** - Direct price comparison with correlation value

6. **Rolling Correlation** - 30-day rolling correlation trend

## Understanding Correlation

The script calculates correlation coefficient between -1 and 1:

- **> 0.7** = Strong positive (stocks move together)

- **0.3 to 0.7** = Moderate positive

- **-0.3 to 0.3** = Weak/no correlation

- **-0.7 to -0.3** = Moderate negative

- **< -0.7** = Strong negative (stocks move opposite)

## Customizing

**Change Stocks:**

Edit line 167 in the script:

```python

tickers = ["MAHSCOOTER.NS", "BAJAJHLDNG.NS"]

```

Replace with any NSE tickers (must end with .NS)

**Change Time Period:**

Edit line 172:

```python

data = fetch_stock_data(tickers, period="5y")

```

Options: "1y", "2y", "6mo", "max"

## Script Functions

- `fetch_stock_data()` - Downloads price data from Yahoo Finance

- `calculate_correlation()` - Computes correlation matrix and coefficient

- `calculate_statistics()` - Calculates key metrics for each stock

- `save_to_excel()` - Exports data to multi-sheet Excel file

- `create_visualizations()` - Generates and saves 6 charts

- `main()` - Runs the complete analysis pipeline

## Error Handling

The script handles:

- Invalid ticker symbols

- Empty data returns

- Missing or incomplete data

- Calculation errors

Error messages will guide you if something goes wrong.

## Notes

- Make sure ticker symbols are correct and supported by Yahoo Finance

- NSE stocks need `.NS` suffix (e.g., RELIANCE.NS)

- Internet connection required to fetch data

- Graphs display on screen and save automatically

## Troubleshooting

**No data retrieved?**

- Check ticker symbols are correct

- Verify Yahoo Finance supports the tickers

- Check internet connection

**Excel file won't open?**

- Make sure openpyxl is installed: `pip install openpyxl`

**Graphs don't display?**

- On some systems, you might need to install tkinter

- Graphs still save as PNG even if display fails