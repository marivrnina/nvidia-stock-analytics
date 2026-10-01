# NVIDIA Stock Analytics Dashboard

An interactive financial analytics dashboard for exploring NVIDIA (NVDA) stock performance, risk, and historical trends.

Built with Python, Streamlit, Plotly, and Yahoo Finance.

## Project Overview

The goal of this project was to create a compact financial dashboard that makes it easier to analyze NVIDIA's historical stock performance without working through raw market data.

The dashboard combines return and risk metrics with interactive visualizations and an S&P 500 benchmark.

Users can change the analysis period and toggle moving averages directly from the dashboard.

## Key Insights

### Strong Long-Term Performance

Over the selected period beginning in January 2021, NVIDIA generated a cumulative price return of approximately **1,642%**.

This represents substantial long-term appreciation, although the return was not consistent throughout the period. The price chart shows several periods of significant growth as well as major corrections.

### High Return Came With High Volatility

NVIDIA's annualized volatility was approximately **50.6%** over the analyzed period.

This indicates that the stock experienced substantial price fluctuations despite its strong overall return.

The daily return distribution also shows that most daily movements were concentrated around zero, with occasional much larger positive and negative movements.

### Significant Historical Drawdowns

The maximum drawdown during the selected period was approximately **-66.3%**.

This means that at its largest peak-to-trough decline, NVIDIA lost roughly two-thirds of its value from a previous high before recovering.

This highlights an important distinction between long-term return and the risk an investor would have experienced along the way.

### Risk-Adjusted Performance

The dashboard estimates a Sharpe ratio of approximately **1.64**, using a 4% risk-free-rate assumption.

The positive Sharpe ratio indicates that NVIDIA's historical returns compensated for the volatility observed during the selected period, although the result depends on the selected timeframe and risk-free-rate assumption.

### NVIDIA vs. the S&P 500

To provide market context, NVIDIA's performance is compared with the S&P 500 using the hypothetical growth of $100 invested at the beginning of the selected period.

The visualization shows substantial divergence between NVIDIA and the broader market, particularly during NVIDIA's major growth periods.

The comparison also demonstrates why benchmarking an individual stock can provide more context than evaluating its return independently.

### Moving Averages and Price Trends

The dashboard includes 50-day and 200-day moving averages to make longer-term price trends easier to identify.

The 50-day moving average responds more quickly to recent price movements, while the 200-day moving average provides a smoother view of the longer-term trend.

### Monthly Performance

Monthly returns show that NVIDIA's long-term growth was not evenly distributed across time.

The stock experienced both strongly positive months and substantial negative months, reinforcing the volatility observed in the other risk measures.

## Dashboard Features

- Historical NVIDIA stock prices
- 50-day and 200-day moving averages
- Cumulative period return
- Annualized volatility
- Sharpe ratio
- Maximum drawdown
- Monthly return analysis
- Daily return distribution
- S&P 500 benchmark
- Interactive date selection
- Interactive moving-average controls

## Tech Stack

- **Python**
- **Pandas** for data manipulation and financial calculations
- **NumPy** for numerical analysis
- **yfinance** for historical market data
- **Plotly** for interactive visualizations
- **Streamlit** for the dashboard interface

## Financial Metrics

Daily returns are calculated as:

`Return = (Current Price / Previous Price) - 1`

Annualized volatility is estimated using:

`Annualized Volatility = Standard Deviation of Daily Returns × √252`

Maximum drawdown measures the largest percentage decline from a previous historical peak.

The Sharpe ratio is calculated using an assumed annual risk-free rate of 4%.

## Run the Dashboard

Install the required libraries:

pip install streamlit yfinance pandas numpy plotly

Run the application:

streamlit run app.py

## Data Source

Historical market data is retrieved programmatically using Yahoo Finance through the `yfinance` Python package.

Data and calculated metrics depend on the selected date range and may change as new market data becomes available.

## Disclaimer

This project is intended for educational and portfolio purposes only and does not constitute investment advice.
