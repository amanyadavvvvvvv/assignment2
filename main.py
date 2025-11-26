import yfinance as yf
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

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

def calculate_statistics(data):
    """Calculate basic statistics for the stocks"""
    try:
        stats = pd.DataFrame({
            'Mean': data.mean(),
            'Median': data.median(),
            'Std Dev': data.std(),
            'Min': data.min(),
            'Max': data.max(),
            'Current Price': data.iloc[-1] if len(data) > 0 else None
        })
        return stats
    except Exception as e:
        print(f"Error calculating statistics: {str(e)}")
        return None

def save_to_excel(data, corr_matrix, stats, tickers, filename=None):
    """Save all data and analysis to Excel file"""
    try:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"stock_analysis_{timestamp}.xlsx"
        
        # Create Excel writer
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: Raw stock data
            data.to_excel(writer, sheet_name='Stock Prices')
            
            # Sheet 2: Correlation matrix
            corr_matrix.to_excel(writer, sheet_name='Correlation Matrix')
            
            # Sheet 3: Statistics
            if stats is not None:
                stats.to_excel(writer, sheet_name='Statistics')
            
            # Sheet 4: Summary
            summary = pd.DataFrame({
                'Ticker': tickers,
                'Data Points': [len(data)] * len(tickers),
                'Date Range': [f"{data.index[0].date()} to {data.index[-1].date()}"] * len(tickers)
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"✓ Data saved to Excel: {filename}\n")
        return filename
        
    except Exception as e:
        print(f"Error saving to Excel: {str(e)}")
        return None

def create_visualizations(data, corr_matrix, tickers):
    """Create and save visualizations"""
    try:
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 10))
        
        # 1. Line plot - Stock prices over time
        ax1 = plt.subplot(2, 3, 1)
        for ticker in tickers:
            if ticker in data.columns:
                ax1.plot(data.index, data[ticker], label=ticker, linewidth=2)
        ax1.set_title('Stock Prices Over Time', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date', fontsize=10)
        ax1.set_ylabel('Price (₹)', fontsize=10)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Normalized prices (starting at 100)
        ax2 = plt.subplot(2, 3, 2)
        normalized_data = (data / data.iloc[0]) * 100
        for ticker in tickers:
            if ticker in normalized_data.columns:
                ax2.plot(normalized_data.index, normalized_data[ticker], label=ticker, linewidth=2)
        ax2.set_title('Normalized Stock Performance (Base=100)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Date', fontsize=10)
        ax2.set_ylabel('Indexed Value', fontsize=10)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Correlation heatmap
        ax3 = plt.subplot(2, 3, 3)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                    fmt='.3f', square=True, ax=ax3, cbar_kws={'label': 'Correlation'})
        ax3.set_title('Correlation Heatmap', fontsize=14, fontweight='bold')
        
        # 4. Daily returns distribution
        ax4 = plt.subplot(2, 3, 4)
        returns = data.pct_change().dropna()
        for ticker in tickers:
            if ticker in returns.columns:
                ax4.hist(returns[ticker] * 100, alpha=0.6, bins=50, label=ticker)
        ax4.set_title('Daily Returns Distribution', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Daily Return (%)', fontsize=10)
        ax4.set_ylabel('Frequency', fontsize=10)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Scatter plot
        ax5 = plt.subplot(2, 3, 5)
        if len(tickers) >= 2:
            ax5.scatter(data[tickers[0]], data[tickers[1]], alpha=0.5, s=20)
            ax5.set_title(f'Price Relationship', fontsize=14, fontweight='bold')
            ax5.set_xlabel(f'{tickers[0]} Price (₹)', fontsize=10)
            ax5.set_ylabel(f'{tickers[1]} Price (₹)', fontsize=10)
            ax5.grid(True, alpha=0.3)
            
            # Add correlation value to plot
            corr_val = corr_matrix.iloc[0, 1]
            ax5.text(0.05, 0.95, f'Correlation: {corr_val:.3f}', 
                    transform=ax5.transAxes, fontsize=12, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 6. Rolling correlation (30-day window)
        ax6 = plt.subplot(2, 3, 6)
        if len(tickers) >= 2:
            rolling_corr = data[tickers[0]].rolling(window=30).corr(data[tickers[1]])
            ax6.plot(rolling_corr.index, rolling_corr, linewidth=2, color='purple')
            ax6.axhline(y=0, color='r', linestyle='--', alpha=0.3)
            ax6.set_title('30-Day Rolling Correlation', fontsize=14, fontweight='bold')
            ax6.set_xlabel('Date', fontsize=10)
            ax6.set_ylabel('Correlation Coefficient', fontsize=10)
            ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        graph_filename = f"stock_analysis_graphs_{timestamp}.png"
        plt.savefig(graph_filename, dpi=300, bbox_inches='tight')
        print(f"✓ Graphs saved: {graph_filename}\n")
        
        # Show the plots
        plt.show()
        
        return graph_filename
        
    except Exception as e:
        print(f"Error creating visualizations: {str(e)}")
        return None

def main():
    """Main execution function"""
    try:
        # List of stocks
        tickers = ["MAHSCOOTER.NS", "BAJAJHLDNG.NS"]
        
        print("="*60)
        print("STOCK CORRELATION ANALYSIS TOOL")
        print("="*60 + "\n")
        
        # Fetch stock data
        data = fetch_stock_data(tickers, period="5y")
        
        if data is None:
            print("\nFailed to fetch stock data. Exiting.")
            return
        
        # Display first few rows
        print("Stock Data (Closing Prices) - First 5 rows:")
        print(data.head())
        print()
        
        # Calculate correlation
        corr_matrix, corr_value = calculate_correlation(data, tickers)
        
        if corr_matrix is None:
            print("\nFailed to calculate correlation. Exiting.")
            return
        
        # Calculate statistics
        stats = calculate_statistics(data)
        
        # Display correlation matrix
        print("Correlation Matrix:")
        print(corr_matrix)
        print()
        
        # Display correlation coefficient
        if corr_value is not None:
            print(f"Correlation Coefficient between {tickers[0]} and {tickers[1]}: {corr_value:.4f}")
            
            # Interpret correlation
            if corr_value > 0.7:
                interpretation = "Strong Positive Correlation"
            elif corr_value > 0.3:
                interpretation = "Moderate Positive Correlation"
            elif corr_value > -0.3:
                interpretation = "Weak/No Correlation"
            elif corr_value > -0.7:
                interpretation = "Moderate Negative Correlation"
            else:
                interpretation = "Strong Negative Correlation"
            
            print(f"Interpretation: {interpretation}\n")
        
        # Display statistics
        if stats is not None:
            print("Stock Statistics:")
            print(stats)
            print()
        
        # Save to Excel
        excel_file = save_to_excel(data, corr_matrix, stats, tickers)
        
        # Create visualizations
        graph_file = create_visualizations(data, corr_matrix, tickers)
        
        print("="*60)
        print("ANALYSIS COMPLETE!")
        print("="*60)
        if excel_file:
            print(f"📊 Excel Report: {excel_file}")
        if graph_file:
            print(f"📈 Graphs: {graph_file}")
        print()
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error in main execution: {str(e)}")

if __name__ == "__main__":
    main()