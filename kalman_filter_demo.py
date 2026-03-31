#!/usr/bin/env python3
"""
Simple 1D Kalman Filter Demonstration
======================================

This script demonstrates how a Kalman filter works by simulating a robot
moving through a hallway with noisy measurements from GPS and odometry.

The filter elegantly solves the problem: "How do I estimate my true position
when both my motion command execution and sensor readings contain noise?"

Author: Indiana Drones SLAM Project
Course: CS 7638 - Robotics: AI Techniques (OMSCS)
"""

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
        
        Args:
            initial_position: Starting position estimate
            initial_velocity: Starting velocity estimate
            process_noise: How much we expect the system to deviate from predictions
                          (models acceleration, wheel slip, etc.)
            measurement_noise: How much we trust each sensor reading
                              (higher = less trust in measurements)
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
        """Get current position estimate."""
        return self.x[0, 0]
    
    def get_velocity(self):
        """Get current velocity estimate."""
        return self.x[1, 0]
    
    def get_position_uncertainty(self):
        """Get position uncertainty (standard deviation)."""
        return np.sqrt(self.P[0, 0])
    
    def get_velocity_uncertainty(self):
        """Get velocity uncertainty (standard deviation)."""
        return np.sqrt(self.P[1, 1])


def main():
    """Run the Kalman filter simulation and visualization."""
    
    print("=" * 70)
    print("SIMPLE KALMAN FILTER DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Simulate a robot moving through a hallway
    print("Scenario: Robot in a hallway with noisy GPS and odometry")
    print("-" * 70)
    
    np.random.seed(42)
    
    # Ground truth: robot moves at constant velocity
    time_steps = 50
    true_velocity = 0.5  # meters per time step
    true_position = np.zeros(time_steps)
    for t in range(1, time_steps):
        true_position[t] = true_position[t-1] + true_velocity
    
    print(f"True velocity: {true_velocity} m/step")
    print(f"True trajectory: 0 to {true_position[-1]:.1f} meters")
    print()
    
    # Noisy measurements from a sensor (e.g., GPS)
    measurement_noise_std = 1.5  # 1 sigma uncertainty in position
    measurements = true_position + np.random.normal(0, measurement_noise_std, time_steps)
    
    print(f"Measurement noise (1-sigma): {measurement_noise_std} meters")
    print()
    
    # Initialize filter
    print("Initializing Kalman filter...")
    kf = SimpleKalmanFilter1D(
        initial_position=measurements[0],
        initial_velocity=0,
        process_noise=0.01,      # Low process noise = trust motion model
        measurement_noise=measurement_noise_std**2  # Match actual noise
    )
    print(f"Initial position: {kf.get_position():.2f} m")
    print(f"Initial uncertainty: {kf.get_position_uncertainty():.2f} m")
    print()
    
    # Run filter
    print("Running filter cycle: predict -> measure -> update...")
    estimates = []
    uncertainties = []
    
    for t in range(time_steps):
        # Predict: advance based on motion model
        kf.predict()
        
        # Update: incorporate new measurement
        kf.update(measurements[t])
        
        # Store results
        estimates.append(kf.get_position())
        uncertainties.append(kf.get_position_uncertainty())
    
    estimates = np.array(estimates)
    uncertainties = np.array(uncertainties)
    
    print("Filter execution complete.")
    print()
    
    # Calculate performance metrics
    measurement_rmse = np.sqrt(np.mean((measurements - true_position)**2))
    filter_rmse = np.sqrt(np.mean((estimates - true_position)**2))
    improvement = (1 - filter_rmse / measurement_rmse) * 100
    
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Measurement RMSE (raw GPS): {measurement_rmse:.3f} meters")
    print(f"Filter RMSE (Kalman):       {filter_rmse:.3f} meters")
    print(f"Accuracy improvement:       {improvement:.1f}%")
    print()
    
    # Visualization
    plt.figure(figsize=(14, 8))
    
    # Plot 1: Position estimates
    plt.subplot(2, 1, 1)
    plt.plot(true_position, 'g-', linewidth=2.5, label='Ground Truth', zorder=3)
    plt.scatter(range(time_steps), measurements, alpha=0.4, s=30, 
                label=f'Noisy Measurements (σ={measurement_noise_std}m)', zorder=2)
    plt.plot(estimates, 'r-', linewidth=2.5, label='Kalman Filter Estimate', zorder=3)
    plt.fill_between(range(time_steps), 
                     estimates - 2*uncertainties, 
                     estimates + 2*uncertainties,
                     alpha=0.25, color='red', label='95% Confidence Interval', zorder=1)
    plt.xlabel('Time Step')
    plt.ylabel('Position (meters)')
    plt.title('Kalman Filter: Blending Predictions and Noisy Measurements')
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Errors
    plt.subplot(2, 1, 2)
    measurement_error = np.abs(measurements - true_position)
    filter_error = np.abs(estimates - true_position)
    plt.plot(measurement_error, 'b--', linewidth=1.5, alpha=0.7, label='Measurement Error')
    plt.plot(filter_error, 'r-', linewidth=2, label='Filter Error')
    plt.fill_between(range(time_steps), 0, uncertainties, alpha=0.2, color='red', 
                     label='Filter Uncertainty Bounds')
    plt.xlabel('Time Step')
    plt.ylabel('Absolute Error (meters)')
    plt.title('Error Reduction: How the Kalman Filter Improves Estimates')
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('kalman_filter_visualization.png', dpi=150, bbox_inches='tight')
    print("Visualization saved to: kalman_filter_visualization.png")
    plt.show()
    
    print()
    print("=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print()
    print("1. PREDICT: The filter advances position based on velocity estimate")
    print("   → Uses motion model: position(t+1) = position(t) + velocity(t)")
    print()
    print("2. UPDATE: New measurement arrives, filter computes Kalman gain")
    print("   → Gain balances trust in prediction vs measurement based on uncertainty")
    print()
    print("3. COVARIANCE: Filter tracks its own uncertainty")
    print("   → Uncertainty shrinks when measurements confirm predictions")
    print("   → Uncertainty grows when predictions are less reliable")
    print()
    print("4. OPTIMALITY: Kalman gain is mathematically optimal")
    print("   → Minimizes estimation error under Gaussian noise assumptions")
    print("   → Weights are computed, not arbitrary averages")
    print()
    print("This filter is the foundation of all modern robotics navigation systems:")
    print("  • GPS/IMU fusion in smartphones and autonomous vehicles")
    print("  • SLAM (Simultaneous Localization And Mapping)")
    print("  • Apollo Guidance Computer (used to land on the Moon!)")
    print()


if __name__ == '__main__':
    main()
