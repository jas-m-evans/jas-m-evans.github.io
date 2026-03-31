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

## A Simple Kalman Filter in Python

To make this concrete, here's a minimal 1D Kalman filter that demonstrates the predict-update cycle. Imagine a robot is trying to track its position along a hallway. It has wheel odometry (which drifts) and occasional GPS readings (which are noisy). The Kalman filter blends these two imperfect sources into a better estimate.

```python
import numpy as np
import matplotlib.pyplot as plt

class SimpleKalmanFilter1D:
    """
    A 1D Kalman filter for tracking position.
    
    State: position (x) and velocity (v)
    Measurements: noisy position observations
    """
    
    def __init__(self, initial_position=0, initial_velocity=0, 
                 process_noise=0.01, measurement_noise=1.0):
        """
        Initialize the filter.
        
        process_noise: How much we expect the system to deviate from predictions
                       (models acceleration, wheel slip, etc.)
        measurement_noise: How much we trust each sensor reading
        """
        # State vector: [position, velocity]
        self.x = np.array([[initial_position], [initial_velocity]])
        
        # Covariance matrix: uncertainty in [position, velocity]
        self.P = np.eye(2) * 0.5
        
        # State transition matrix: position += velocity * dt (dt=1 for simplicity)
        self.F = np.array([[1, 1],
                          [0, 1]])
        
        # Measurement matrix: we observe position only
        self.H = np.array([[1, 0]])
        
        # Process noise covariance
        self.Q = np.eye(2) * process_noise
        
        # Measurement noise covariance
        self.R = np.array([[measurement_noise]])
    
    def predict(self):
        """Prediction step: advance the state based on motion model."""
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
    
    def update(self, z):
        """
        Update step: incorporate a new measurement.
        
        This is where the magic happens. The filter computes the Kalman gain,
        which tells us how much to trust the measurement vs. the prediction.
        """
        # Innovation: difference between measured and predicted observation
        y = np.array([[z]]) - self.H @ self.x
        
        # Innovation covariance: uncertainty in the innovation
        S = self.H @ self.P @ self.H.T + self.R
        
        # Kalman gain: how much weight to give the measurement
        # If measurement noise is low (trusted), gain is high (trust measurement)
        # If process noise is low (confident in prediction), gain is low (trust prediction)
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Update state: blend prediction and measurement
        self.x = self.x + K @ y
        
        # Update covariance: express new uncertainty
        self.P = (np.eye(2) - K @ self.H) @ self.P
    
    def get_position(self):
        return self.x[0, 0]
    
    def get_uncertainty(self):
        return np.sqrt(self.P[0, 0])  # Standard deviation in position


# Simulate a robot moving through a hallway
np.random.seed(42)

# Ground truth: robot moves at constant velocity
time_steps = 50
true_velocity = 0.5
true_position = np.zeros(time_steps)
for t in range(1, time_steps):
    true_position[t] = true_position[t-1] + true_velocity

# Noisy measurements from a sensor (e.g., GPS)
measurement_noise_std = 1.5
measurements = true_position + np.random.normal(0, measurement_noise_std, time_steps)

# Initialize filter
kf = SimpleKalmanFilter1D(
    initial_position=measurements[0],
    initial_velocity=0,
    process_noise=0.01,
    measurement_noise=measurement_noise_std**2
)

# Run filter
estimates = []
uncertainties = []

for t in range(time_steps):
    kf.predict()
    kf.update(measurements[t])
    estimates.append(kf.get_position())
    uncertainties.append(kf.get_uncertainty())

estimates = np.array(estimates)
uncertainties = np.array(uncertainties)

# Visualize results
plt.figure(figsize=(12, 6))

# Plot true trajectory
plt.plot(true_position, 'g-', linewidth=2, label='Ground Truth')

# Plot noisy measurements
plt.scatter(range(time_steps), measurements, alpha=0.5, s=20, label='Noisy Measurements')

# Plot Kalman filter estimate with uncertainty bounds
plt.plot(estimates, 'r-', linewidth=2, label='Kalman Filter Estimate')
plt.fill_between(range(time_steps), 
                 estimates - 2*uncertainties, 
                 estimates + 2*uncertainties,
                 alpha=0.2, color='red', label='95% Confidence Interval')

plt.xlabel('Time Step')
plt.ylabel('Position')
plt.legend()
plt.title('Kalman Filter: Blending Predictions and Noisy Measurements')
plt.grid(True, alpha=0.3)
plt.show()

# Print results
print(f"Measurement RMSE: {np.sqrt(np.mean((measurements - true_position)**2)):.3f}")
print(f"Filter RMSE: {np.sqrt(np.mean((estimates - true_position)**2)):.3f}")
print(f"Accuracy improvement: {(1 - np.sqrt(np.mean((estimates - true_position)**2)) / np.sqrt(np.mean((measurements - true_position)**2))) * 100:.1f}%")
```

**What's happening here:**

1. **Predict**: The filter advances the state using a motion model (position increases by velocity).
2. **Update**: A noisy measurement arrives. The filter computes a **Kalman gain** that answers: "Should I more heavily weight my prediction or this measurement?"
3. **Covariance tracking**: The filter tracks uncertainty (variance) in both position and velocity. As measurements confirm the prediction, uncertainty shrinks. When predictions drift, uncertainty grows.
4. **Result**: The filtered trajectory is much smoother and closer to ground truth than the raw measurements alone.

In the visualization, notice how the filter's confidence bounds (red shaded region) compress as measurements accumulate, then widen when fewer independent observations arrive. This adaptive uncertainty quantification is the heart of robustness.

For a 1D hallway, the improvement is modest. But in 6D pose space with 20 landmark coordinates added to the state vector (as in the drone SLAM problem), the multiplier effect of uncertainty propagation is enormous. This is why Kalman-style filters power every GPS/IMU fusion, every smartphone positioning system, and every autonomous vehicle.

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

{% comment %}
Internal references (hidden from rendered page):
- OMSCS path: rait/IndianaDrones/
- Assignment implementation scaffold: rait/IndianaDrones/indiana_drones.py
- Evaluation harness: rait/IndianaDrones/testing_suite_indiana_drones.py
- Test scenarios and constraints: rait/IndianaDrones/test_cases.py
- Project brief: rait/IndianaDrones/cs7638-indiana-drones.pdf
{% endcomment %}

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