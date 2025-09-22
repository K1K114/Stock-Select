# Stock Analysis Pipeline
A comprehensive command-line stock analysis tool that provides real-time market data, historical analysis, forecasting, and portfolio risk assessment.

---

## Features

### 📊 Stock Lookup
- Real-time stock data including current price, volume, market cap  
- 52-week high/low ranges and PE ratios  
- Historical data visualization with interactive charts  
- 30-day ARIMA price forecasting  

### 🏢 Sector Overview
Pre-configured sector analysis for major industries:
- **Technology**: AAPL, MSFT, GOOGL, NVDA, META  
- **Finance**: JPM, BAC, GS, V, MA  
- **Healthcare**: LLY, JNJ, UNH, ABBV, PFE  
- **Energy**: XOM, CVX, COP, SLB, EOG  

Includes side-by-side comparison of key metrics.

### 💼 Portfolio Analysis
- Multi-stock portfolio risk analysis  
- Expected annual returns and volatility calculations  
- Sharpe ratio computation with risk-free rate assumptions  
- Portfolio composition breakdown  
- Modern Portfolio Theory implementation  

### Requirements
- Python 3.7+
- Internet connection for real-time data
- Terminal/command prompt with ASCII support for best display

---

## Installation
Clone or download the repository:
```bash
git clone <repository-url>
cd stock-analysis-pipeline
pip install -r requirements.txt
python stock_analysis.py

