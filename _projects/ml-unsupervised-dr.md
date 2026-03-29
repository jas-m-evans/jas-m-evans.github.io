---
title: "Unsupervised Learning and Dimensionality Reduction"
description: "A comparative study of clustering and dimensionality reduction across real datasets, with metric-driven evaluation and runtime profiling."
layout: project
---

## The Problem: Structure Without Labels

Imagine walking into a crowded room where everyone is talking at once, and nobody is wearing a name tag.

That is unsupervised learning.

No labels. No answer key. Just patterns hiding in feature space, and the constant risk of convincing yourself that noise is signal.

This project from [CS 7641: Machine Learning](https://omscs.gatech.edu/cs-7641-machine-learning) asks a hard question: *when data has no labels, how do we decide which structure to trust?*

## Research Questions

- When does K-Means beat EM, and when does EM beat K-Means?
- Which reduction method keeps useful signal while shrinking the feature space?
- How often do quality metrics disagree with runtime reality?
- Can we turn these experiments into a repeatable decision process?

## A Quick Way To Think About It

If clustering is grouping people at a party by conversation style, PCA is dimming the noisy lights so the group shapes become easier to see.

- Clustering says: "Who belongs together?"
- PCA says: "Which directions in this data actually matter most?"

Together, they turn a chaotic high-dimensional dataset into something you can reason about.

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

## Clustering, Taught Quickly

Clustering looks simple until geometry fights back.

- **K-Means** places centroids and pulls points to the nearest center. It is fast and strong when cluster shapes are compact.
- **EM (Gaussian Mixture Models)** models each cluster as a probability distribution. It is more flexible when boundaries are fuzzy and overlap is real.

The key lesson from my runs: there is no permanent champion. The winner changes with data geometry.

## PCA, Taught Quickly

PCA finds the directions where data varies most, then projects data onto those directions.

- In plain terms: PCA keeps the strongest signal and drops weaker directions.
- In practice: this often makes clustering cleaner, faster, or both.
- In this project: PCA was the most reliable first reduction pass across both datasets.

ICA and random projection still had value, especially for specific constraints, but PCA was the most reliable default when balancing interpretability, stability, and performance.

## Evidence From My OMSCS Artifacts

The results below come from my original A3 artifacts (`ML/A3/log.txt`, `ML/A3/bak.txt`, `ML/A3/jevans99-analysis.pdf`).

### Snapshot Table: Four High-Signal Results

| Dataset | Pipeline | Best k | Silhouette | Davies-Bouldin | Time (s) |
| --- | --- | --- | --- | --- | --- |
| Wine | PCA + K-Means | 2 | 0.6082 | 0.6073 | 0.0732 |
| Wine | ICA + K-Means | 3 | 0.0776 | 3.8938 | 0.0514 |
| Census | PCA + K-Means | 2 | 0.5846 | 0.6088 | 0.0690 |
| Census | PCA + EM | 2 | 0.6066 | 0.5434 | 0.0966 |

Why this table matters:

- PCA consistently held strong quality on both datasets.
- ICA could be competitive in narrow cases, but was much less stable in cluster quality.
- Best settings often happened at low k, especially k=2.
- Runtime stayed practical for strong PCA combinations.

One practical pattern repeated throughout the experiments: the strongest quality settings were usually at small k, often k=2, and quality dropped as k increased while runtime climbed.

## Selected Visuals

I kept a small set of figures that directly support the main story.

### 1) Cluster geometry on Wine

![Wine K-Means clusters](/assets/images/projects/wine_kmeans_clusters.jpg)

![Wine EM clusters](/assets/images/projects/wine_em_clusters.jpg)

These two plots tell a useful story fast. K-Means produces tighter geometric partitions, while EM is more comfortable when boundaries blur. Same data, different assumptions, different behavior.

## Key Findings

- Algorithm ranking changed by dataset, so fixed preferences were fragile.
- Better reduction did not always mean better clustering, which exposed interaction effects between preprocessing and cluster geometry.
- Runtime profiling changed final recommendations in several cases where metric differences were small.
- Reconstruction behavior was a useful warning signal: when information loss rose too quickly, cluster quality usually degraded next.
- On Wine, PCA and RCA repeatedly outperformed ICA for clustering quality.
- On Census, PCA remained a strong baseline while ICA was more sensitive and often slower.

## If You Are New To This Topic

Use this simple workflow:

1. Start with PCA to simplify the space.
2. Run both K-Means and EM, do not assume one will win.
3. Compare Silhouette, Davies-Bouldin, and runtime together.
4. Favor solutions that stay strong at small k before scaling complexity.

Unsupervised learning is less about finding one perfect algorithm and more about building confidence that your pattern is real.

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
