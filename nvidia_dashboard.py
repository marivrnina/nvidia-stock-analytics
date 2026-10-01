import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="NVIDIA Analytics", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>

.stApp {
    background-color: #0B0B0B;
    color: white;
}

.block-container {
    padding-top: 45px;
    padding-bottom: 15px;
    padding-left: 35px;
    padding-right: 35px;
    max-width: 1600px;
}

[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #292929;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #171717, #121212);
    border: 1px solid #2A2A2A;
    padding: 13px 18px;
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.20);
}

[data-testid="stMetricLabel"] {
    color: #A5A5A5 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

[data-testid="stMetricValue"] {
    color: #76B900 !important;
    font-size: 28px !important;
    font-weight: 650 !important;
}

[data-testid="stPlotlyChart"] {
    background-color: #151515;
    border: 1px solid #292929;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="column"] {
    padding-top: 4px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom:22px;">
    <div style="font-size:34px; line-height:1.25; font-weight:700; color:#FFFFFF; letter-spacing:-0.8px;">
        NVIDIA Analytics
    </div>
    <div style="font-size:14px; color:#A0A0A0; margin-top:7px;">
        Market Performance Dashboard · NVDA
    </div>
    <div style="font-size:12px; font-weight:600; color:#76B900; margin-top:5px;">
        January 2021 — Present
    </div>
</div>
""", unsafe_allow_html=True)

start_date = st.sidebar.date_input("Start date", pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End date", date.today())

ma50 = st.sidebar.checkbox("50-day moving average", True)
ma200 = st.sidebar.checkbox("200-day moving average", True)

nvda = yf.download("NVDA", start=start_date, end=end_date, auto_adjust=True, progress=False)
sp500 = yf.download("^GSPC", start=start_date, end=end_date, auto_adjust=True, progress=False)

if isinstance(nvda.columns, pd.MultiIndex):
    nvda.columns = nvda.columns.get_level_values(0)

if isinstance(sp500.columns, pd.MultiIndex):
    sp500.columns = sp500.columns.get_level_values(0)

if nvda.empty:
    st.warning("No data available for this date range.")
    st.stop()

nvda["Return"] = nvda["Close"].pct_change()
nvda["MA50"] = nvda["Close"].rolling(50).mean()
nvda["MA200"] = nvda["Close"].rolling(200).mean()

current_price = nvda["Close"].iloc[-1]
start_price = nvda["Close"].iloc[0]

total_return = (current_price / start_price - 1) * 100
volatility = nvda["Return"].std() * np.sqrt(252) * 100
annual_return = ((1 + nvda["Return"].mean()) ** 252 - 1) * 100
sharpe = (annual_return / 100 - 0.04) / (volatility / 100)

rolling_max = nvda["Close"].cummax()
drawdown = nvda["Close"] / rolling_max - 1
max_drawdown = drawdown.min() * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Current Price", f"${current_price:.2f}")
col2.metric("Period Return", f"{total_return:.1f}%")
col3.metric("Annual Volatility", f"{volatility:.1f}%")
col4.metric("Sharpe Ratio", f"{sharpe:.2f}")
col5.metric("Max Drawdown", f"{max_drawdown:.1f}%")

left, right = st.columns(2, gap="medium")

with left:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=nvda.index,
        y=nvda["Close"],
        name="NVDA",
        line=dict(color="#76B900", width=2.3)
    ))

    if ma50:
        fig.add_trace(go.Scatter(
            x=nvda.index,
            y=nvda["MA50"],
            name="50-day MA",
            line=dict(color="#FFFFFF", width=1.3)
        ))

    if ma200:
        fig.add_trace(go.Scatter(
            x=nvda.index,
            y=nvda["MA200"],
            name="200-day MA",
            line=dict(color="#666666", width=1.3)
        ))

    fig.update_layout(
        title=dict(text="Stock Performance", font=dict(size=17, color="#FFFFFF"), x=0.04),
        template="plotly_dark",
        paper_bgcolor="#151515",
        plot_bgcolor="#151515",
        height=300,
        margin=dict(l=50, r=20, t=55, b=40),
        font=dict(size=12, color="#B5B5B5"),
        yaxis_title="Price ($)",
        legend=dict(orientation="h", y=-0.17, x=0.02, font=dict(size=11))
    )

    fig.update_xaxes(gridcolor="#252525", tickfont=dict(size=11))
    fig.update_yaxes(gridcolor="#252525", tickfont=dict(size=11), title_font=dict(size=12))

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with right:

    comparison = pd.DataFrame()
    comparison["NVDA"] = nvda["Close"] / nvda["Close"].iloc[0] * 100
    comparison["S&P 500"] = sp500["Close"] / sp500["Close"].iloc[0] * 100
    comparison = comparison.dropna()

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=comparison.index,
        y=comparison["NVDA"],
        name="NVDA",
        line=dict(color="#76B900", width=2.3)
    ))

    fig2.add_trace(go.Scatter(
        x=comparison.index,
        y=comparison["S&P 500"],
        name="S&P 500",
        line=dict(color="#C0C0C0", width=1.5)
    ))

    fig2.update_layout(
        title=dict(
            text="Performance vs S&P 500<br><sup>Growth of $100 invested</sup>",
            font=dict(size=17, color="#FFFFFF"),
            x=0.04
        ),
        template="plotly_dark",
        paper_bgcolor="#151515",
        plot_bgcolor="#151515",
        height=300,
        margin=dict(l=55, r=20, t=55, b=40),
        font=dict(size=12, color="#B5B5B5"),
        yaxis_title="Value ($)",
        legend=dict(orientation="h", y=-0.17, x=0.02, font=dict(size=11))
    )

    fig2.update_xaxes(gridcolor="#252525", tickfont=dict(size=11))
    fig2.update_yaxes(gridcolor="#252525", tickfont=dict(size=11), title_font=dict(size=12))

    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

bottom1, bottom2, bottom3 = st.columns(3, gap="medium")

monthly_returns = nvda["Close"].resample("ME").last().pct_change() * 100

monthly = pd.DataFrame()
monthly["Date"] = monthly_returns.index
monthly["Return"] = monthly_returns.values
monthly = monthly.dropna()

colors = []

for value in monthly["Return"]:
    if value >= 0:
        colors.append("#76B900")
    else:
        colors.append("#666666")

with bottom1:

    fig3 = go.Figure()

    fig3.add_trace(go.Bar(
        x=monthly["Date"],
        y=monthly["Return"],
        marker_color=colors
    ))

    fig3.update_layout(
        title=dict(text="Monthly Returns", font=dict(size=16, color="#FFFFFF"), x=0.05),
        template="plotly_dark",
        paper_bgcolor="#151515",
        plot_bgcolor="#151515",
        height=245,
        margin=dict(l=45, r=15, t=50, b=35),
        font=dict(size=11, color="#B5B5B5"),
        yaxis_title="Return (%)",
        showlegend=False
    )

    fig3.update_xaxes(gridcolor="#252525", tickfont=dict(size=10))
    fig3.update_yaxes(gridcolor="#252525", tickfont=dict(size=10))

    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

with bottom2:

    returns = nvda["Return"].dropna() * 100

    fig4 = go.Figure()

    fig4.add_trace(go.Histogram(
        x=returns,
        nbinsx=45,
        marker_color="#76B900"
    ))

    fig4.update_layout(
        title=dict(
            text="Daily Return Distribution<br><sup>Frequency of daily price changes</sup>",
            font=dict(size=16, color="#FFFFFF"),
            x=0.05
        ),
        template="plotly_dark",
        paper_bgcolor="#151515",
        plot_bgcolor="#151515",
        height=245,
        margin=dict(l=45, r=15, t=50, b=35),
        font=dict(size=11, color="#B5B5B5"),
        xaxis_title="Daily Return (%)",
        showlegend=False
    )

    fig4.update_xaxes(gridcolor="#252525", tickfont=dict(size=10))
    fig4.update_yaxes(gridcolor="#252525", tickfont=dict(size=10))

    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

with bottom3:

    drawdown_data = pd.DataFrame()
    drawdown_data["Date"] = nvda.index
    drawdown_data["Drawdown"] = drawdown.values * 100

    fig5 = go.Figure()

    fig5.add_trace(go.Scatter(
        x=drawdown_data["Date"],
        y=drawdown_data["Drawdown"],
        line=dict(color="#76B900", width=1.5),
        fill="tozeroy",
        fillcolor="rgba(118,185,0,0.18)"
    ))

    fig5.update_layout(
        title=dict(
            text="Drawdown<br><sup>Decline from previous market peak</sup>",
            font=dict(size=16, color="#FFFFFF"),
            x=0.05
        ),
        template="plotly_dark",
        paper_bgcolor="#151515",
        plot_bgcolor="#151515",
        height=245,
        margin=dict(l=45, r=15, t=50, b=35),
        font=dict(size=11, color="#B5B5B5"),
        yaxis_title="Drawdown (%)",
        showlegend=False
    )

    fig5.update_xaxes(gridcolor="#252525", tickfont=dict(size=10))
    fig5.update_yaxes(gridcolor="#252525", tickfont=dict(size=10))

    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})