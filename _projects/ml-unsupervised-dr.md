---
title: "Unsupervised Learning and Dimensionality Reduction"
description: "A comparative study of clustering and dimensionality reduction across real datasets, with metric-driven evaluation and runtime profiling."
layout: project
---

## Overview

This [CS 7641: Machine Learning](https://omscs.gatech.edu/cs-7641-machine-learning) project investigated unsupervised learning quality through a structured comparison of clustering methods and dimensionality reduction techniques. The emphasis was on research process: hypothesis, controlled experiments, metric interpretation, and synthesis.

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

## Visualizations and Analysis

The original assignment produced many diagnostic plots; the portfolio page now shows a smaller set of representative figures and focuses on interpretation.

### 1) Clustering behavior differs by dataset

On Wine, both methods recovered meaningful structure, but they separated classes for different reasons.

![K-Means clustering on Wine dataset](/assets/images/projects/wine_kmeans_clusters.jpg)

![EM clustering on Wine dataset](/assets/images/projects/wine_em_clusters.jpg)

Interpretation:

- K-Means gave cleaner geometric partitions when cluster shape was compact.
- EM handled overlap more gracefully when clusters were not strictly spherical.
- The practical takeaway was to select by data geometry, not by a fixed algorithm preference.

### 2) PCA was most stable for compact summaries

PCA loadings on Wine and Census showed that a relatively small subset of components captured most variance.

![PCA loadings on Wine](/assets/images/projects/pca_loading_wine.jpg)

![PCA loadings on Census](/assets/images/projects/pca_loading_census.jpg)

Interpretation:

- PCA offered the best interpretability-to-performance trade-off for first-pass reduction.
- ICA and random projection were still useful, but less consistent across both datasets.
- In workflow terms: PCA first, then verify alternatives if domain constraints require them.

### 3) Information retention exposed method trade-offs

Reconstruction error provided a direct signal of information loss after reduction.

![Wine reconstruction error](/assets/images/projects/wine_recon_error.jpg)

![Census reconstruction error](/assets/images/projects/census_recon_error.jpg)

Interpretation:

- Lower-dimensional representations on Wine retained structure more reliably than on Census.
- Census required more careful component selection to avoid aggressive information loss.
- This matched clustering behavior: when reconstruction degraded, downstream cluster quality usually degraded as well.

### 4) Convergence profiles matter in real usage

Metric quality alone did not pick a winner; runtime and convergence behavior changed deployment choices.

![Training loss across methods](/assets/images/projects/loss.jpg)

Interpretation:

- Some methods reached acceptable quality quickly and were preferred for iterative analysis cycles.
- Others yielded marginally better scores but at significantly higher runtime cost.
- Final recommendation favored methods that balanced quality and speed for repeatable experimentation.

## Artifacts

- Course: [CS 7641: Machine Learning](https://omscs.gatech.edu/cs-7641-machine-learning)
- OMSCS path: ML/A3/
- Experiment implementation: ML/A3/main.py
- Analysis traces and report draft materials: ML/A3/log.txt and ML/A3/bak.txt

## Policy Note

This page shares high-level research outcomes only. Implementation details are kept private to align with course policy.
