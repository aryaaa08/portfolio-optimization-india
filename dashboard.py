

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Indian Equity Portfolio Optimization",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "Indian Equity Portfolio Optimization Dashboard"
)

st.markdown(
    """
    **Modern Portfolio Theory • Portfolio Optimization •
    Out-of-Sample Backtesting • Robustness Analysis**
    """
)

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    performance = pd.read_csv(
        "performance_table.csv",
        index_col=0
    )

    weights = pd.read_csv(
        "optimized_portfolio_weights.csv",
        index_col=0
    )

    frontier = pd.read_csv(
        "efficient_frontier.csv"
    )

    daily_returns = pd.read_csv(
        "daily_returns.csv",
        index_col=0,
        parse_dates=True
    )

    robustness = pd.read_csv(
        "robustness_performance_table.csv",
        index_col=0
    )

    sector_weights = pd.read_csv(
        "sector_weights.csv",
        index_col=0
    )

    risk_free_sensitivity = pd.read_csv(
        "risk_free_sensitivity.csv",
        index_col=0
    )

    wealth = pd.read_csv(
        "robustness_wealth_paths.csv",
        index_col=0,
        parse_dates=True
    )

    return (
        performance,
        weights,
        frontier,
        daily_returns,
        robustness,
        sector_weights,
        risk_free_sensitivity,
        wealth
    )


(
    performance,
    weights,
    frontier,
    daily_returns,
    robustness,
    sector_weights,
    risk_free_sensitivity,
    wealth
) = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Dashboard Controls")

portfolio_options = [
    "Minimum Variance",
    "Maximum Sharpe",
    "Equal Weight",
    "Nifty 50"
]

selected_portfolio = st.sidebar.selectbox(
    "Select Portfolio",
    portfolio_options
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    ### Research Design

    **Universe:** 20 Indian equities

    **Historical period:** 2015–2025

    **Training:** 2015–2022

    **Testing:** 2023–2025

    **Benchmark:** Nifty 50

    **Constraints:**
    - No short selling
    - Maximum 25% per stock
    - Weights sum to 100%
    """
)


# ============================================================
# SECTION 1 — KEY PERFORMANCE INDICATORS
# ============================================================

st.header("Out-of-Sample Performance")

selected_metrics = performance.loc[
    selected_portfolio
]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Annual Return",
        f"{selected_metrics['Annual Return']:.2%}"
    )

with col2:
    st.metric(
        "Annual Volatility",
        f"{selected_metrics['Annual Volatility']:.2%}"
    )

with col3:
    st.metric(
        "Sharpe Ratio",
        f"{selected_metrics['Sharpe Ratio']:.2f}"
    )

with col4:
    st.metric(
        "Maximum Drawdown",
        f"{selected_metrics['Maximum Drawdown']:.2%}"
    )


# ============================================================
# SECTION 2 — PERFORMANCE TABLE
# ============================================================

st.subheader("Portfolio Performance Comparison")

performance_display = performance.copy()

performance_display["Annual Return"] = (
    performance_display["Annual Return"] * 100
).round(2)

performance_display["Annual Volatility"] = (
    performance_display["Annual Volatility"] * 100
).round(2)

performance_display["Maximum Drawdown"] = (
    performance_display["Maximum Drawdown"] * 100
).round(2)

performance_display["Sharpe Ratio"] = (
    performance_display["Sharpe Ratio"]
).round(2)

st.dataframe(
    performance_display,
    use_container_width=True
)


# ============================================================
# SECTION 3 — RISK RETURN CHART
# ============================================================

st.header("Risk–Return Analysis")

risk_return = performance.reset_index()

risk_return.columns = [
    "Portfolio",
    "Annual Return",
    "Annual Volatility",
    "Sharpe Ratio",
    "Maximum Drawdown"
]

fig = px.scatter(
    risk_return,
    x="Annual Volatility",
    y="Annual Return",
    text="Portfolio",
    size="Sharpe Ratio",
    hover_data=[
        "Sharpe Ratio",
        "Maximum Drawdown"
    ],
    title="Out-of-Sample Risk–Return Profile"
)

fig.update_traces(
    textposition="top center"
)

fig.update_layout(
    xaxis_title="Annualized Volatility",
    yaxis_title="Annualized Return"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SECTION 4 — PORTFOLIO ALLOCATION
# ============================================================

st.header("Portfolio Allocation")

if selected_portfolio == "Nifty 50":

    st.info(
        "Nifty 50 is used as the benchmark and does not have "
        "portfolio weights in this analysis."
    )

else:

    selected_weights = weights.copy()

    if selected_portfolio == "Equal Weight":

        selected_weights["Equal Weight"] = (
            1 / len(selected_weights)
        )

    selected_weights = selected_weights[
        selected_portfolio
    ].sort_values(
        ascending=False
    )

    allocation_df = pd.DataFrame({
        "Stock": selected_weights.index,
        "Weight": selected_weights.values
    })

    fig = px.bar(
        allocation_df.sort_values("Weight"),
        x="Weight",
        y="Stock",
        orientation="h",
        title=f"{selected_portfolio} Portfolio Weights"
    )

    fig.update_layout(
        xaxis_title="Portfolio Weight",
        yaxis_title="Stock"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SECTION 5 — SECTOR ALLOCATION
# ============================================================

st.header("Sector Allocation")

if selected_portfolio != "Nifty 50":

    if selected_portfolio == "Equal Weight":

        sector_data = sector_weights[
            "Equal Weight"
        ]

    else:

        sector_data = sector_weights[
            selected_portfolio
        ]

    sector_data = sector_data.sort_values(
        ascending=False
    )

    sector_df = pd.DataFrame({
        "Sector": sector_data.index,
        "Weight": sector_data.values
    })

    fig = px.bar(
        sector_df,
        x="Sector",
        y="Weight",
        title=f"{selected_portfolio} Sector Allocation"
    )

    fig.update_layout(
        yaxis_title="Portfolio Weight"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SECTION 6 — EFFICIENT FRONTIER
# ============================================================

st.header("Efficient Frontier")

fig = go.Figure()

# Efficient frontier

fig.add_trace(
    go.Scatter(
        x=frontier["Volatility"],
        y=frontier["Target Return"],
        mode="lines",
        name="Efficient Frontier"
    )
)


# Random portfolios

random_portfolios = pd.read_pickle(
    "random_portfolios.pkl"
)

fig.add_trace(
    go.Scatter(
        x=random_portfolios["Volatility"],
        y=random_portfolios["Return"],
        mode="markers",
        name="Random Portfolios",
        marker=dict(
            size=4,
            opacity=0.25
        )
    )
)


fig.update_layout(
    title="Efficient Frontier and Feasible Portfolio Set",
    xaxis_title="Annualized Volatility",
    yaxis_title="Expected Annualized Return"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SECTION 7 — ROBUSTNESS ANALYSIS
# ============================================================

st.header("Robustness Analysis")

st.markdown(
    """
    This section evaluates whether portfolio conclusions remain
    similar under alternative portfolio construction and
    rebalancing approaches.
    """
)

robustness_display = robustness.copy()

for column in [
    "Annual Return",
    "Annual Volatility",
    "Maximum Drawdown"
]:

    robustness_display[column] = (
        robustness_display[column] * 100
    ).round(2)

robustness_display["Sharpe Ratio"] = (
    robustness_display["Sharpe Ratio"]
).round(2)

st.dataframe(
    robustness_display,
    use_container_width=True
)


# ============================================================
# SECTION 8 — ROBUSTNESS SHARPE COMPARISON
# ============================================================

fig = px.bar(
    robustness_display.reset_index(),
    x="index",
    y="Sharpe Ratio",
    title="Sharpe Ratio Across Robustness Strategies"
)

fig.update_layout(
    xaxis_title="Strategy",
    yaxis_title="Sharpe Ratio"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SECTION 9 — CUMULATIVE WEALTH
# ============================================================

st.header("Cumulative Wealth")

wealth_plot = wealth.copy()

fig = go.Figure()

for column in wealth_plot.columns:

    fig.add_trace(
        go.Scatter(
            x=wealth_plot.index,
            y=wealth_plot[column],
            mode="lines",
            name=column
        )
    )

fig.update_layout(
    title="Growth of ₹1 Under Alternative Strategies",
    xaxis_title="Date",
    yaxis_title="Portfolio Value"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SECTION 10 — RISK-FREE RATE SENSITIVITY
# ============================================================

st.header("Risk-Free Rate Sensitivity")

rf_data = risk_free_sensitivity.copy()

fig = go.Figure()

for portfolio in rf_data.columns:

    fig.add_trace(
        go.Scatter(
            x=rf_data.index,
            y=rf_data[portfolio],
            mode="lines+markers",
            name=portfolio
        )
    )

fig.update_layout(
    title="Sharpe Ratio Sensitivity to Risk-Free Rate",
    xaxis_title="Risk-Free Rate",
    yaxis_title="Sharpe Ratio"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SECTION 11 — RESEARCH FINDINGS
# ============================================================

st.header("Research Findings")

best_return = performance[
    "Annual Return"
].idxmax()

best_sharpe = performance[
    "Sharpe Ratio"
].idxmax()

lowest_volatility = performance[
    "Annual Volatility"
].idxmin()

best_drawdown = performance[
    "Maximum Drawdown"
].idxmax()


st.markdown(
    f"""
    ### Key Findings

    **Highest realized annual return:**  
    {best_return} — {performance.loc[best_return, "Annual Return"]:.2%}

    **Highest realized Sharpe ratio:**  
    {best_sharpe} — {performance.loc[best_sharpe, "Sharpe Ratio"]:.2f}

    **Lowest realized volatility:**  
    {lowest_volatility} — {performance.loc[lowest_volatility, "Annual Volatility"]:.2%}

    **Smallest maximum drawdown:**  
    {best_drawdown} — {performance.loc[best_drawdown, "Maximum Drawdown"]:.2%}
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Portfolio Optimization & Backtesting of Indian Equities | "
    "Modern Portfolio Theory | 2015–2025"
)