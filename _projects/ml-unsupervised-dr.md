---
title: "Unsupervised Learning and Dimensionality Reduction"
description: "A comparative study of clustering and dimensionality reduction across real datasets, with metric-driven evaluation and runtime profiling."
layout: project
---

## Overview

This CS7641 project investigated unsupervised learning quality through a structured comparison of clustering methods and dimensionality reduction techniques. The emphasis was on research process: hypothesis, controlled experiments, metric interpretation, and synthesis.

## Research Focus

- How do K-Means and Expectation Maximization differ in cluster quality across domains?
- Which dimensionality reduction methods preserve structure best for downstream tasks?
- How should quality metrics and runtime be balanced when choosing a method?

## Approach

- Clustering: K-Means and Gaussian Mixture Models (EM)
- Dimensionality reduction: PCA, ICA, Random Projection, feature selection
- Metrics: Silhouette score, Davies-Bouldin score, and wall-clock time
- Cross-dataset evaluation to test stability of conclusions

## Key Findings

- Method ranking changed across datasets, highlighting the importance of context-specific model selection.
- Some reductions improved clustering separability while others mainly improved computational efficiency.
- Runtime analysis surfaced practical trade-offs often missed by metric-only comparisons.

## Artifacts

- Course: CS7641 Machine Learning
- OMSCS path: ML/A3/
- Experiment implementation: ML/A3/main.py
- Analysis traces and report draft materials: ML/A3/log.txt and ML/A3/bak.txt

## Policy Note

This page shares high-level research outcomes only. Implementation details are kept private to align with course policy.
