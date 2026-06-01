#!/usr/bin/env python3
"""Public-safe Kalman filter sample with plotting."""

import numpy as np
import matplotlib.pyplot as plt


class SimpleKalmanFilter1D:
    """A 1D Kalman filter for tracking position."""

    def __init__(self, initial_position=0, initial_velocity=0, process_noise=0.01, measurement_noise=1.0):
        self.x = np.array([[initial_position], [initial_velocity]])  # [position, velocity]
        self.P = np.eye(2) * 0.5
        self.F = np.array([[1, 1], [0, 1]])
        self.H = np.array([[1, 0]])
        self.Q = np.eye(2) * process_noise
        self.R = np.array([[measurement_noise]])

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z):
        y = np.array([[z]]) - self.H @ self.x
        s = self.H @ self.P @ self.H.T + self.R
        k = self.P @ self.H.T @ np.linalg.inv(s)
        self.x = self.x + k @ y
        self.P = (np.eye(2) - k @ self.H) @ self.P

    def get_position(self):
        return self.x[0, 0]

    def get_uncertainty(self):
        return np.sqrt(self.P[0, 0])


def main():
    np.random.seed(42)
    time_steps = 50
    true_velocity = 0.5

    true_position = np.zeros(time_steps)
    for t in range(1, time_steps):
        true_position[t] = true_position[t - 1] + true_velocity

    measurement_noise_std = 1.5
    measurements = true_position + np.random.normal(0, measurement_noise_std, time_steps)

    kf = SimpleKalmanFilter1D(
        initial_position=measurements[0],
        initial_velocity=0,
        process_noise=0.01,
        measurement_noise=measurement_noise_std**2,
    )

    estimates, uncertainties = [], []
    for t in range(time_steps):
        kf.predict()
        kf.update(measurements[t])
        estimates.append(kf.get_position())
        uncertainties.append(kf.get_uncertainty())

    estimates = np.array(estimates)
    uncertainties = np.array(uncertainties)

    plt.figure(figsize=(12, 6))
    plt.plot(true_position, "g-", linewidth=2, label="Ground Truth")
    plt.scatter(range(time_steps), measurements, alpha=0.5, s=20, label="Noisy Measurements")
    plt.plot(estimates, "r-", linewidth=2, label="Kalman Filter Estimate")
    plt.fill_between(
        range(time_steps),
        estimates - 2 * uncertainties,
        estimates + 2 * uncertainties,
        alpha=0.2,
        color="red",
        label="95% Confidence Interval",
    )
    plt.xlabel("Time Step")
    plt.ylabel("Position")
    plt.legend()
    plt.title("Kalman Filter: Blending Predictions and Noisy Measurements")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("kalman_filter_visualization.png", dpi=150)
    plt.show()

    meas_rmse = np.sqrt(np.mean((measurements - true_position) ** 2))
    filt_rmse = np.sqrt(np.mean((estimates - true_position) ** 2))
    improvement = (1 - filt_rmse / meas_rmse) * 100
    print(f"Measurement RMSE: {meas_rmse:.3f}")
    print(f"Filter RMSE: {filt_rmse:.3f}")
    print(f"Accuracy improvement: {improvement:.1f}%")


if __name__ == "__main__":
    main()
