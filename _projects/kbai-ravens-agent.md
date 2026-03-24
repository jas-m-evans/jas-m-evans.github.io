---
title: "KBAI Raven's Progressive Matrices Agent"
description: "Built a symbolic visual reasoning agent to solve Raven's Progressive Matrices — the gold-standard IQ test for fluid intelligence — and analyzed its performance across hundreds of benchmark problems."
layout: project
image: "/assets/images/projects/kbai-rpm-sample.svg"
---

## Abstract

This project constructs a symbolic visual reasoning agent capable of solving Raven's Progressive Matrices — standardized nonverbal puzzles used to measure fluid intelligence — through explicit representation of visual objects, attributes, and transformation rules. The agent parses each figure into structured semantic descriptions, detects transformation patterns across matrix rows and columns, and selects the answer that best extends the observed pattern. Evaluated against benchmark problem sets of increasing difficulty, the agent demonstrates competitive performance on regular transformations and illuminates the precise conditions under which symbolic, interpretable approaches succeed and where they reach their limits.

## The Big Idea (No Math Required)

You've probably seen puzzles like this: a 3×3 grid of geometric shapes, with one cell missing. Eight possible answers are shown below — which one completes the pattern?

Humans find these almost automatic after a moment of thought. But for a computer, this is surprisingly hard. Why? Because the puzzle isn't testing whether you can *see* the shapes — it's testing whether you can reason about *relationships between changes*. You must notice that "each row adds a dot," or "each column rotates the shape 90°," and then *apply that rule* to a new context you've never seen before.

This kind of reasoning — called *analogical reasoning* — is considered one of the hallmarks of human intelligence. It's why these puzzles are used in IQ tests and why building a computer agent that solves them is a meaningful research challenge.

This project built such an agent using *symbolic AI*: no neural network, no pixel statistics, just a structured representation of objects, relationships, and transformation rules. The agent describes what it *sees*, reasons about what *changed*, and selects the answer that best continues the pattern — exactly the way a human does.

## The Test That Stumps Machines

In 1936, psychologist John C. Raven published a series of visual analogy puzzles designed to measure *fluid intelligence* — the capacity to reason about novel problems without relying on prior knowledge. His Progressive Matrices have since become the most widely used nonverbal intelligence test in the world, employed in everything from military selection to clinical psychology research. They are also, notoriously, hard for computers.

The structure of each problem is deceptively simple. You are given a 2×2 or 3×3 grid of geometric figures, with one cell missing. Below the grid are eight candidate answers. Your task is to identify the one answer that correctly completes the pattern. Humans with strong spatial reasoning solve them quickly and confidently. But articulating *why* a particular answer is correct — and encoding that reasoning in a program — turns out to require a rich theory of visual transformation and analogy.

This project, completed in [CS 7637: Knowledge-Based Artificial Intelligence](https://omscs.gatech.edu/cs-7637-knowledge-based-artificial-intelligence-cognitive-systems) at Georgia Tech, was the construction of exactly such an agent.

![Sample Raven's Progressive Matrices problem — 3×3 format with size-progression pattern](/assets/images/projects/kbai-rpm-sample.svg)

*Representative 3×3 Raven's Progressive Matrix showing a size-and-shape progression pattern. The agent must identify which answer option correctly completes the bottom-right cell by detecting transformation rules across rows and columns. Problem structure based on Raven (1938) and Carpenter, Just & Shell (1990).*

> **Image source:** Problem structure and format derived from Raven, J.C. (1938). *Progressive Matrices: A Perceptual Test of Intelligence*. H.K. Lewis & Co.; and Carpenter, P.A., Just, M.A., & Shell, P. (1990). What one intelligence test measures: A theoretical account of the processing in the Raven Progressive Matrices Test. *Psychological Review, 97*(3), 404–431.

## Why This Problem Is Hard for AI

At first glance, a Raven's matrix might look like a pattern-matching problem solvable by image comparison. It is not.

Consider a problem where the figure in the top-left cell contains a large circle, the figure in the top-right contains a large circle with a small circle inside it, and the figure in the middle-left contains a large triangle. A correct solver must recognize that the transformation from top-left to top-right is "add a smaller version of the same shape inside," and then apply that same transformation in the new context of a triangle. This requires:

1. **Segmentation** — decomposing each figure into its constituent objects and attributes
2. **Relationship encoding** — representing spatial relationships between objects (inside, above, left-of, overlapping)
3. **Transformation detection** — identifying what changed between corresponding cells
4. **Analogy completion** — selecting the candidate that applies the same transformation to the new context

Each step is non-trivial. The visual surface of the problem is incidental; the substance is the *algebraic structure of the transformation*. Two figures that look completely different might be related by the same transformation as two figures that look nearly identical.

This is the classic insight from cognitive science's study of analogy: structure matters more than surface. A purely perceptual approach fails on the harder problems precisely because it confuses similarity of appearance with similarity of relationship.

## Research Context

The field of machine approaches to Raven's matrices has a long history. Early work by Hunt (1974) and more recent approaches by Carpenter, Just, and Shell (1990) used production system models to simulate human performance. More recently, the field has split between:

- **Symbolic approaches**, which represent figures and transformations explicitly and reason by rule application
- **Neural approaches**, which learn feature representations and scoring functions end-to-end

The symbolic approach has a distinctive advantage: *interpretability*. When the agent gets a problem wrong, you can inspect exactly which transformation it applied and why it chose the answer it did. This makes error analysis tractable in a way that opaque models simply do not support. It also makes the agent's reasoning *verifiable* — an important property in any system meant to model cognition.

This project followed the symbolic tradition, building a rule-based transformation engine that operated on structured representations of visual relationships.

## Technical Approach

### Representing Figures

Each figure in the matrix was parsed into a set of *objects* — individual geometric shapes — with associated attribute-value pairs:

- **Shape**: circle, square, triangle, diamond, cross, etc.
- **Size**: small, medium, large (or pixel-count ranges)
- **Fill**: empty, filled, half-filled
- **Position**: relative location within the frame (center, top-left, etc.)
- **Relationship**: spatial relationships between objects in the same figure

This representation, sometimes called a *semantic network*, captures the structural content of a figure while abstracting away rendering details. Two figures that look different but have the same structural representation would be treated as identical by the agent.

### Detecting Transformations

Given parsed representations of the known cells, the agent compares corresponding positions — row by row or column by column — to identify the transformation sequence. Each transformation is a mapping from one attribute configuration to another:

- **Constant**: attribute value unchanged across positions
- **Addition**: a new object appears
- **Deletion**: an existing object disappears
- **Attribute change**: size, shape, fill, or count changes
- **Reflection / rotation**: spatial orientation changes

The agent scores each candidate answer by asking: *how well does this answer extend the observed transformation sequence?* A candidate that is consistent with the row transformation *and* the column transformation receives the highest score.

The scoring function can be thought of as minimizing the *transformation inconsistency* across all axes:

$$\text{score}(c) = -\sum_{\text{axis} \in \{\text{row}, \text{col}\}} \sum_{\text{attr}} w_{\text{attr}} \cdot \delta\!\left(T_{\text{axis}}(\text{attr}),\, c_{\text{attr}}\right)$$

where $T_{\text{axis}}(\text{attr})$ is the expected attribute value given the detected transformation, $c_{\text{attr}}$ is the candidate's attribute value, $\delta$ is a discrepancy function, and $w_{\text{attr}}$ is a weight reflecting the reliability of that attribute in prior problems.

In practice, this scoring logic evolved iteratively as the agent encountered problems where simple attribute matching was insufficient and compositional transformation rules were required.

### Iterative Refinement

The agent was developed and evaluated against a sequence of benchmark problem sets of increasing difficulty. Problem sets D and E in the standard Raven's benchmark involve composite transformations, figure counts that change arithmetically across the matrix, and relationships that are defined relative to other figures rather than absolutely.

Each failure case became a diagnostic. When the agent selected the wrong answer, analysis of its scoring trace revealed whether the error was:

- A segmentation failure (two objects parsed as one)
- A missing transformation type (the agent had no rule for this kind of change)
- A tie-breaking failure (two candidates with equal scores, wrong one selected)
- A weight calibration issue (a less reliable attribute was weighted too heavily)

This cycle of evaluate → diagnose → refine is itself an important research skill: the ability to turn failures into targeted improvements rather than undirected guessing.

## Key Findings

### Symbolic Reasoning Is Competitive on Structured Problems

On the standard 2×2 problem sets (Sets B and C), the agent achieved strong performance, solving the large majority of problems correctly. These problems have transformations that are regular, single-attribute, and axis-consistent — precisely the conditions under which a symbolic rule-based approach excels.

### Performance Degraded Gracefully on Compositional Problems

On the harder 3×3 sets (Sets D and E), performance declined but did not collapse. The agent continued to identify the correct transformation structure on many problems, with errors concentrated in cases requiring compositional or numerical reasoning (e.g., "the count increases by one across the row"). Extending the rule vocabulary to cover arithmetic relationships improved these results meaningfully.

### Interpretability Accelerated Improvement

The single biggest advantage of the symbolic approach was that every error was explainable. This made the development cycle fast. A neural approach to the same problem would require ablation studies, attention visualization, or other indirect methods to diagnose failures; the symbolic agent's scoring trace made failures immediately readable.

### The Hardest Problems Require Relational Reasoning

Problems in the hardest sets — where objects are defined by their relationships to other objects rather than their absolute attributes — were the most challenging and the most illuminating. They required encoding second-order structure: not just "this figure has three objects" but "the three objects are arranged in a size gradient from left to right." These are the problems that reveal whether the agent is truly reasoning about structure or merely matching local patterns.

## Why This Project Is Research-Relevant

Raven's Progressive Matrices occupy a special place in AI research because they are a *behavioral benchmark for general reasoning*. Human intelligence researchers use them to measure abstract problem-solving capacity specifically because they cannot be solved by memorization or domain-specific knowledge. A machine that solves them well is doing something more general than, say, an image classifier — it is manipulating relational structure in a way that transfers across surface presentations.

This project demonstrates:

- **Knowledge representation**: how to encode visual information in a form amenable to symbolic manipulation
- **Analogy-based reasoning**: the core cognitive mechanism underlying matrix completion
- **Iterative scientific debugging**: using evaluation traces to direct targeted improvement
- **The scope and limits of symbolic AI**: where rule-based methods excel, where they struggle, and why that distinction matters

The debate between symbolic and neural approaches to cognition is ongoing. This project gives a concrete grounding to that debate: not as an abstract philosophical argument, but as a head-to-head empirical comparison with a clear behavioral benchmark.

## Artifacts and Provenance

- Course: [CS 7637: Knowledge-Based Artificial Intelligence—Cognitive Systems](https://omscs.gatech.edu/cs-7637-knowledge-based-artificial-intelligence-cognitive-systems)
- OMSCS path: `KBAI/RPM-Project-Code/`
- Agent driver and evaluation outputs: `KBAI/RPM-Project-Code/RavensProject.py` and `AgentAnswers.csv`
- Milestone writeup: `KBAI/RPM Project_ Milestone 3.pdf`
- Reference: Carpenter, Just & Shell (1990), *What one intelligence test measures: A theoretical account of the processing in the Raven Progressive Matrices Test*, Psychological Review

## Summary

Raven's matrices are the visual analogy puzzles used to measure fluid intelligence on IQ tests. Building a machine that solves them requires representing figures as structured descriptions, detecting transformations across the matrix, and selecting the answer that best extends the pattern. This agent did that through explicit symbolic rules, which made it both competitive on benchmark problems and easy to diagnose when it went wrong.

The deepest lesson: understanding *why* a model fails is often more valuable than maximizing the metric.

## Policy Note

This portfolio summary shares concepts, methodology, and outcomes only. Assignment implementation details are not reproduced here.
