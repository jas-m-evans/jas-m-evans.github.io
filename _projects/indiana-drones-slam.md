---
title: "Indiana Drones: SLAM Under Uncertainty"
description: "A robotics-focused study of simultaneous localization and mapping, with noisy sensing, constrained motion, and extraction planning."
layout: project
image: "/assets/images/projects/indiana-drones-map.svg"
---

## The Problem: Lost in Your Own Map

Imagine you're in a completely dark room. Your only tool is a camera that flashes for one second every few minutes. In that brief moment of light, you glimpse the couch on the far wall and a chair nearby. Then darkness returns.

As you move forward cautiously, two questions plague you: *Where am I now?* and *What does this room actually look like?* These aren't independent. If your mental map is wrong, you'll misevaluate your position. If you misjudge where you stand, every new piece of information you gather warps the map further.

This is the core problem of robotics: **Simultaneous Localization and Mapping (SLAM).**

For the past decade, SLAM has been the unsolved technical challenge preventing robots from operating in unmapped, GPS-denied environments. Drones over buildings with no landmarks. Submarines investigating the ocean floor. Rovers exploring other planets. All face this same fundamental dilemma.

This project from [CS 7638: Robotics: AI Techniques](https://omscs.gatech.edu/cs-7638-robotics-ai-techniques) explores how to build robust SLAM systems when *every sensor lies a little*, *every movement misses its target a little*, and the stakes require precision anyway.

## The Challenge

In the assignment environment, an autonomous drone wakes up at an unknown global position. It doesn't know where it is. It receives noisy measurements to visible landmarks (trees with known radii), and must navigate to extract treasure while avoiding obstacles. All while building an accurate map and localizing itself simultaneously.

![Representative course-style SLAM environment](/assets/images/projects/indiana-drones-map.svg)

The constraints are punishing:
- **Measurement noise**: Distance and bearing readings are off by 5% and 3% respectively
- **Motion uncertainty**: The drone overshoots, undershoots, or drifts in unexpected ways
- **Partial observability**: The drone's sensors only see trees within a limited horizon
- **Discrete task requirements**: Treasure extraction succeeds only within a strict distance threshold, typically 0.25 meters

The core insight: this isn't primarily a path planning problem. It's an **estimation problem masquerading as a planning problem**.

## How Robots See and Think: The Kalman Filter

At the heart of SLAM lies a deceptively elegant algorithm called the **Kalman filter**, a mathematical technique that solves one of the 20th century's most consequential problems: *How do you blend predictions and measurements when both contain error?*

### The Core Idea: Two-Phase Reasoning

The Kalman filter operates in a predict-then-update cycle:

**Phase 1 (Prediction):** Based on what you know and the motion command you just issued, predict where you should be and what you should see. But quantify your uncertainty: "I'm probably here, but I'm only 70% confident."

**Phase 2 (Update):** New measurements arrive from sensors. These measurements contain noise and error, but they ground the estimate in reality. The filter asks: "Which should I trust more, my prediction or this measurement?" It doesn't simply average them. Instead, it weights them intelligently based on *how much uncertainty each one carries*.

This is the magic: **uncertainty quantification.**

### Why Uncertainty Matters

Every estimate doesn't just have a "best guess." It has an associated "confidence band." Your smartphone's GPS might say "you're here, plus-or-minus 50 feet." Dead reckoning (calculating position from accelerometer readings) might say "you're here, plus-or-minus 3 feet, but that uncertainty *grows* as time passes."

When these estimates conflict, the Kalman filter combines them optimally. It's not a heuristic guess. The mathematics that produces this optimal weighting comes from probability theory, specifically from understanding how Gaussian distributions (bell curves) behave when combined. The filter computes a quantity called the **Kalman gain**, which answers: "Given the uncertainty in my prediction and the uncertainty in this measurement, what weighted average should I use?"

The result: an estimate more accurate than any single sensor could provide, and resilient to sensor failures. If GPS goes out, the filter continues tracking using wheel odometry and corrects drift when GPS returns.

### Why It's Recursive and Efficient  

Every second (or millisecond, depending on the system), the filter updates using the previous estimate and the new measurement. This recursive nature is why Kalman filters appear in everything from spacecraft to smartphones to autonomous vehicles. They're computationally efficient enough to run everywhere.

### Extended and Nonlinear Variants

The classical Kalman filter assumes linear systems. Real robots don't behave that way. When a drone turns, the relationship between its wheel rotations and its position becomes nonlinear. The **Extended Kalman Filter (EKF)** linearizes these relationships locally, and **Unscented Kalman Filters** use clever sampling to handle nonlinearity even better.

For SLAM specifically, robots maintain a state vector that includes not just *their own pose* (position + orientation), but *all landmark positions too*. This couples the localization and mapping problems: as the robot localizes itself better, its landmarks snap into focus. As landmarks become more precise, errors in robot pose become visible. Both estimates improve together, step by step.

## Applied to Robotics and Autonomous Systems

In this assignment, the drone faces a concrete sensor fusion problem:

- **Perception**: Noisy range-and-bearing measurements to visible trees update the belief about tree locations
- **Estimation**: A state tracker (using Kalman-style updates) maintains a coherent drone pose and landmark geometry despite compounding errors
- **Decision-making**: The planner chooses motion commands that preserve enough accuracy to reach treasure extraction range

The coupling is tight. Once errors in the drone's pose estimate exceed the extraction distance threshold, the treasure becomes unreachable. The planner doesn't fail because of bad planning logic. It fails because bad estimation created an unusable world model.

### From Theory to Practice  

In the project, this manifests as several insights:

**Estimation Stability Is the Core Bottleneck**: The dominant failure mode isn't poor planning. It's pose drift. Once pose drift grows, the planner appears to collapse because actions are evaluated against an increasingly inaccurate world model.

**Noise-Tolerant Logic Beats Aggressive Movement**: Cases with nonzero distance and bearing noise reward conservative, geometry-consistent updates. In short missions, aggressive movement looks fast, but under uncertainty it amplifies downstream extraction error. Slow, careful estimation beats fast, confident mistakes.

**Information Gathering as Exploration**: When the drone's sensor horizon is limited, map completeness becomes path-dependent. The order of exploration matters because landmark acquisition itself becomes an information-gathering action, not just a navigation side effect.

**Obstacle Geometry as First-Class Constraint**: Tree radii and corridor shapes materially affect feasible trajectories. A planner that ignores clearance margins succeeds in open environments but fails in dense ones.

**Strict Thresholds Expose Real Accuracy**: The extraction distance requirement forces practical precision. Many estimators *look* visually close while still failing discrete task objectives. This mirrors real-world robotics where "approximately correct" isn't good enough.

## Historical Context: The Algorithm That Went to the Moon

The Kalman filter was invented by Rudolf Kálmán in the 1960s and immediately found its killer application: the Apollo Guidance Computer. Apollo needed to know its position in space with remarkable precision, with the margin of error for a lunar landing measured in meters across 238,000 miles of travel.

Remarkably, the Apollo Guidance Computer had **2 kilobytes of memory**, less computing power than a modern wristwatch. Yet it successfully performed Kalman filtering operations that steered humanity to the Moon. This single achievement secured the algorithm's place in every navigation system since, from submarines to smartphones to autonomous vehicles.

## Why This Research Matters

For those studying robotics and autonomous systems, this project demonstrates more than code:

- **Uncertainty as a modeling problem**, not just an implementation detail
- **The inseparability of sensing, inference, and planning** in autonomous systems
- **Why modest sensor noise becomes catastrophic estimation error** if not handled carefully
- **The power of probabilistic reasoning** under constraints

The broader lesson: robotics isn't about building the fastest or most complex system. It's about managing uncertainty intelligently, step by step, until coherence emerges.

## Artifacts and Provenance

- Course: [CS 7638: Robotics: AI Techniques](https://omscs.gatech.edu/cs-7638-robotics-ai-techniques)
- OMSCS path: rait/IndianaDrones/
- Assignment implementation scaffold: rait/IndianaDrones/indiana_drones.py
- Evaluation harness: rait/IndianaDrones/testing_suite_indiana_drones.py
- Test scenarios and constraints: rait/IndianaDrones/test_cases.py
- Project brief: rait/IndianaDrones/cs7638-indiana-drones.pdf

## Key Sources on Kalman Filtering and SLAM

1. **Thrun, S., Burgard, W., & Fox, D. (2005).** Probabilistic Robotics. MIT Press. Available: https://mitpress.mit.edu/9780262201629/probabilistic-robotics/

2. **Bzarg, T.** Kalman Filters Explained Simply. Online tutorial: https://bzarg.com/p/reading-sensor-data/

3. **Labbe, R.** Kalman and Bayesian Filters in Python. Comprehensive notebook: https://github.com/rlabbe/filterpy

4. **MIT OpenCourseWare.** 6.S198: Introduction to Nonlinear Filtering. https://ocw.mit.edu/

5. **FilterPy Documentation.** Kalman filtering library for Python: https://filterpy.readthedocs.io/

6. **Welch, G., & Bishop, G. (2006).** An Introduction to the Kalman Filter. UNC Computer Science. https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf

## Reader-Friendly TL;DR

If you're new to SLAM and robotics:

- **Navigation is easy** when the map is perfect and you know where you are
- **Mapping is easy** when your location is perfect
- **Real robots have neither**

SLAM is the method that makes both estimates improve together, step by step, under uncertainty. The Kalman filter is the mathematical engine that powers this feedback loop.

## Policy Note

This writeup intentionally presents methodology, concepts, and analysis only. Assignment solution code is not reproduced here.