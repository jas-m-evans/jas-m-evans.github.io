---
title: "KBAI Raven's Progressive Matrices Agent"
description: "Built a symbolic visual reasoning agent for Raven's matrices and analyzed performance across benchmark problem sets."
layout: project
image: "/assets/images/projects/kbai-rpm-sample.svg"
---

## Overview

This project focused on classical AI reasoning for visual analogy problems in Raven's Progressive Matrices. The system emphasized interpretable decision rules and structured reasoning rather than end-to-end deep learning.

![Sample Raven's Progressive Matrices problem](/assets/images/projects/kbai-rpm-sample.svg)

## Research Focus

- How far can symbolic reasoning go on abstract visual analogy tasks?
- Which transformations are most informative for 2x2 and 3x3 matrix patterns?
- How should solver behavior be evaluated across diverse problem families?

## Approach

- Parsed visual relationships between problem frames and candidate answers
- Encoded transformation logic and scoring heuristics for analogy completion
- Iteratively refined reasoning rules using benchmark feedback
- Tracked solution outputs and aggregate performance across sets

## Key Findings

- Symbolic methods can be highly competitive on structured visual reasoning tasks.
- Interpretable reasoning made error analysis significantly easier than opaque models.
- Performance improved as transformation rules became more compositional.

## Artifacts

- Course: [CS 7637: Knowledge-Based Artificial Intelligence and Cognitive Systems](https://omscs.gatech.edu/cs-7637-knowledge-based-artificial-intelligence-cognitive-systems)

{% comment %}
Internal references (hidden from rendered page):
- OMSCS path: KBAI/RPM-Project-Code/
- Driver and evaluation outputs: KBAI/RPM-Project-Code/RavensProject.py and AgentAnswers.csv
- Milestone writeup: KBAI/RPM Project_ Milestone 3.pdf
{% endcomment %}

## Policy Note

This portfolio summary shares concepts and outcomes only. Assignment implementation details are not published here.
