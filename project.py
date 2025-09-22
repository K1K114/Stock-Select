# STOCK ANALYSIS PIPELINE

from pyfiglet import Figlet
from tabulate import tabulate
import yfinance as yf
from datetime import date, timedelta
import warnings
from alive_progress import alive_bar
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import os

# Setup
pio.renderers.default = "browser"
warnings.filterwarnings("ignore")
os.system("clear")


# ---------------------- Data Classes ----------------------
class StockData:
    """Container for individual stock data"""
    def __init__(self, ticker, monthly_data, fast, pastyear, chart):
        self.ticker = ticker
        self.monthly_data = monthly_data
        self.fast = fast
        self.pastyear = pastyear
        self.chart = chart


class IndustryData:
    """Container for sector/industry summary data"""
    def __init__(self, name, stocklist, headers):
        self.name = name
        self.stocklist = stocklist
        self.headers = headers


# ---------------------- CLI ----------------------
def main():
    while True:
        display_title()
        choice = input("Enter an option (1-4): ").strip()

        if choice == "1":
            stock_lookup()
        elif choice == "2":
            sector_lookup()
        elif choice == "3":
            portfolio_analysis()
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice, please try again.")

    goodbye_message()


def display_title():
    os.system("clear")
    title = Figlet(font="slant").renderText("Stock Select")
    print(title)
    table = [[1, "Search a Stock"], [2, "Sector Overview"],
             [3, "Portfolio Analysis"], [4, "Exit"]]
    print(tabulate(table, headers=["ID", "Feature"], tablefmt="fancy_grid"))
    print("")


def goodbye_message():
    msg = Figlet(font="larry3d").renderText("Ending Session...")
    print(msg)


# ---------------------- Stock Lookup ----------------------
def stock_lookup():
    ticker = input("\nEnter a stock ticker (e.g., AAPL, TSLA): ").upper().strip()
    data = fetch_stock_data(ticker)

    if not data:
        print("❌ Could not retrieve data.")
        return

    fast = data.fast
    print(f"\n📊 {ticker} - Market Data Today (USD)\n")
    
    # Handle both fast_info and info dict formats
    def get_value(source, *field_names):
        for field in field_names:
            if hasattr(source, field) and getattr(source, field) is not None:
                return getattr(source, field)
            elif isinstance(source, dict) and field in source and source[field] is not None:
                return source[field]
        return 'N/A'
    
    print(f" Current Price:           {get_value(fast, 'last_price', 'regularMarketPrice', 'currentPrice')}")
    print(f" Previous Close:          {get_value(fast, 'previous_close', 'regularMarketPreviousClose', 'previousClose')}")
    print(f" 52 Week Range:           {get_value(fast, 'year_low', 'fiftyTwoWeekLow')} - {get_value(fast, 'year_high', 'fiftyTwoWeekHigh')}")
    print(f" Market Cap:              {get_value(fast, 'market_cap', 'marketCap')}")
    print(f" Volume:                  {get_value(fast, 'last_volume', 'regularMarketVolume', 'volume')}")
    print(f" PE Ratio (TTM):          {get_value(fast, 'trailing_pe', 'trailingPE')}")
    print(f" 1-Year Target Estimate:  {get_value(fast, 'target_mean_price', 'targetMeanPrice')}\n")

    show_hist = input("Show past year historical data (y/n)? ").lower()
    if show_hist in ["y", "yes"]:
        headers = ["Date", "Open", "High", "Low", "Close", "Volume"]
        print(tabulate(data.monthly_data, headers=headers, tablefmt="grid"))

    show_chart = input("Show past year chart (y/n)? ").lower()
    if show_chart in ["y", "yes"]:
        data.chart.show()

    forecast_choice = input("Run forecast for next 30 days (y/n)? ").lower()
    if forecast_choice in ["y", "yes"]:
        forecast_prices(data)
    
    input("\n📋 Press Enter to return to main menu...")


def fetch_stock_data(ticker):
    try:
        with alive_bar(3, title="Fetching Data", bar="smooth") as bar:
            today = date.today()
            last_year = today - timedelta(weeks=52)

            stock = yf.Ticker(ticker)
            monthly = stock.history(start=last_year, end=today, interval="1mo")
            if monthly.empty:
                print(f"❌ No data found for ticker: {ticker}")
                return None
                
            # Try fast_info first, fall back to info if needed
            try:
                fast = stock.fast_info
                # Test if fast_info is working by checking for a common field
                if not hasattr(fast, 'last_price') or fast.last_price is None:
                    fast = stock.info
            except:
                fast = stock.info
            bar()

            daily = stock.history(start=last_year, end=today, interval="1d")
            if daily.empty:
                print(f"❌ No daily data found for ticker: {ticker}")
                return None
            bar()

            chart = go.Figure(go.Scatter(x=daily.index, y=daily["Close"],
                                         mode="lines", name=f"{ticker} Close"))
            chart.update_layout(
                title=f"{ticker} - Past Year Closing Prices",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                template="plotly_white"
            )
            bar()

            # Format monthly data for display
            monthly_formatted = []
            for idx, row in monthly.iterrows():
                monthly_formatted.append([
                    idx.strftime('%Y-%m-%d'),
                    f"{row['Open']:.2f}",
                    f"{row['High']:.2f}",
                    f"{row['Low']:.2f}",
                    f"{row['Close']:.2f}",
                    f"{int(row['Volume']):,}"
                ])

            return StockData(
                ticker,
                monthly_formatted,
                fast,
                daily,
                chart
            )
    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {e}")
        return None


def forecast_prices(data):
    try:
        closes = data.pastyear["Close"].dropna()
        if len(closes) < 30:
            print("❌ Insufficient data for forecasting (need at least 30 data points)")
            return
            
        model = ARIMA(closes, order=(5, 1, 0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=30)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=closes.index, y=closes, mode="lines", name="Historical"))
        future_dates = pd.date_range(closes.index[-1] + pd.Timedelta(days=1), periods=30)
        fig.add_trace(go.Scatter(x=future_dates, y=forecast, mode="lines", name="Forecast"))
        fig.update_layout(title=f"{data.ticker} - 30 Day Forecast",
                          xaxis_title="Date", yaxis_title="Price (USD)",
                          template="plotly_white")
        fig.show()
        print(f"📈 Forecast completed for {data.ticker}")
    except Exception as e:
        print(f"❌ Error generating forecast: {e}")


# ---------------------- Sector Overview ----------------------
def sector_lookup():
    print("\n📂 Choose a sector:")
    sectors = {
        "technology": ["AAPL", "MSFT", "GOOGL", "NVDA", "META"],
        "finance": ["JPM", "BAC", "GS", "V", "MA"],
        "healthcare": ["LLY", "JNJ", "UNH", "ABBV", "PFE"],
        "energy": ["XOM", "CVX", "COP", "SLB", "EOG"]
    }

    for i, sector in enumerate(sectors.keys(), start=1):
        print(f"{i}: {sector.title()}")

    choice = input("\nEnter sector name: ").lower().strip()
    if choice not in sectors:
        print("❌ Invalid sector")
        return

    data = fetch_sector_data(choice, sectors[choice])
    if data:
        print(f"\n📊 {data.name}\n")
        print(tabulate(data.stocklist, headers=data.headers, tablefmt="fancy_grid"))
        input("\n📋 Press Enter to return to main menu...")


def fetch_sector_data(name, tickers):
    results = []
    headers = ["Ticker", "Quote", "52W Range", "PE", "Volume"]

    try:
        with alive_bar(len(tickers), title="Fetching Sector Data", bar="smooth") as bar:
            for t in tickers:
                try:
                    stock = yf.Ticker(t)
                    
                    # Try fast_info first, fall back to info if needed
                    try:
                        fast = stock.fast_info
                        # Check if fast_info has data
                        if hasattr(fast, 'last_price') and fast.last_price is not None:
                            info_source = fast
                        else:
                            # Fall back to info method
                            info_source = stock.info
                    except:
                        # If fast_info fails, use info method
                        info_source = stock.info
                    
                    # Get current price using multiple possible field names
                    current_price = None
                    for price_field in ['last_price', 'regularMarketPrice', 'currentPrice', 'price']:
                        if hasattr(info_source, price_field):
                            current_price = getattr(info_source, price_field)
                        elif isinstance(info_source, dict) and price_field in info_source:
                            current_price = info_source[price_field]
                        if current_price is not None:
                            break
                    
                    # Get 52-week range
                    year_low = None
                    year_high = None
                    for low_field in ['year_low', 'fiftyTwoWeekLow']:
                        if hasattr(info_source, low_field):
                            year_low = getattr(info_source, low_field)
                        elif isinstance(info_source, dict) and low_field in info_source:
                            year_low = info_source[low_field]
                        if year_low is not None:
                            break
                    
                    for high_field in ['year_high', 'fiftyTwoWeekHigh']:
                        if hasattr(info_source, high_field):
                            year_high = getattr(info_source, high_field)
                        elif isinstance(info_source, dict) and high_field in info_source:
                            year_high = info_source[high_field]
                        if year_high is not None:
                            break
                    
                    # Get PE ratio
                    pe_ratio = None
                    for pe_field in ['trailing_pe', 'trailingPE', 'pe_ratio']:
                        if hasattr(info_source, pe_field):
                            pe_ratio = getattr(info_source, pe_field)
                        elif isinstance(info_source, dict) and pe_field in info_source:
                            pe_ratio = info_source[pe_field]
                        if pe_ratio is not None:
                            break
                    
                    # Get volume
                    volume = None
                    for vol_field in ['last_volume', 'regularMarketVolume', 'volume']:
                        if hasattr(info_source, vol_field):
                            volume = getattr(info_source, vol_field)
                        elif isinstance(info_source, dict) and vol_field in info_source:
                            volume = info_source[vol_field]
                        if volume is not None:
                            break
                    
                    # Format values
                    quote = f"${current_price:.2f}" if current_price else "N/A"
                    year_range = f"${year_low:.2f} - ${year_high:.2f}" if year_low and year_high else "N/A"
                    pe_str = f"{pe_ratio:.2f}" if pe_ratio else "N/A"
                    volume_str = f"{volume:,}" if volume else "N/A"
                    
                    results.append([t, quote, year_range, pe_str, volume_str])
                    
                except Exception as e:
                    print(f"⚠️  Warning: Could not fetch data for {t}: {e}")
                    results.append([t, "N/A", "N/A", "N/A", "N/A"])
                bar()

        return IndustryData(f"Top {name.title()} Stocks", results, headers)
    except Exception as e:
        print(f"❌ Error fetching sector data: {e}")
        return None


# ---------------------- Portfolio Analysis ----------------------
def portfolio_analysis():
    try:
        tickers_input = input("\nEnter tickers in portfolio (comma separated, e.g., AAPL,MSFT,GOOGL): ").upper().strip()
        tickers = [t.strip() for t in tickers_input.split(",") if t.strip()]
        
        if not tickers:
            print("❌ No tickers provided.")
            return
            
        weights_input = input("Enter weights (comma separated, e.g., 0.4,0.3,0.3): ").strip()
        try:
            weights = [float(w.strip()) for w in weights_input.split(",") if w.strip()]
        except ValueError:
            print("❌ Invalid weight format. Please enter numbers separated by commas.")
            return

        if len(tickers) != len(weights):
            print("❌ Number of tickers must match number of weights.")
            return
            
        if not np.isclose(sum(weights), 1.0, atol=0.01):
            print(f"❌ Weights must sum to 1.0 (currently sum to {sum(weights):.3f})")
            return

        print(f"\n📊 Analyzing portfolio with {len(tickers)} stocks...")
        
        today = date.today()
        last_year = today - timedelta(weeks=52)

        # Download data with error handling
        print("📥 Downloading historical data...")
        raw_data = yf.download(tickers, start=last_year, end=today, progress=False)
        
        if raw_data.empty:
            print("❌ No data retrieved for the specified tickers.")
            return
        
        # Handle different data structures based on number of tickers and available columns
        if len(tickers) == 1:
            # Single ticker - data might not have MultiIndex
            if isinstance(raw_data.columns, pd.MultiIndex):
                if "Adj Close" in [col[0] for col in raw_data.columns]:
                    data = raw_data["Adj Close"].to_frame()
                    data.columns = [tickers[0]]
                elif "Close" in [col[0] for col in raw_data.columns]:
                    data = raw_data["Close"].to_frame()
                    data.columns = [tickers[0]]
                else:
                    print("❌ No suitable price data found.")
                    return
            else:
                # Simple column structure
                if "Adj Close" in raw_data.columns:
                    data = raw_data[["Adj Close"]].copy()
                    data.columns = [tickers[0]]
                elif "Close" in raw_data.columns:
                    data = raw_data[["Close"]].copy()
                    data.columns = [tickers[0]]
                else:
                    print("❌ No suitable price data found.")
                    return
        else:
            # Multiple tickers - should have MultiIndex
            if isinstance(raw_data.columns, pd.MultiIndex):
                if "Adj Close" in raw_data.columns.get_level_values(0):
                    data = raw_data["Adj Close"]
                elif "Close" in raw_data.columns.get_level_values(0):
                    data = raw_data["Close"]
                else:
                    print("❌ No suitable price data found.")
                    return
            else:
                print("❌ Unexpected data structure for multiple tickers.")
                return
        
        if data.empty:
            print("❌ No data retrieved for the specified tickers.")
            return
            
        # Handle single ticker case
        if len(tickers) == 1:
            data = pd.DataFrame({tickers[0]: data})
            
        returns = data.pct_change().dropna()

        # Check if we have sufficient data
        if len(returns) < 30:
            print("❌ Insufficient historical data for analysis (need at least 30 days)")
            return

        mean_returns = returns.mean() * 252  # Annualized
        cov_matrix = returns.cov() * 252     # Annualized

        weights = np.array(weights)
        port_return = np.dot(weights, mean_returns)
        port_vol = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
        
        # Calculate Sharpe ratio (assuming risk-free rate of 2%)
        risk_free_rate = 0.02
        sharpe = (port_return - risk_free_rate) / port_vol if port_vol > 0 else 0

        print("\n📊 Portfolio Analysis Results\n")
        print(f" Expected Annual Return: {port_return:.2%}")
        print(f" Annual Volatility:      {port_vol:.2%}")
        print(f" Sharpe Ratio:           {sharpe:.2f}")
        print(f" Risk-Free Rate Used:    {risk_free_rate:.2%}\n")

        # Display individual stock weights
        print("📋 Portfolio Composition:")
        for ticker, weight in zip(tickers, weights):
            print(f" {ticker}: {weight:.1%}")
        
        input("\n📋 Press Enter to return to main menu...")
        
    except Exception as e:
        print(f"❌ Error in portfolio analysis: {e}")
        input("\n📋 Press Enter to return to main menu...")


# ---------------------- Run ----------------------
if __name__ == "__main__":
    main()