---
title: "Supervised Learning: Five Algorithms, Two Domains, One Experimental Framework"
description: "A rigorous comparative study of five supervised learning algorithms across two structurally different datasets — examining bias, variance, decision geometry, and the true cost of generalization."
layout: project
---

## The Question Behind the Experiment

Every supervised learning project rests on an implicit question: *what makes a classifier work here, and would it work somewhere else?*

That question sounds deceptively simple. In practice, answering it rigorously requires controlling for dataset-specific effects, running systematic hyperparameter searches, examining learning dynamics rather than single-point results, and being honest about what the numbers actually say. This project, completed in [CS 7641: Machine Learning](https://omscs.gatech.edu/cs-7641-machine-learning) at Georgia Tech, was an exercise in exactly that kind of disciplined experimental science.

Five algorithm families. Two structurally different datasets. One unified evaluation framework. The goal was not to find the best model. It was to understand *how* these models differ, *why* those differences emerge, and *when* the tradeoffs matter.

## Two Datasets, Two Worlds

### Dataset 1: Physicochemical Wine Quality

The first dataset is drawn from [UC Irvine's Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/wine+quality) and tracks red and white wines from the Vinho Verde region of Portugal. Each sample captures eleven physicochemical measurements — fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free and total sulfur dioxide, density, pH, sulphates, and alcohol content — with a quality label ranging from three to eight, assigned by panels of trained human tasters.

This is not a trivial classification problem. It is a problem of *mapping physics to perception*. The labels carry genuine noise — two sommeliers rating the same wine may disagree by a point — and the class distribution is sharply imbalanced: the middle quality scores (five and six) dominate the dataset, while extremes (three, four, eight) appear rarely. A naive model that predicts "five or six" for every sample achieves respectable accuracy while learning almost nothing about what makes a wine exceptional or poor.

What makes this dataset scientifically useful as a benchmark is precisely that challenge: it demands the model learn the *boundary structure* of a noisy, nonlinear, imbalanced problem, not just fit a clean signal.

### Dataset 2: Census Income

The second dataset is the [UCI Adult Census dataset](https://archive.ics.uci.edu/ml/datasets/adult), derived from the 1994 U.S. Census Bureau database. The task is binary classification: predict whether an individual's annual income exceeds \$50,000 based on fourteen features including age, education level, occupation, marital status, and hours worked per week. The dataset contains over 48,000 records.

This problem differs from the wine task in almost every structural dimension. The input space is categorical and mixed, not purely continuous. The signal is stronger and the class boundary more stable. The features relate to socioeconomic factors that carry real-world consequence, and the dataset has become canonical in fairness-aware machine learning research as a benchmark for studying how predictive models interact with demographic attributes.

Together, these two datasets were chosen deliberately: one with a noisy, multiclass, continuous-feature structure; one with a clean binary decision in a mixed categorical space. If a finding held across both, it was meaningful. If it only appeared in one, the dataset's geometry was likely the cause.

## The Five Algorithm Families

The heart of this project was a controlled comparison of five distinct model families, each representing a different inductive bias — a different set of assumptions about what structure in the data is worth learning.

### 1. Decision Trees

A decision tree partitions the feature space into axis-aligned rectangles, selecting at each node the split that maximizes the reduction in impurity. For classification, the standard criterion is the Gini impurity:

$$G(t) = \sum_{k=1}^{K} \hat{p}_{tk}(1 - \hat{p}_{tk})$$

where $\hat{p}_{tk}$ is the fraction of class-$k$ samples at node $t$. A split is chosen to minimize the weighted average impurity of the two resulting children. The tree grows until every leaf is pure or a depth constraint is reached.

The core question for decision trees is not what they compute — it is *how deep to let them grow*. An unpruned tree memorizes training data. A heavily pruned tree underfits. The depth hyperparameter directly controls the bias-variance balance, and validation curves over depth are one of the clearest demonstrations of that tradeoff in all of machine learning.

### 2. k-Nearest Neighbors

k-NN is a non-parametric method: it makes no assumptions about the functional form of the decision boundary. At inference time, a new point is classified by a plurality vote among its $k$ nearest neighbors under some distance metric — typically Euclidean:

$$d(\mathbf{x}, \mathbf{x}') = \sqrt{\sum_{j=1}^{d}(x_j - x_j')^2}$$

The parameter $k$ governs smoothness. When $k = 1$, the classifier is maximally flexible: the decision boundary is a Voronoi tessellation of the training data, and training error is zero. As $k$ increases, the boundary smooths out and bias rises while variance falls. The optimal $k$ is a function of the intrinsic dimensionality of the data and the amount of label noise.

k-NN has a critical operational property: it is a *lazy learner*. Training is free — no parameters are fit — but inference is expensive, scaling as $O(nd)$ per query in a naive implementation. For large datasets, this becomes the binding computational constraint.

### 3. Support Vector Machines

SVMs seek the maximum-margin hyperplane separating two classes. In the linearly separable case, the optimization problem is:

$$\min_{\mathbf{w}, b} \frac{1}{2}\|\mathbf{w}\|^2 \quad \text{subject to} \quad y_i(\mathbf{w}^T \mathbf{x}_i + b) \geq 1 \;\; \forall i$$

where the margin is $\frac{2}{\|\mathbf{w}\|}$ and the constraints enforce correct classification with at least unit distance from the boundary. In practice, a soft-margin formulation is used that tolerates misclassification through slack variables $\xi_i \geq 0$:

$$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_i \xi_i$$

The regularization parameter $C$ trades margin width against training accuracy. Large $C$ tolerates little slack; small $C$ allows wider margins with more training error.

When the data is not linearly separable in input space, the *kernel trick* maps features to a higher-dimensional space where linear separation may exist, without ever computing the explicit mapping. The Radial Basis Function (RBF) kernel, $K(\mathbf{x}, \mathbf{x}') = \exp(-\gamma \|\mathbf{x} - \mathbf{x}'\|^2)$, effectively measures similarity through a Gaussian. Together, $C$ and $\gamma$ form the core of the SVM tuning problem.

### 4. Neural Networks (MLP)

A multilayer perceptron computes a composition of affine transformations and nonlinearities:

$$f(\mathbf{x}) = \sigma^{(L)}\!\left(\mathbf{W}^{(L)} \cdots \sigma^{(1)}\!\left(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}\right) \cdots + \mathbf{b}^{(L)}\right)$$

Training minimizes cross-entropy loss $\mathcal{L} = -\sum_i \sum_k y_{ik} \log \hat{p}_{ik}$ via backpropagation and stochastic gradient descent. The model has the highest capacity of any algorithm in this study — given sufficient width and depth, an MLP can approximate any continuous function — but that capacity cuts both ways. Without regularization (dropout, weight decay, early stopping), a sufficiently large network will memorize training labels rather than learn generalizable structure.

The gap between training and validation accuracy on learning curves is the diagnostic signal. A model that achieves 99% training accuracy and 72% validation accuracy has not solved the problem; it has described the training set.

### 5. Gradient Boosting

Gradient boosting builds an ensemble by additively combining weak learners — typically shallow decision trees — each one trained to correct the residuals of the previous ensemble. The prediction at step $m$ is:

$$F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \eta \cdot h_m(\mathbf{x})$$

where $h_m$ is the new tree, $\eta$ is the learning rate, and the tree is fit to the negative gradient of the loss — effectively the direction of steepest descent in function space. This view, due to Friedman (2001), is called *functional gradient descent*.

The combination of a slow learning rate and many shallow trees tends to produce models with excellent generalization, but at a meaningful computational cost. Runtime scales with the number of boosting rounds, and each round requires a full pass over the training data.

## Experimental Design

Every algorithm was evaluated under the same protocol, designed to surface generalization rather than overfit to a lucky configuration.

**Hyperparameter sweeps** used cross-validated grid search, evaluating each configuration on held-out data rather than training performance. The objective was always generalization; training accuracy was recorded for diagnostic purposes only.

**Validation curves** plotted test performance as a function of a single hyperparameter while holding others fixed. These curves make the bias-variance tradeoff visible: on the left, the model is underfit and both training and validation error are high; on the right, training error continues to fall while validation error rises, signaling overfitting.

**Learning curves** asked a different question: how does performance change as a function of training set size? A model with irreducible high error regardless of data volume is limited by its hypothesis class. A model where training and validation error converge as $n$ grows is operating in the regime where more data helps.

**Runtime benchmarking** measured wall-clock training and inference time, because in practice computational cost is never free.

## Key Findings

### Finding 1: No Single Model Dominated Across Both Domains

The most important result of this experiment is also the most humbling: none of the five algorithms consistently outperformed all others across both datasets. Performance was strongly domain-dependent, and the algorithms that appeared "best" on the wine task were not the same ones that led on the census task.

This is not a failure of the experiment. It is the correct result. The No Free Lunch theorem, formalized by Wolpert and Macready (1997), states that no learning algorithm outperforms every other algorithm on every possible problem when performance is averaged uniformly across all possible data distributions. The practical implication: algorithm selection is always a domain-specific judgment, not a universal ranking.

### Finding 2: Decision Tree Depth Is a Direct Dial for Bias-Variance

The validation curve for decision tree depth was among the clearest demonstrations in the study. At depth one or two, the model was too constrained to capture the problem structure — high bias, comparable training and validation error, both poor. As depth increased, training accuracy improved rapidly while validation accuracy lagged, eventually declining. The crossover point identified the optimal capacity for each dataset.

Notably, the optimal depth differed between datasets. The physicochemical wine problem, with its noisy labels and complex feature interactions, rewarded deeper trees than the census problem. The signal-to-noise ratio of the target is a real constraint on how complex a model can profitably be.

### Finding 3: SVMs Were Strong but Sensitive to Kernel Tuning

Support vector machines achieved competitive performance on both datasets but required careful selection of both $C$ and $\gamma$. The RBF kernel was consistently better than the linear kernel on the wine task (where the boundary is nonlinear in the physicochemical space) and approximately equivalent on the census task.

The runtime cost of SVMs is worth noting: training scales as $O(n^2)$ to $O(n^3)$ for the quadratic programming formulation, making it the most expensive algorithm tested on large datasets. For the census data with 48,000 records, this was the binding constraint on how finely the hyperparameter grid could be searched.

### Finding 4: Neural Networks Required the Most Careful Tuning to Avoid Overfitting

MLPs achieved the highest raw capacity but also produced the worst validation performance in early configurations. The gap between training and validation accuracy was largest for neural networks, reflecting their tendency to memorize training labels when regularization is insufficient.

With appropriate dropout, weight decay, and early stopping, MLPs became competitive — but the tuning burden was substantially higher than for tree-based methods. This is the central practical tradeoff of high-capacity models: they can learn more complex functions, but only if you help them not learn *everything*.

### Finding 5: Gradient Boosting Provided the Best Consistent Performance

Across both datasets, gradient boosting achieved the best or near-best performance with the least additional tuning effort compared to SVMs or neural networks. The combination of strong regularization through the learning rate and ensemble averaging gave it robustness to the kinds of noisy labels present in the wine data.

The runtime cost was meaningful — many boosting rounds on the census dataset was notably slower than k-NN or a shallow decision tree — but the performance-to-tuning-effort ratio made it the most practically useful algorithm in this study.

## Why the Wine Dataset Is the Hard One

It is worth spending a moment on what makes the wine quality task genuinely difficult, beyond its reputation as a standard benchmark.

Human wine quality ratings are a proxy signal, not a ground truth. Two trained tasters assessing the same bottle may differ by a point. The measurement process introduces label noise at the source that no model can remove, because the noise is baked into the target variable, not the features. The Bayes error rate — the irreducible minimum error achievable by any classifier — is nonzero and likely nontrivial for this task.

At the same time, the physicochemical features carry real information. Alcohol content, volatile acidity, and sulphate concentration are all genuine predictors of perceived quality. The challenge is that their effects are nonlinear and interactive: the relationship between acidity and quality depends on the level of residual sugar and the sulfur dioxide balance. Feature engineering or model capacity is required to capture these interactions.

The imbalance problem compounds everything. With most samples clustered at quality five and six, a model that learns only the dominant cluster will appear to perform well by accuracy while being useless for distinguishing high-quality from low-quality wine. Metrics like macro-averaged F1 score and per-class precision reveal what accuracy hides.

This is, in short, a realistic problem: noisy labels, nonlinear interactions, imbalanced classes, and a target that is a human judgment rather than a physical measurement. The census task is cleaner and its lessons clearer, but the wine task is closer to what supervised learning looks like in production environments where the ground truth is not always crisp.

## Why This Project Is Research-Relevant

Comparative algorithm studies are a cornerstone of empirical machine learning research. The contribution is not a new algorithm; it is the construction of a controlled experimental setting that lets the algorithms speak for themselves.

This project demonstrates:

- Experimental design: controlling confounds, separating hyperparameter effects from dataset effects, using held-out data consistently.
- Diagnostic thinking: learning curves, validation curves, and runtime benchmarks are tools for understanding *why* a model behaves the way it does, not just *what* it achieves.
- Scientific reasoning: the finding that no single model dominates is a real result, not a failure. It is what the data says, and it is consistent with theoretical expectations.
- Practical judgment: knowing when gradient boosting's simplicity of deployment beats SVM's marginal accuracy gain, or when an MLP's capacity is genuinely needed, is a skill that only emerges from running this kind of comparison.

The methodology here scales directly to production ML: define a baseline, run controlled experiments, diagnose failure modes, and select models based on evidence rather than convention.

## Artifacts and Provenance

- Course: [CS 7641: Machine Learning](https://omscs.gatech.edu/cs-7641-machine-learning)
- OMSCS path: `ML/A1/`
- Core implementation: `ML/A1/main.py`
- Writeup guidance and methodology context: `ML/A1/README.txt`
- Reference datasets: [UCI Wine Quality](https://archive.ics.uci.edu/ml/datasets/wine+quality), [UCI Adult Census](https://archive.ics.uci.edu/ml/datasets/adult)

## Reader-Friendly TL;DR

If you want one sentence: this project ran five learning algorithms on two structurally different datasets, systematically tuned each one, and analyzed the results to understand *why* performance differed — not just *that* it differed.

The wine data was not chosen because it was interesting on its own. It was chosen because its label noise, class imbalance, and nonlinear feature interactions make it a harder and more realistic classification problem than clean benchmarks, and because comparing its results to the census dataset separated what was algorithmically general from what was dataset-specific.

That comparison is the scientific contribution.

## Policy Note

This page shares methodology, mathematical framing, and high-level findings only. Implementation details are kept private to respect CS 7641 academic integrity policy.