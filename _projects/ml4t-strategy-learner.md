---
title: "Strategy Learner for Algorithmic Trading"
description: "Designed and backtested two equity trading strategies — one built by hand from technical indicators, one learned from historical data — then systematically dismantled both under varying market friction to understand what drives their behavior."
layout: project
---

## Abstract

This project designs, trains, and evaluates two equity trading strategies: a hand-crafted rule-based system using classical technical indicators (Bollinger Bands, RSI, Price/SMA Ratio) and a machine-learned classifier trained on historical return data. Both strategies are assessed on in-sample (2008–2009) and out-of-sample (2010) periods using cumulative return and Sharpe ratio, with a market impact sensitivity analysis as the primary experimental lever. The central finding is that the learned strategy's advantage over the manual baseline is real under low-friction conditions but erodes measurably as transaction costs increase — establishing that the performance edge is conditional on market microstructure rather than absolute.

## The Big Idea (No Math Required)

Imagine you're trying to decide when to buy and sell a stock. You could do it two ways:

1. **By hand**: Study charts, read books about technical analysis, and write down explicit rules — "if the price drops below its 20-day average AND volume is rising, buy."
2. **Let a machine figure it out**: Feed the computer years of historical prices and returns, and let it discover patterns you might never think to look for.

This project did both, then asked the harder question: *which one actually works, and why does it appear to work?*

It turns out that almost any strategy can look brilliant on historical data if you stare at it long enough — that's called **overfitting**, and it's the central hazard of quantitative trading. The real test is whether the strategy's apparent edge survives realistic market conditions: transaction costs, slippage, and the fact that every trade you make slightly moves the price against you.

Both strategies were evaluated under a systematic range of those realistic constraints. The result: the machine-learned strategy was more adaptive in volatile markets, but both strategies degraded gracefully (and in revealing ways) as market friction increased. Understanding *why* the edge eroded — and where it didn't — is the whole point.

## The Central Question of Quantitative Finance

Every trading strategy carries an implicit theory about the market: that prices are predictable, that certain signals carry information about future returns, that there is an edge to be found if you look in the right place. The hard part is not finding a strategy that appears to work on historical data. The hard part is knowing *why* it appears to work and whether that reason will hold in the future.

This project, completed in [CS 7646: Machine Learning for Trading](https://omscs.gatech.edu/cs-7646-machine-learning-trading) at Georgia Tech, was a rigorous examination of exactly that question. I built two strategies — one hand-crafted from classical technical analysis, one learned from historical returns using a supervised model — and then evaluated both under multiple experimental conditions designed to expose where each strategy's apparent advantage lived and where it vanished.

## The Benchmark: A Manual Rule-Based Strategy

Before teaching a model anything, I built a strategy by hand. This is a discipline as much as a step: a manual strategy forces you to articulate *why* you expect a given signal to predict future returns. It serves as an interpretable baseline that the machine must beat on its own terms.

### Technical Indicators

The manual strategy used three classical technical indicators as signals.

**Bollinger Bands** measure where the current price sits relative to a rolling mean and standard deviation. If the price at time $t$ is $P_t$, the middle band is a 20-day simple moving average $\text{SMA}_{20}$, and the upper and lower bands are:

$$\text{Upper}(t) = \text{SMA}_{20}(t) + 2\sigma_{20}(t), \qquad \text{Lower}(t) = \text{SMA}_{20}(t) - 2\sigma_{20}(t)$$

The Bollinger Band percentage indicator, $\%B$, normalizes price position within the bands:

$$\%B(t) = \frac{P_t - \text{Lower}(t)}{\text{Upper}(t) - \text{Lower}(t)}$$

Values near zero suggest the price is near its lower band — a potential reversal signal for mean-reversion strategies. Values near one suggest the price is near its upper band.

**Relative Strength Index (RSI)** measures the magnitude of recent gains versus recent losses over a window of $n$ days:

$$\text{RSI}(t) = 100 - \frac{100}{1 + \frac{\text{avg gain}_{n}(t)}{\text{avg loss}_{n}(t)}}$$

Values above 70 are conventionally interpreted as "overbought" (potential sell signal); values below 30 as "oversold" (potential buy signal). The RSI is designed to capture momentum and its potential exhaustion.

**Price/SMA Ratio** simply measures how far the current price has deviated from its rolling mean — a momentum and reversion signal that complements the Bollinger Band structure.

### Trading Logic

The manual strategy entered long positions when multiple indicators aligned on a bullish signal, exited or went short when they aligned on a bearish signal, and held otherwise. Position sizing was fixed at 1000 shares long or short. Commission and market impact were explicitly modeled.

This strategy is interpretable, auditable, and grounded in a century of technical analysis tradition. It also has a structural weakness: its rules are fixed. They do not adapt to changing market regimes, to asset-specific behavior, or to the fact that technical signals that worked in one decade may not work in the next.

## The Learned Strategy

The learned strategy replaced fixed rules with a supervised model trained on historical data. The model was given the same technical indicators as input features — alongside engineered lags and cross-indicator interactions — and asked to predict whether the stock would yield a positive return over the next $N$ trading days.

The learning objective was:

$$\hat{y}_t = f(\%B_t, \text{RSI}_t, \text{PrSMA}_t, \text{lagged features})$$

where $\hat{y}_t \in \{+1, -1\}$ indicates a buy or sell signal for the next holding period. The model was trained entirely on in-sample data (2008–2009) and evaluated on a separate out-of-sample period (2010) to assess generalization.

The key design choices:

- **In-sample training only**: the model could not see out-of-sample data during any part of training or hyperparameter selection
- **Lookahead labeling**: training labels were generated by looking forward $N$ days at actual returns — a common practice in supervised trading that requires careful handling to avoid leakage
- **Discrete signals**: rather than predicting a continuous return, the model output was a buy/hold/sell decision, making its actions directly comparable to the manual strategy

## Performance Measurement

Two metrics anchored the evaluation.

**Cumulative Return** is the simplest measure of a strategy's absolute performance:

$$\text{CumReturn}(T) = \frac{P_T - P_0}{P_0}$$

where $P_0$ is the portfolio value at the start of the evaluation period and $P_T$ is its value at time $T$. This metric answers the first-order question — did the strategy make money? — but says nothing about how much risk was taken to earn that return.

**Sharpe Ratio** measures risk-adjusted return. For a strategy with daily returns $r_1, r_2, \ldots, r_T$ and risk-free rate $r_f$ (approximated as zero for simplicity):

$$\text{Sharpe} = \frac{\sqrt{252} \cdot \mathbb{E}[r_t - r_f]}{\text{std}(r_t - r_f)}$$

The factor $\sqrt{252}$ annualizes the ratio assuming 252 trading days per year. A Sharpe ratio above 1.0 is generally considered acceptable; above 2.0 is strong. The ratio rewards strategies that earn returns with low volatility and penalizes strategies that earn the same returns through wild swings.

Both metrics were evaluated separately for in-sample and out-of-sample periods, because a strategy that appears excellent in-sample but collapses out-of-sample has learned the training data rather than the market.

## Experiment 1: In-Sample vs. Out-of-Sample

The first experiment compared both strategies across the in-sample training period and the held-out test period. The learned strategy's superior in-sample performance was expected — it was trained on that data. The scientifically interesting question was whether the performance advantage persisted out-of-sample.

The result was instructive: the learned strategy maintained a measurable advantage in out-of-sample cumulative return and Sharpe ratio compared to the manual strategy, but the advantage narrowed. The compression of the performance gap between in-sample and out-of-sample periods is a diagnostic for overfitting. A large gap suggests the model memorized rather than generalized. A modest gap suggests genuine learning.

The manual strategy showed a more stable in-sample/out-of-sample relationship, consistent with its fixed rules — it neither improved in-sample nor degraded out-of-sample in the same way as the learned model. This is the characteristic behavior of a rule-based system: consistent, but limited in its ability to adapt.

## Experiment 2: Market Impact Sensitivity

The second experiment was the more revealing one. Market *impact* models the cost of executing a trade: when you buy a large position, your order moves the price against you, and when you sell, you move it down. The impact parameter $\lambda$ scales this effect:

$$\text{effective price (buy)} = P_t \cdot (1 + \lambda), \qquad \text{effective price (sell)} = P_t \cdot (1 - \lambda)$$

The experiment varied $\lambda$ from 0.001 (minimal friction) to 0.009 (high friction) and recorded the performance of both strategies at each setting.

The key finding was asymmetric sensitivity. The manual strategy's performance degraded approximately linearly with impact — each trade cost more, and the strategy made fewer profitable trades, but the relationship was predictable. The learned strategy's performance was more sensitive: at low impact settings, it achieved higher returns by executing more frequent, opportunistic trades; at high impact settings, its performance degraded faster than the manual strategy because those frequent trades became expensive.

This is a fundamental insight about high-frequency trading strategies: their edge often lives in the transaction cost regime. The alpha — the excess return — that a learned strategy identifies may be real, but if it requires many small trades to capture, it can be entirely consumed by friction. A strategy that appears promising in a zero-impact simulation may be unprofitable in live trading.

## Key Findings

### Finding 1: The Learned Strategy Outperformed in Low-Impact Conditions

At low market impact, the learned strategy achieved higher cumulative returns and a better Sharpe ratio than the manual strategy, both in-sample and out-of-sample. This is the result that justifies the machine learning investment: the model found patterns in the technical indicator space that human-designed rules did not fully capture.

### Finding 2: Sensitivity Analysis Was More Informative Than Single-Run Results

Single-point performance comparisons are almost always misleading in trading research. The impact sensitivity experiment revealed that the learned strategy's advantage was conditional — real and meaningful at low friction, but eroding or reversing at higher friction. A portfolio report that presented only the low-impact result would create a false impression of robustness.

### Finding 3: In-Sample/Out-of-Sample Gap Quantifies Overfitting Risk

The performance gap between in-sample and out-of-sample periods was larger for the learned strategy than for the manual strategy, as expected. The magnitude of this gap is a practical risk signal. A small gap is encouraging; a large gap demands investigation into whether the model is learning genuine regularities or fitting noise.

### Finding 4: Technical Indicators Carry Real but Noisy Signal

Both strategies relied on the same technical indicators and both achieved positive out-of-sample returns, confirming that the indicators carry genuine predictive information about near-term price direction. But neither strategy's out-of-sample performance matched its in-sample performance, confirming that the signal is noisy and regime-dependent. This is consistent with the efficient market hypothesis under its weaker forms: excess returns are possible but not guaranteed, and their sources erode as they become widely known and traded.

## Why This Work Matters

Algorithmic trading is a difficult ML setting: the data is noisy, regimes shift, and seemingly strong backtests can fail in deployment. The point of this project was not to claim a universally superior strategy. The point was to isolate when performance appears, when it vanishes, and why.

The most transferable lessons were:

- **Principled baseline design**: building an interpretable manual strategy before training a model
- **Rigorous experimental comparison**: evaluating both strategies under identical conditions
- **Sensitivity analysis as a core method**: market impact variation as the key experimental lever
- **Risk-aware performance evaluation**: Sharpe ratio alongside cumulative return
- **Scientific honesty**: reporting the conditions under which the learned strategy's advantage disappears

The methodology is not specific to trading. The pattern — build a baseline, train a learner, compare under varied conditions, diagnose where the advantage lives — applies to any ML application where deployment conditions differ from training conditions.

## Artifacts and Provenance

- Course: [CS 7646: Machine Learning for Trading](https://omscs.gatech.edu/cs-7646-machine-learning-trading)

{% comment %}
Internal references (hidden from rendered page):
- OMSCS path: ML4T/P8/
- Experiment scripts: ML4T/P8/experiment1.py and ML4T/P8/experiment2.py
- Report: ML4T/P8/report.pdf
{% endcomment %}

## Summary

I built a rule-based trading strategy from technical indicators, then trained a machine learning model on historical stock data to learn a better strategy. The learned strategy outperformed the manual one — but only under low-friction conditions. When I simulated realistic market impact, the advantage eroded. The most important finding was not which strategy won, but under *what conditions* each strategy was better.

That conditional framing — knowing when an advantage is real and when it depends on assumptions — is the primary scientific contribution.

## Policy Note

This page intentionally excludes code and implementation specifics. Only high-level methods and evaluation outcomes are presented.
