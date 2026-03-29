---
title: "Unsupervised Learning and Dimensionality Reduction"
description: "A comparative study of clustering and dimensionality reduction across real datasets, with metric-driven evaluation and runtime profiling."
layout: project
---

## The Problem: Structure Without Labels

Supervised learning gets clear instructions. Unsupervised learning gets silence.

No target labels. No direct objective tied to business outcomes. Just raw feature space and a question: *is there meaningful structure here, or am I seeing patterns that are not real?*

This project from [CS 7641: Machine Learning](https://omscs.gatech.edu/cs-7641-machine-learning) explores that question through clustering and dimensionality reduction across multiple datasets.

The heart of the work is not model tuning for a single score. It is method selection under ambiguity.

## Research Questions

- When does K-Means beat EM, and when does EM beat K-Means?
- Which reduction method keeps useful signal while shrinking the feature space?
- How often do quality metrics disagree with runtime reality?
- Can we turn these experiments into a repeatable decision process?

## Experimental Design

I compared methods in a controlled pipeline:

- Clustering: K-Means and Gaussian Mixture Models (EM)
- Dimensionality reduction: PCA, ICA, Random Projection, feature selection
- Evaluation metrics: Silhouette score, Davies-Bouldin score, and wall-clock time
- Cross-dataset validation: test whether conclusions transfer or collapse

This made it easier to separate true algorithm behavior from dataset-specific noise.

Dataset context from the original assignment artifacts:

- Wine dataset: 1,599 rows, 12 attributes (binary target transformation in the assignment workflow)
- Adult Census dataset: 32,561 rows, 15 attributes with encoded categorical variables

## Why Clustering Is Fascinating

Clustering is often presented as a one-click preprocessing step. In practice, it is deeply geometric.

- K-Means assumes roughly spherical, equally scaled clusters and can perform beautifully when that assumption is close to true.
- EM is softer and probabilistic, which helps when real clusters overlap or have different covariance structures.

The interesting result was not that one model always won. The interesting result was that **the winner changed with data geometry**. That shift is exactly why unsupervised model selection needs evidence, not habit.

## Why PCA Stood Out

PCA consistently delivered the strongest first-pass reduction in this project.

- It provided compact representations that were easy to reason about.
- It preserved enough variance to support downstream clustering quality.
- It improved iteration speed without immediately destroying structure.

ICA and random projection still had value, especially for specific constraints, but PCA was the most reliable default when balancing interpretability, stability, and performance.

## Evidence From My OMSCS Artifacts

The points above are based on my original outputs in `ML/A3/log.txt` and `ML/A3/bak.txt`, not only portfolio-level summaries.

Selected examples:

- Wine + K-Means + PCA at k=2: Silhouette 0.6082, Davies-Bouldin 0.6073, time 0.0732s
- Wine + K-Means + ICA best case (k=3): Silhouette 0.0776, Davies-Bouldin 3.8938, time 0.0514s
- Wine + EM + PCA at k=2: Silhouette 0.5054, Davies-Bouldin 0.7088, time 0.0580s
- Census + K-Means + PCA at k=2: Silhouette 0.5846, Davies-Bouldin 0.6088, time 0.0690s
- Census + EM + PCA at k=2: Silhouette 0.6066, Davies-Bouldin 0.5434, time 0.0966s
- Census + EM + ICA best case (k=7): Silhouette 0.4569, Davies-Bouldin 1.7561, time 0.2043s

One practical pattern repeated throughout the experiments: the strongest quality settings were usually at small k, often k=2, and quality dropped as k increased while runtime climbed.

## Selected Visuals

I kept a small set of figures that directly support the main story.

### 1) Cluster geometry on Wine

![Wine K-Means clusters](/assets/images/projects/wine_kmeans_clusters.jpg)

![Wine EM clusters](/assets/images/projects/wine_em_clusters.jpg)

These two plots show why comparing K-Means and EM is not optional. They respond differently to overlap and shape, even on the same dataset.

### 2) PCA structure signal on Wine

![Wine PCA loading plot](/assets/images/projects/pca_loading_wine.jpg)

This loading plot supports the case for PCA as an effective first reduction pass: major structure is captured early, which helped downstream clustering stability.

## Key Findings

- Algorithm ranking changed by dataset, so fixed preferences were fragile.
- Better reduction did not always mean better clustering, which exposed interaction effects between preprocessing and cluster geometry.
- Runtime profiling changed final recommendations in several cases where metric differences were small.
- Reconstruction behavior was a useful warning signal: when information loss rose too quickly, cluster quality usually degraded next.
- On Wine, PCA and RCA repeatedly outperformed ICA for clustering quality.
- On Census, PCA remained a strong baseline while ICA was more sensitive and often slower.

## Practical Playbook From This Project

- Start with PCA as a baseline reduction strategy.
- Compare K-Means and EM early instead of committing to one family.
- Treat internal metrics as directional signals, not absolute truth.
- Use runtime as a first-class criterion when methods are close in quality.
- Re-check conclusions on a second dataset before calling them general.

## Visual Notes

The original assignment included many plots. This portfolio version keeps only a few high-signal visuals and moves the emphasis to interpretation and decision logic.

## Artifacts

- Course: [CS 7641: Machine Learning](https://omscs.gatech.edu/cs-7641-machine-learning)
- OMSCS path: ML/A3/
- Experiment implementation: ML/A3/main.py
- Analysis traces and report draft materials: ML/A3/log.txt and ML/A3/bak.txt
- Full assignment report draft: ML/A3/jevans99-analysis.pdf

## Policy Note

This page shares high-level research outcomes only. Implementation details are kept private to align with course policy.
