# portfolio-optimization-india
# Portfolio Optimization & Backtesting of Indian Equities

### Modern Portfolio Theory · Quantitative Finance · Out-of-Sample Backtesting

> **Can a quantitatively optimized portfolio of Indian equities outperform a simple benchmark on a risk-adjusted basis when evaluated on unseen data?**

This project applies **Modern Portfolio Theory (MPT)** and constrained portfolio optimization to a diversified universe of **20 major Indian equities**. The analysis progresses from individual stock return and risk estimation, through covariance analysis and efficient-frontier construction, to **out-of-sample backtesting** against the Nifty 50.

Unlike a purely theoretical optimization exercise, this project explicitly separates the data into **training and testing periods**, so that portfolios optimized on historical information are evaluated on data the optimizer never saw.

---

## Live Dashboard

**Interactive Streamlit Dashboard:** `[Add your deployed Streamlit URL here]`

The dashboard lets you explore:

- Portfolio performance and risk-return characteristics
- Stock-level and sector-level allocations
- The efficient frontier and randomly simulated portfolios
- Out-of-sample wealth growth
- Robustness and risk-free-rate sensitivity analysis
- Portfolio concentration

---

## Project Overview

Portfolio optimization is fundamentally a trade-off between **expected return and risk**. The goal is not to pick the assets with the highest historical returns, but to understand how assets interact through their **covariance and correlation structure**, and to build portfolios that use that structure efficiently.

This project investigates three portfolio construction strategies:

1. **Equal Weight Portfolio**
2. **Minimum Variance Portfolio**
3. **Maximum Sharpe Ratio Portfolio**

Each is evaluated against the **Nifty 50 benchmark** over an out-of-sample period, combining:

- Financial data analysis
- Statistical risk measurement
- Modern Portfolio Theory
- Constrained numerical optimization
- Efficient-frontier construction
- Portfolio backtesting
- Risk-adjusted performance evaluation
- Robustness and sensitivity analysis
- Interactive financial visualization

---

## Research Question

> **Can a quantitatively optimized portfolio of Indian equities outperform a simple benchmark on a risk-adjusted basis when evaluated on unseen data?**

Optimization is performed using **2015–2022 data**, while portfolio performance is evaluated independently using **2023–2025 data**. This reduces look-ahead bias and gives a more realistic sense of whether historical optimization actually translates into future performance.

---

## Methodology

### 1. Equity Universe

Twenty established Indian equities spanning multiple sectors of the economy:

| Company | Ticker | Sector |
|---|---|---|
| Reliance Industries | `RELIANCE.NS` | Energy |
| HDFC Bank | `HDFCBANK.NS` | Financials |
| ICICI Bank | `ICICIBANK.NS` | Financials |
| State Bank of India | `SBIN.NS` | Financials |
| Kotak Mahindra Bank | `KOTAKBANK.NS` | Financials |
| Tata Consultancy Services | `TCS.NS` | IT |
| Infosys | `INFY.NS` | IT |
| ITC | `ITC.NS` | FMCG |
| Hindustan Unilever | `HINDUNILVR.NS` | FMCG |
| Sun Pharmaceutical | `SUNPHARMA.NS` | Healthcare |
| Bharti Airtel | `BHARTIARTL.NS` | Telecom |
| Larsen & Toubro | `LT.NS` | Industrials |
| Mahindra & Mahindra | `M&M.NS` | Automobiles |
| Maruti Suzuki | `MARUTI.NS` | Automobiles |
| Asian Paints | `ASIANPAINT.NS` | Consumer / Materials |
| UltraTech Cement | `ULTRACEMCO.NS` | Construction Materials |
| NTPC | `NTPC.NS` | Power |
| Power Grid Corporation | `POWERGRID.NS` | Power |
| Tata Steel | `TATASTEEL.NS` | Metals |
| Hindalco Industries | `HINDALCO.NS` | Metals |

The universe was chosen to provide exposure across major segments of the Indian equity market while keeping the asset universe manageable for optimization.

### 2. Data

Historical daily adjusted prices are sourced from **Yahoo Finance** via `yfinance`.

**Study period:** 2015–2025, split into:

```
2015–2022  →  Training / Optimization Period
              (estimate returns, estimate covariance, optimize weights)

2023–2025  →  Out-of-Sample Testing Period
              (apply frozen weights, evaluate realized performance)
```

The separation between optimization and evaluation is central to the project.

### 3. Return Estimation

Daily returns:

$$
R_t = \frac{P_t}{P_{t-1}} - 1
$$

Annualized expected return, from the mean daily return:

$$
E(R_{annual}) = (1+\bar{R}_{daily})^{252}-1
$$

(252 ≈ trading days per year)

### 4. Risk Measurement

Daily volatility:

$$
\sigma_i = \sqrt{Var(R_i)}
$$

Annualized volatility:

$$
\sigma_{annual} = \sigma_{daily}\sqrt{252}
$$

The **covariance matrix** and **correlation matrix** across all 20 stocks are also computed, forming the basis for diversification analysis.

### 5. Modern Portfolio Theory

For a portfolio with weight vector \(w\):

**Expected Return:** $E(R_p)=w^T\mu$

**Variance:** $\sigma_p^2=w^T\Sigma w$

**Volatility:** $\sigma_p=\sqrt{w^T\Sigma w}$

where \(\mu\) is the vector of expected returns and \(\Sigma\) is the covariance matrix.

### 6. Sharpe Ratio

$$
Sharpe=\frac{R_p-R_f}{\sigma_p}
$$

The primary analysis uses a **6% annual risk-free rate**, with sensitivity analysis at **4%, 6%, and 8%**.

### 7. Portfolio Optimization

**Equal Weight** — every stock gets $w_i = 1/N$ (5% each for 20 stocks).

**Minimum Variance:**

$$
\min_w \; w^T\Sigma w \quad \text{s.t.} \quad \sum_i w_i = 1, \;\; 0 \leq w_i \leq 0.25
$$

**Maximum Sharpe Ratio:**

$$
\max_w \; \frac{w^T\mu-R_f}{\sqrt{w^T\Sigma w}} \quad \text{s.t.} \quad \sum_i w_i = 1, \;\; 0 \leq w_i \leq 0.25
$$

Short selling is not permitted, and no single stock may exceed 25% of the portfolio. Optimization uses **Sequential Least Squares Programming (SLSQP)**.

### 8. Efficient Frontier

The frontier is built by solving a sequence of minimum-variance problems across target return levels, mapping the relationship between expected return and portfolio risk. Thousands of randomly weighted portfolios are also simulated to visualize the broader feasible risk-return space.

### 9. Backtesting Framework

**Training period (2015–2022):** estimate returns, estimate covariance, optimize weights.

**Testing period (2023–2025):** apply the frozen weights and measure realized returns, volatility, Sharpe ratio, and maximum drawdown against the Nifty 50 — a genuine out-of-sample evaluation rather than an in-sample fit.

---

## Results

*Based on the 2023–2025 out-of-sample testing period.*

| Strategy | Annual Return | Annual Volatility | Sharpe Ratio | Max Drawdown |
|---|---:|---:|---:|---:|
| Minimum Variance | 12.43% | 11.14% | 0.58 | -20.62% |
| Maximum Sharpe | 8.28% | 12.48% | 0.18 | -22.65% |
| **Equal Weight** | **19.30%** | 11.95% | **1.11** | **-16.13%** |
| Nifty 50 | 13.13% | 12.02% | 0.59 | **-15.77%** |

---

## Key Findings

**1. Equal Weight outperformed the optimized portfolios out-of-sample.**
Equal Weight returned 19.30% annually, ahead of Minimum Variance (12.43%), Maximum Sharpe (8.28%), and the Nifty 50 (13.13%) — a reminder that an optimized portfolio doesn't automatically beat simple diversification on unseen data.

**2. Equal Weight also produced the strongest realized Sharpe ratio.**
1.11, versus 0.58 (Minimum Variance), 0.18 (Maximum Sharpe), and 0.59 (Nifty 50) — the best realized risk-adjusted performance of the group.

**3. Minimum Variance achieved the lowest volatility (11.14%),** as designed — but lower volatility didn't translate into the highest return.

**4. Maximum Sharpe did not remain optimal out-of-sample,** realizing a Sharpe ratio of only 0.18 despite being explicitly optimized for that metric in-sample. This is a meaningful result, not a methodology failure — it highlights the sensitivity of mean-variance optimization to expected-return estimation, covariance estimation, regime shifts, and parameter instability.

**5. The Nifty 50 had the smallest maximum drawdown (-15.77%),** the shallowest peak-to-trough decline of any strategy tested.

---

## Robustness Analysis

To check whether the headline results depend on a single optimization setup, several additional tests were run:

- **Quarterly rebalancing** — weights recalculated periodically using trailing estimation windows, to test stability under periodic re-optimization.
- **Risk parity** — a portfolio equalizing risk contributions rather than capital allocations: $RC_i = w_i \frac{(\Sigma w)_i}{\sigma_p}$
- **Risk-free rate sensitivity** — the Maximum Sharpe optimization re-run at 4%, 6%, and 8% risk-free rates.
- **Weight stability** — quarterly Maximum Sharpe weights examined for stability versus significant reallocation over time, as a lens on parameter sensitivity and concentration risk.

---

## Technology Stack

| Category | Tools |
|---|---|
| Language | Python |
| Financial Data | `yfinance` |
| Data Analysis | `pandas`, `numpy` |
| Optimization | `scipy.optimize` |
| Visualization | `matplotlib`, `seaborn`, `plotly` |
| Dashboard | `Streamlit` |
| Environment | Jupyter Notebook, Git / GitHub |

---

## Project Structure

```
portfolio-optimization-india/
│
├── dashboard.py
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── data/
│   ├── adjusted_prices.csv
│   ├── daily_returns.csv
│   ├── risk_return_summary.csv
│   ├── correlation_matrix.csv
│   ├── covariance_matrix.csv
│   ├── annualized_covariance_matrix.csv
│   ├── random_portfolios.pkl
│   ├── optimized_portfolio_weights.csv
│   ├── efficient_frontier.csv
│   ├── performance_table.csv
│   ├── sector_weights.csv
│   ├── robustness_performance_table.csv
│   ├── risk_free_sensitivity.csv
│   ├── robustness_wealth_paths.csv
│   └── quarterly_max_sharpe_weights.csv
│
└── notebooks/
    ├── 01_data_collection.ipynb
    ├── 02_returns_risk.ipynb
    ├── 03_mpt.ipynb
    ├── 04_optimization.ipynb
    ├── 05_backtesting.ipynb
    ├── 06_efficient_frontier.ipynb
    ├── 07_results_analysis.ipynb
    └── 08_robustness_analysis.ipynb
```

---

## Notebook Workflow

| Notebook | Objective |
|---|---|
| `01_data_collection` | Collect and prepare historical equity prices |
| `02_returns_risk` | Calculate returns, variance, volatility, covariance, and correlation |
| `03_mpt` | Apply Modern Portfolio Theory to portfolio construction |
| `04_optimization` | Generate random portfolios and perform optimization |
| `05_backtesting` | Conduct out-of-sample portfolio evaluation |
| `06_efficient_frontier` | Construct and visualize the efficient frontier |
| `07_results_analysis` | Compare performance, allocation, and concentration |
| `08_robustness_analysis` | Test rebalancing, risk parity, and parameter sensitivity |

---

## Installation

```bash
git clone https://github.com/YOUR-USERNAME/portfolio-optimization-india.git
cd portfolio-optimization-india
pip install -r requirements.txt
```

## Running the Dashboard

```bash
streamlit run dashboard.py
```

## Reproducing the Analysis

Run the notebooks sequentially:

```
01_data_collection → 02_returns_risk → 03_mpt → 04_optimization →
05_backtesting → 06_efficient_frontier → 07_results_analysis → 08_robustness_analysis
```

Each notebook generates intermediate datasets consumed by later notebooks and the dashboard.

---

## Key Assumptions

- No short selling
- Maximum allocation of 25% to any individual stock
- Portfolio weights sum to 100%
- ~252 trading days per year
- Primary risk-free rate assumption of 6%
- Expected returns and covariance are estimated from historical data
- Transaction costs and taxes are not incorporated
- Optimization uses only information available during the training period
- Portfolio weights are frozen for the primary 2023–2025 out-of-sample evaluation

---

## Limitations

Mean-variance optimization is highly sensitive to its inputs — small changes in expected-return assumptions can produce large changes in optimized weights. Other limitations:

- Historical performance does not guarantee future performance
- Covariance relationships may shift over time
- Transaction costs, market impact, taxes, and brokerage fees are not modeled
- Liquidity constraints beyond the 25% weight cap are not modeled
- No alternative assets (bonds, gold, international equities) are included
- The Nifty 50 is a broad benchmark, not a portfolio built from the same 20-stock universe

These limitations are especially relevant when interpreting the Maximum Sharpe results.

---

## Why the Out-of-Sample Result Matters

A central lesson of this project: **optimizing on historical data does not guarantee superior future performance.** The Maximum Sharpe portfolio was built specifically to maximize the in-sample Sharpe ratio, yet its realized out-of-sample performance was substantially weaker than the simple Equal Weight portfolio.

This underscores the importance of **out-of-sample testing over in-sample optimization alone**, and a broader point in quantitative finance: added model complexity doesn't automatically translate into better investment outcomes. A simple diversification rule can outperform a theoretically "optimal" strategy when that strategy is sensitive to estimation error.

---

## Future Improvements

- Black-Litterman portfolio optimization
- Shrinkage covariance estimation
- Robust portfolio optimization
- Conditional Value-at-Risk (CVaR) optimization
- Downside-risk optimization
- Transaction-cost and turnover modeling
- Rolling-window optimization
- Regime-dependent portfolio allocation
- Factor-based portfolio construction (Fama-French)
- Incorporating bonds and gold
- Additional Indian benchmark comparisons
- Machine-learning-based return forecasting
- Live portfolio monitoring

---

## Disclaimer

This project is for **educational, research, and quantitative-finance portfolio demonstration purposes only**. Results are based on historical market data and model assumptions, and do not constitute investment advice or a recommendation to buy or sell any security. Past performance does not guarantee future results.

---

## Author

**Anjali Arya**
Quantitative Finance · Financial Analytics · Data Science

Developed to explore the application of statistical modeling, portfolio theory, numerical optimization, and empirical backtesting to Indian equity markets.

---

## License

Licensed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
