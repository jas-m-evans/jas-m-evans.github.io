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

### Clustering Analysis

K-Means and Expectation Maximization clustering on the Wine dataset:

![K-Means clustering on Wine dataset](/assets/images/projects/wine_kmeans_clusters.jpg)

![EM clustering on Wine dataset](/assets/images/projects/wine_em_clusters.jpg)

Clustering results on Census data with correlation structure:

![K-Means clustering on Census dataset](/assets/images/projects/census_kmeans_clusters1.jpg)

![EM clustering on Census dataset](/assets/images/projects/census_em_clusters.jpg)

Wine dataset correlation and structure:

![Wine dataset correlation heatmap](/assets/images/projects/wine_heatmap.jpg)

![Wine dataset pairwise relationships](/assets/images/projects/wine_pairplot.jpg)

### Dimensionality Reduction

PCA loadings across datasets reveal which features capture the most variance:

![PCA loadings on Wine](/assets/images/projects/pca_loading_wine.jpg)

![PCA loadings on Census](/assets/images/projects/pca_loading_census.jpg)

ICA identifies independent sources in the data:

![ICA loadings on Wine](/assets/images/projects/ica_loading_wine.jpg)

![ICA loadings on Census](/assets/images/projects/ica_loading_census.jpg)

Random projection and component analysis:

![RCA loadings on Wine](/assets/images/projects/rca_loading_wine.jpg)

![RCA loadings on Census](/assets/images/projects/rca_loading_census.jpg)

### Reconstruction and Convergence

Reconstruction error analysis shows how well each method preserves information:

![Wine reconstruction error](/assets/images/projects/wine_recon_error.jpg)

![Census reconstruction error](/assets/images/projects/census_recon_error.jpg)

Training loss and convergence behavior across methods:

![Training loss across methods](/assets/images/projects/loss.jpg)

## Artifacts

- Course: [CS 7641: Machine Learning](https://omscs.gatech.edu/cs-7641-machine-learning)
- OMSCS path: ML/A3/
- Experiment implementation: ML/A3/main.py
- Analysis traces and report draft materials: ML/A3/log.txt and ML/A3/bak.txt

## Policy Note

This page shares high-level research outcomes only. Implementation details are kept private to align with course policy.
