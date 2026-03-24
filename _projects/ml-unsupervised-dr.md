---
title: "Unsupervised Learning and Dimensionality Reduction"
description: "A comparative study of clustering and dimensionality reduction across two real-world datasets — examining when structure exists, how to find it, and what happens when you reduce a high-dimensional space to its essential geometry."
layout: project
image: "/assets/images/projects/unsupervised-overview.svg"
---

## Abstract

This study compares two clustering algorithms (K-Means and Expectation Maximization with Gaussian Mixture Models) and four dimensionality reduction methods (Principal Component Analysis, Independent Component Analysis, random projection, and feature selection) across two structurally contrasting real-world datasets. Cluster quality is evaluated using silhouette scores and Davies-Bouldin indices without ground-truth labels, while computational cost is benchmarked through wall-clock timing. Results demonstrate that algorithm rankings are strongly dataset-dependent, no single method dominates universally, and pairing dimensionality reduction with clustering improves quality in ways that vary systematically with the underlying data geometry — establishing that method selection requires understanding both algorithmic assumptions and data structure.

![Unsupervised learning overview: clustering and dimensionality reduction](/assets/images/projects/unsupervised-overview.svg)

*Two fundamental questions in unsupervised learning: which groups exist in unlabeled data (clustering), and what is the minimal set of dimensions needed to describe its shape (dimensionality reduction)? Visualization adapted from concepts in Bishop (2006) and Murphy (2012).*

> **Image source:** Conceptual framework based on Bishop, C.M. (2006). *Pattern Recognition and Machine Learning*, Ch. 9–12. Springer; and Murphy, K.P. (2012). *Machine Learning: A Probabilistic Perspective*, Ch. 11–12. MIT Press.

## The Big Idea (No Math Required)

Imagine you're handed a box of 10,000 photographs of people — no names, no labels, nothing. Can you sort them into meaningful groups? You might notice that some photos look like they're taken outdoors, some indoors. Some people are wearing formal clothes, some are casual. Without anyone telling you the categories, your brain naturally finds patterns and draws distinctions.

That is exactly what **unsupervised learning** does. There are no labels. No teacher. Just raw data, and the question: *what structure exists here?*

This project explored two techniques for doing exactly that:

**Clustering — "Which groups exist?"**

Like sorting a messy pile of photographs into albums, clustering algorithms group similar data points together. Two methods were compared:

- **K-Means**: Each point belongs to exactly one group. The algorithm finds the group centers (centroids) that minimize the total distance from points to their assigned center. Fast and intuitive, but assumes groups are roughly round.
- **Expectation Maximization (GMM)**: Like K-Means, but more honest about uncertainty — a point near the boundary between two groups gets *partial membership* in both. This is closer to how the real world works.

**Dimensionality Reduction — "What's essential?"**

Most real-world datasets have many features (columns). A lot of those features are redundant or noisy. Dimensionality reduction is like summarizing a 300-page report into a 2-page executive summary — you lose some details, but the key structure is preserved. Two methods:

- **PCA (Principal Component Analysis)**: Finds the directions in which the data varies the most. Rotate and compress to keep only the "important" axes. Like discovering that all those different wine measurements can mostly be explained by two underlying factors.
- **ICA (Independent Component Analysis)**: Separates mixed signals into their independent sources. Imagine two people talking simultaneously in a room — ICA unmixes the overlapping audio to isolate each voice.

The deeper experiment: does reducing the dimensions *before* clustering make the clusters better? The answer depends entirely on the structure of the data — which is precisely what makes the comparison interesting.

## The Problem with Labels

Most of the world's data does not come with answers attached. There are no ground-truth labels on customer behavior, no authoritative tags on the full breadth of genomic sequences, no oracle telling you that these stock movements group into four regimes and not three. Supervised learning, for all its power, requires a teacher. Unsupervised learning asks a more fundamental question: *what structure does the data contain on its own?*

This project, completed in [CS 7641: Machine Learning](https://omscs.gatech.edu/cs-7641-machine-learning) at Georgia Tech, investigated that question through a controlled experiment comparing clustering algorithms and dimensionality reduction techniques across two datasets with very different geometries. The goal was not to achieve any particular score — there is no ground truth in unsupervised learning — but to understand how different methods characterize structure, when they agree, and when they disagree in ways that reveal something real about the data.

## The Two Problems

**Clustering** asks: can this dataset be partitioned into groups of points that are more similar to each other than to points in other groups? The answer depends entirely on what "similar" means, which turns out to be a deep question disguised as a simple one.

**Dimensionality reduction** asks: can this high-dimensional dataset be faithfully represented in a lower-dimensional space? The answer depends on what you mean by "faithfully" — preserve distances, preserve local neighborhoods, preserve statistical independence, preserve variance? Different answers to that question produce fundamentally different reductions.

The two problems interact: a well-chosen dimensionality reduction often improves clustering quality, because it removes noise, decorrelates features, and makes the cluster geometry more visible. Measuring that interaction was a core part of this study.

## Datasets

The study used two datasets chosen for structural contrast. The first had dense continuous features with nonlinear interaction effects. The second had a mix of categorical and continuous inputs, a stronger class signal, and more separable geometry. By holding the method fixed and varying the data, the experiment separated what was true about the algorithm from what was true about the domain.

## Clustering Methods

### K-Means: Variance Minimization

K-Means partitions $n$ points into $k$ clusters by minimizing the total within-cluster sum of squared distances to each cluster centroid:

$$\min_{\{C_j\},\{\boldsymbol{\mu}_j\}} \sum_{j=1}^{k} \sum_{\mathbf{x}_i \in C_j} \|\mathbf{x}_i - \boldsymbol{\mu}_j\|^2$$

The algorithm alternates between two steps until convergence:

1. **Assignment**: assign each point to the cluster with the nearest centroid
2. **Update**: recompute each centroid as the mean of its assigned points

This is guaranteed to converge to a local minimum of the objective, though not necessarily the global minimum. The result depends on initialization, and it is common practice to run K-Means many times with different random starts and keep the solution with the lowest total variance.

The algorithm encodes strong assumptions: clusters are convex, roughly spherical, and of comparable size. When those assumptions are violated — when the true cluster structure is elongated, nested, or unevenly sized — K-Means will partition the data incorrectly regardless of how much data you give it. Visualizing cluster shapes before committing to K-Means is always worth doing.

### Expectation Maximization: Probabilistic Mixture Modeling

Expectation Maximization (EM) for Gaussian Mixture Models (GMMs) extends K-Means in a principled direction. Rather than assigning each point to exactly one cluster, EM models the data as a mixture of $k$ Gaussian distributions and computes a *soft assignment* — the probability that each point belongs to each component. The generative model is:

$$p(\mathbf{x}) = \sum_{j=1}^{k} \pi_j \cdot \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_j, \boldsymbol{\Sigma}_j)$$

where $\pi_j$ is the mixture weight for component $j$, $\boldsymbol{\mu}_j$ is its mean, and $\boldsymbol{\Sigma}_j$ is its covariance matrix. Training maximizes the log-likelihood of the data:

$$\mathcal{L}(\boldsymbol{\theta}) = \sum_{i=1}^{n} \log \sum_{j=1}^{k} \pi_j \cdot \mathcal{N}(\mathbf{x}_i \mid \boldsymbol{\mu}_j, \boldsymbol{\Sigma}_j)$$

The EM algorithm iterates between an **E-step**, which computes the posterior responsibility of each component for each point:

$$r_{ij} = \frac{\pi_j \cdot \mathcal{N}(\mathbf{x}_i \mid \boldsymbol{\mu}_j, \boldsymbol{\Sigma}_j)}{\sum_{l} \pi_l \cdot \mathcal{N}(\mathbf{x}_i \mid \boldsymbol{\mu}_l, \boldsymbol{\Sigma}_l)}$$

and an **M-step**, which updates the parameters using those responsibilities as soft weights.

The key advantage over K-Means is expressiveness: GMMs allow elliptical clusters of different sizes and orientations through the full covariance matrix $\boldsymbol{\Sigma}_j$. They also provide a proper probabilistic model, enabling Bayesian model selection and uncertainty quantification. The cost is computational: fitting full covariance matrices scales as $O(k \cdot d^2)$ per iteration, and numerical stability requires regularization when components become nearly singular.

## Dimensionality Reduction Methods

### Principal Component Analysis

PCA finds the directions in the feature space that explain the most variance. Given a zero-mean data matrix $\mathbf{X} \in \mathbb{R}^{n \times d}$, the covariance matrix is $\boldsymbol{\Sigma} = \frac{1}{n}\mathbf{X}^T\mathbf{X}$. The principal components are its eigenvectors, ordered by eigenvalue:

$$\boldsymbol{\Sigma} \mathbf{v}_k = \lambda_k \mathbf{v}_k, \qquad \lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_d \geq 0$$

Projecting onto the top $r$ eigenvectors yields the $r$-dimensional representation that retains the maximum possible variance. The fraction of variance retained is $\sum_{k=1}^{r} \lambda_k / \sum_{k=1}^{d} \lambda_k$, a diagnostic that tells you how much information the reduced representation preserves.

PCA is linear, deterministic, and computationally efficient. Its limitation is that it maximizes *variance*, not *class separability* or *cluster quality*. High-variance directions may be noise; the directions that matter for the task may have moderate variance. For this reason, PCA is often the right starting point, but not always the right answer.

### Independent Component Analysis

ICA attacks a different problem. Where PCA finds directions of maximum variance, ICA finds directions of maximum *statistical independence*, making it the right tool when the data is a mixture of independent signals and you want to separate them.

The ICA model assumes that the observed data $\mathbf{x}$ is a linear mixture of independent non-Gaussian source components $\mathbf{s}$:

$$\mathbf{x} = \mathbf{A}\mathbf{s}$$

where $\mathbf{A}$ is an unknown mixing matrix. Recovery of $\mathbf{s}$ requires finding an unmixing matrix $\mathbf{W} = \mathbf{A}^{-1}$ such that the components of $\mathbf{W}\mathbf{x}$ are as statistically independent as possible. Independence is measured through *non-Gaussianity* — by the Central Limit Theorem, a sum of independent random variables becomes more Gaussian than any of its components, so maximizing non-Gaussianity in the recovered components is a principled way to estimate the original sources.

For data with genuine independent signal structure — as in audio source separation, neuroimaging, or financial factor analysis — ICA recovers meaningful latent components that PCA cannot. For data without that structure, the components may be less interpretable.

### Random Projection

Random projection is perhaps the most counterintuitive dimensionality reduction method: it projects the data onto a randomly chosen lower-dimensional subspace and simply hopes for the best. Remarkably, the theory says this works.

The Johnson-Lindenstrauss lemma (1984) guarantees that for any set of $n$ points in $\mathbb{R}^d$ and any $\varepsilon \in (0, 1)$, there exists a projection to $r = O(\varepsilon^{-2} \log n)$ dimensions that preserves all pairwise distances within a factor of $(1 \pm \varepsilon)$. The required dimensionality depends only logarithmically on the number of points — not on the original dimensionality $d$.

$$r \geq \frac{4 \ln n}{\varepsilon^2/2 - \varepsilon^3/3}$$

The implication is striking: if you have 10,000 points and are willing to tolerate 10% distortion in pairwise distances, a random projection to about 1,800 dimensions suffices regardless of whether the original space was 10,000 dimensions or 10 million. The projection matrix need not be learned; it can be drawn at random from a Gaussian or ±1 distribution and the guarantee holds in expectation.

In practice, random projection is most useful as a preprocessing step: fast, parameter-free, and effective at reducing the computational cost of downstream methods without requiring optimization.

### Feature Selection

Beyond projection-based reduction, standard feature selection techniques identify individual features that carry the most discriminative or variance-explaining information and discard the rest. This approach preserves interpretability at the cost of potentially missing relationships that only appear in linear combinations of features.

## Evaluation Metrics

Evaluating clustering without ground truth labels requires internal validity measures — metrics that characterize cluster quality from the data geometry alone.

**Silhouette score** measures how similar a point is to its own cluster compared to the nearest other cluster:

$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$

where $a(i)$ is the mean distance from point $i$ to other points in its cluster, and $b(i)$ is the mean distance from point $i$ to points in the nearest other cluster. Scores range from $-1$ (wrongly assigned) to $+1$ (well-clustered), with values near zero indicating overlapping clusters.

**Davies-Bouldin index** measures the average similarity between each cluster and its most similar cluster:

$$\text{DB} = \frac{1}{k} \sum_{i=1}^{k} \max_{j \neq i} \frac{s_i + s_j}{d_{ij}}$$

where $s_i$ is the average intra-cluster distance for cluster $i$ and $d_{ij}$ is the distance between centroids $i$ and $j$. Lower values indicate better separation. Unlike silhouette score, the Davies-Bouldin index directly penalizes clusters that are large relative to the distance between their centers.

## Key Findings

### Finding 1: Method Rankings Were Dataset-Dependent

The most consistently replicated result was that no clustering method dominated across both datasets. K-Means achieved better silhouette scores on the first dataset, where the cluster geometry was roughly spherical and the feature space was continuous. EM's richer covariance structure gave it an advantage on the second dataset, where the clusters were elongated and the effective shape of the decision boundary was not axis-aligned.

This is not a paradox. It is a direct consequence of the algorithms' different inductive biases. K-Means assumes spherical clusters; EM can model elliptical ones. The dataset with spherical clusters rewarded K-Means; the dataset with non-spherical clusters rewarded EM. The lesson is that exploratory visualization of cluster geometry should precede algorithm selection.

### Finding 2: Dimensionality Reduction Improved Clustering Quality — But Not Always the Same Way

On the continuous-feature dataset, PCA reduced noise in the feature space and improved clustering performance: the projected representation made the cluster geometry more visible to both K-Means and EM. The improvement was largest when the retained variance was around 80–90% — enough to capture the signal while discarding the noise dimensions.

On the mixed-feature dataset, ICA produced components that were more semantically coherent than PCA components, and clustering on the ICA representation showed higher silhouette scores than on the PCA representation. The underlying structure of that dataset reflected independent generating processes that ICA was better suited to recover.

Random projection showed more variable results: competitive with PCA in some configurations, significantly worse in others, reflecting its inherently random nature. But its speed advantage was consistent and substantial — for large datasets, the computation time was a fraction of the learned reduction methods.

### Finding 3: Runtime Analysis Exposed Real Trade-Offs

Wall-clock benchmarking revealed that EM was substantially slower than K-Means at equivalent cluster counts, and the gap widened as dimensionality increased. For the larger dataset, EM with full covariance matrices was the binding computational constraint. This is a genuine practical consideration: the decision between K-Means and EM is not purely about cluster quality, it is also about what computational budget is available.

Among the dimensionality reduction methods, PCA was fastest (closed-form eigendecomposition), random projection was nearly as fast, and ICA was significantly slower due to its iterative optimization.

### Finding 4: The "Right" Number of Clusters Is Not One Number

Both methods require a specified number of clusters $k$, and selecting $k$ is a non-trivial problem. The elbow method plots total within-cluster variance (for K-Means) or log-likelihood (for EM) as a function of $k$ and looks for a kink in the curve. In practice, the curve often lacks a clean elbow; the "kink" is more of a gradual flattening that requires judgment to locate.

The silhouette score and Davies-Bouldin index gave complementary signals: they often agreed on the best $k$ but sometimes pointed in different directions, particularly when the data had hierarchical structure (clusters within clusters). In those cases, the right answer was not to pick one metric but to understand *why* they disagreed.

## Why This Project Is Research-Relevant

Unsupervised learning is foundational to many practical ML pipelines: anomaly detection, customer segmentation, dimensionality reduction before supervised learning, exploratory analysis of new datasets. But it is also methodologically subtle, because there is no ground truth to optimize against. The researcher must construct a framework for evaluating quality that is defensible on theoretical grounds.

This project demonstrates:

- **Rigorous use of internal validation metrics** as a substitute for external ground truth
- **Principled comparison of algorithms** with different inductive biases across multiple domains
- **Mathematical grounding in clustering objectives and reduction techniques** including EM's probabilistic model and the Johnson-Lindenstrauss guarantee
- **Runtime-aware evaluation** as a component of practical model selection
- **Scientific discipline** in interpreting results that do not have a single right answer

The methodology scales directly to production settings where labels are unavailable and structure must be inferred from data alone.

## Artifacts and Provenance

- Course: [CS 7641: Machine Learning](https://omscs.gatech.edu/cs-7641-machine-learning)
- OMSCS path: `ML/A3/`
- Experiment implementation: `ML/A3/main.py`
- Analysis traces and report draft materials: `ML/A3/log.txt` and `ML/A3/bak.txt`

## Summary

Unsupervised learning finds structure in data without labels. This project ran two clustering algorithms (K-Means and EM) and four dimensionality reduction methods (PCA, ICA, random projection, feature selection) across two datasets, measuring quality with silhouette scores, Davies-Bouldin indices, and wall-clock time.

The result: no method won everywhere. Method rankings depended on the geometry of the data, and choosing the right tool required understanding both the algorithm's assumptions and the data's structure. That matching process — not any individual accuracy number — is the intellectual contribution.

## Policy Note

This page shares high-level research outcomes and mathematical framing only. Implementation details are kept private to align with course policy.
