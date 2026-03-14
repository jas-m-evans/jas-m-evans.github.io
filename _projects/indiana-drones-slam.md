---
title: "Indiana Drones: SLAM Under Uncertainty"
description: "A robotics-focused study of simultaneous localization and mapping, with noisy sensing, constrained motion, and extraction planning."
layout: project
---

## Research Context

This project comes from CS7638 (AI for Robotics) and centers on a classic robotics problem: how does an autonomous agent build a map and localize itself at the same time, while its sensors and movement are noisy?

In the assignment environment, the drone starts at an unknown global position, represents that start as a local origin, receives noisy landmark measurements, and must navigate to extract treasure while avoiding tree obstacles.

The challenge is not just path planning. The harder problem is state estimation under uncertainty.

## What Is SLAM (High-Level)

SLAM stands for Simultaneous Localization and Mapping.

At a high level, SLAM answers two questions continuously:

- Where am I?
- What does the world around me look like?

Those two questions are coupled:

- If your map is wrong, your location estimate drifts.
- If your location estimate drifts, your map updates become wrong.

So SLAM solves a feedback loop. The robot uses landmarks and motion updates to refine both the map and its own pose over time.

In human terms, this is similar to walking through a dark room with a flashlight. You infer where furniture is, but at the same time you also infer where you are standing relative to that furniture.

## Why This Problem Is Hard

This project includes multiple uncertainty sources:

- Measurement noise in distance and bearing readings
- Motion uncertainty in executed moves
- Partial observability from sensor horizon limits
- Dynamic landmark visibility (new trees can appear as the drone moves)

Even when each individual uncertainty looks small, they compound over many steps. Without robust update logic, small errors become large trajectory drift.

## Technical Problem Setup

The coursework is split into two linked parts.

### Part A: Estimation Core

Build a SLAM module that consumes:

- Landmark measurements in the form of distance, bearing, and radius
- Movement commands in the form of turn + forward move

And returns:

- Estimated drone pose
- Estimated landmark positions

### Part B: Action Planning

Build a planner that chooses actions to reach and extract treasure:

- move distance steering
- extract type x y

Extraction only succeeds when the drone is within a strict distance threshold of the treasure.

## SLAM in More Detail (Coursework Level)

In this assignment framing, SLAM behavior follows a repeated cycle:

1. Receive measurements to visible landmarks.
2. Update belief about landmark geometry and current pose.
3. Apply motion update (with steering and distance constraints).
4. Reconcile expected and observed geometry on the next cycle.

A practical way to think about the estimator is as a probabilistic state tracker. Rather than treating each reading as ground truth, it accumulates evidence across timesteps and seeks internally consistent geometry.

The representation in the assignment code references matrix-based information form concepts (Omega/Xi style structure), which is common in graph-style and information-filter SLAM formulations.

## Evaluation Conditions I Analyzed

From the test harness and case definitions in the repository, the evaluation emphasizes robustness under realistic constraints:

- Position tolerances on drone and landmark estimates at approximately 0.25 m
- Typical measurement noise settings around 0.05 (distance) and 0.03 (bearing)
- Horizon-limited sensing in harder cases (for example horizons of 3 or 4)
- Steering and movement limits per action
- Obstacle-rich maps with varying tree radii

For planning tasks, the drone must not only estimate correctly, but also complete treasure extraction with strict geometric requirements.

## Results and Analysis Summary

This project produced its strongest insights in error behavior and robustness, not in one-off trajectory demos.

### 1) Estimation Stability Is the Core Bottleneck

The dominant failure mode in SLAM-style tasks is not usually "bad planning" first, it is pose drift. Once pose drift grows, planner quality appears to collapse because actions are evaluated against an increasingly inaccurate world model.

### 2) Noise-Tolerant Logic Matters More Than Aggressive Motion

Cases with nonzero distance and bearing noise reward conservative, geometry-consistent updates. In short missions, aggressive movement may look fast, but under uncertainty it can amplify downstream extraction error.

### 3) Partial Visibility Changes the Strategy

When horizon is limited, map completeness becomes path dependent. The order in which the drone explores matters because landmark acquisition itself becomes an information-gathering action, not just a navigation side effect.

### 4) Obstacle Geometry Is a First-Class Constraint

Tree radii and corridor shapes materially affect feasible trajectories. A planner that ignores clearance margins can appear correct in open maps but fail in dense maps.

### 5) Strict Extraction Thresholds Expose Real Accuracy

The extraction distance requirement forces practical precision. This is important because many estimators can look visually close while still failing discrete task objectives.

## Why This Project Is Research-Relevant

For a research-oriented profile, this project demonstrates more than implementation:

- It frames uncertainty as a modeling problem, not just a coding task.
- It links estimation quality to downstream decision quality.
- It develops intuition for the trade-off between exploration, confidence, and control.
- It mirrors real robotics and autonomy workflows where sensing, inference, and planning are inseparable.

## Artifacts and Provenance

- Course: CS7638 AI for Robotics
- OMSCS path: rait/IndianaDrones/
- Assignment implementation scaffold: rait/IndianaDrones/indiana_drones.py
- Evaluation harness: rait/IndianaDrones/testing_suite_indiana_drones.py
- Test scenarios and constraints: rait/IndianaDrones/test_cases.py
- Project brief: rait/IndianaDrones/cs7638-indiana-drones.pdf

## Reader-Friendly TL;DR

If you are new to SLAM, this project is a concrete demonstration of a key robotics idea:

- Navigation is easy when the map is perfect.
- Mapping is easy when your location is perfect.
- Real robots have neither.

SLAM is the method that makes both estimates improve together, step by step, under uncertainty.

## Policy Note

This writeup intentionally presents methodology and analysis only. Assignment solution code is not reproduced here.