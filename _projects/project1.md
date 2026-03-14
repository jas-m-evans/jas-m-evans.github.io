---
title: "Supervised Learning on Wine and Census Data"
description: "A rigorous comparative study of five supervised learning algorithms with hyperparameter tuning, validation curves, and runtime analysis."
layout: project
---

## Overview

This project was completed in CS7641 (Machine Learning) and focuses on end-to-end experimental design for supervised classification. I compared multiple model families across two datasets, then analyzed performance, generalization, and computational trade-offs.

## Research Focus

- How do different model classes behave under the same evaluation protocol?
- Which models are most robust across different data regimes?
- What accuracy vs. runtime trade-offs matter in practical settings?

## Approach

- Algorithms evaluated: Decision Trees, k-NN, SVM, MLP, Gradient Boosting
- Systematic hyperparameter sweeps and validation curves for each model family
- Learning curves to diagnose underfitting and overfitting
- Runtime benchmarking to compare training/inference cost

## Key Findings

- No single model dominated every scenario; performance depended strongly on feature space and data distribution.
- Tree-based methods provided a strong speed-performance balance for rapid iteration.
- Higher-capacity models delivered gains but required stricter regularization and tuning to avoid overfitting.
- Comparative analysis quality mattered more than raw leaderboard-style metrics.

## Artifacts

- Course: CS7641 Machine Learning
- OMSCS path: `ML/A1/`
- Core implementation: `ML/A1/main.py`
- Writeup guidance and methodology context: `ML/A1/README.txt`

## Policy Note

This page intentionally shares methodology and outcomes only. Source code is kept private to respect course policy and academic integrity constraints.