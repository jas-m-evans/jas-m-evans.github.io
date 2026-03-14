---
title: "Strategy Learner for Algorithmic Trading"
description: "Compared a rule-based trading strategy and a learned strategy under varying market impact, using quantitative backtesting analysis."
layout: project
image: "/assets/images/projects/ml4t-p8-experiment1.png"
---

## Overview

In this ML4T project, I built and evaluated two equity trading approaches on historical market data: a manual indicator-based strategy and a learned strategy. The goal was to test whether machine learning could outperform hand-crafted rules under realistic friction settings.

![Strategy learner experiment chart](/assets/images/projects/ml4t-p8-experiment1.png)

## Research Focus

- Can a learned policy consistently outperform a manual baseline?
- How sensitive are outcomes to market impact assumptions?
- What does robustness look like across in-sample and out-of-sample tests?

## Approach

- Developed a manual strategy using technical indicators
- Trained a strategy learner and evaluated portfolio trajectories
- Ran sensitivity tests at multiple impact values (for example 0.001 to 0.009)
- Compared cumulative return, risk-adjusted performance, and behavior under volatility

## Key Findings

- Learned strategies improved adaptability in volatile periods relative to static rule logic.
- Market impact assumptions materially changed strategy behavior and final return.
- The strongest insight came from sensitivity analysis, not single-run performance.

## Additional Visuals

![Impact sensitivity result](/assets/images/projects/ml4t-p8-experiment2-1.png)

![Manual strategy baseline](/assets/images/projects/ml4t-p8-manualstrategy1.png)

## Artifacts

- Course: CS7646 Machine Learning for Trading
- OMSCS path: ML4T/P8/
- Experiment scripts: ML4T/P8/experiment1.py and ML4T/P8/experiment2.py
- Report: ML4T/P8/report.pdf

## Policy Note

This page intentionally excludes code and implementation specifics. Only high-level methods and evaluation outcomes are presented.
