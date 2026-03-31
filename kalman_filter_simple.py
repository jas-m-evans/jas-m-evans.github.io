#!/usr/bin/env python3
"""
Simple 1D Kalman Filter - Pure Python (no NumPy required)
==========================================================

This version demonstrates the Kalman filter using only Python's built-in
math library, so it can run anywhere Python is installed.

It shows how the filter blends noisy measurements with predictions to
estimate true position.
"""

import math
import random


class SimpleKalmanFilter1D:
    """A 1D Kalman filter that doesn't require NumPy."""
    
    def __init__(self, initial_position=0.0, process_noise=0.01, measurement_noise=1.0):
        """
        Initialize the filter.
        
        Args:
            initial_position: Starting position estimate
            process_noise: Expected system deviation (lower = trust motion model more)
            measurement_noise: Measurement uncertainty (lower = trust sensors more)
        """
        self.x = initial_position  # Position estimate
        self.v = 0.0               # Velocity estimate
        
        # Uncertainty (covariance)
        self.p_pos = 0.5           # Position uncertainty
        self.p_vel = 0.5           # Velocity uncertainty
        
        # Noise parameters
        self.q = process_noise
        self.r = measurement_noise
    
    def predict(self, delta_t=1.0):
        """Prediction: advance state based on motion model."""
        # Update position: x = x + v*dt
        self.x = self.x + self.v * delta_t
        
        # Update velocity (no acceleration assumed)
        # self.v stays the same
        
        # Update uncertainty (grows with time)
        self.p_pos = self.p_pos + self.q
        self.p_vel = self.p_vel + self.q
    
    def update(self, measurement):
        """Update: incorporate a new measurement."""
        # Innovation (difference between measurement and prediction)
        innovation = measurement - self.x
        
        # Innovation covariance (total uncertainty)
        s = self.p_pos + self.r
        
        # Kalman gain (how much to trust this measurement)
        # High gain = trust measurement, low gain = trust prediction
        k = self.p_pos / s
        
        # Update position estimate (blend prediction and measurement)
        self.x = self.x + k * innovation
        
        # Update uncertainty (shrinks after measurement)
        self.p_pos = (1 - k) * self.p_pos
    
    def get_position(self):
        """Get current position estimate."""
        return self.x
    
    def get_uncertainty(self):
        """Get position uncertainty (standard deviation)."""
        return math.sqrt(max(0, self.p_pos))


def main():
    """Run the Kalman filter demonstration."""
    
    print("=" * 70)
    print("KALMAN FILTER DEMONSTRATION (Pure Python - No NumPy Required)")
    print("=" * 70)
    print()
    
    # Simulation parameters
    random.seed(42)
    time_steps = 20
    true_velocity = 0.5  # meters per step
    measurement_noise_std = 1.5
    
    print(f"Scenario: Robot moving at {true_velocity} m/step with noisy measurements")
    print(f"Measurement noise: ±{measurement_noise_std} meters (1-sigma)")
    print()
    
    # Ground truth trajectory
    true_positions = [0.0]
    for t in range(1, time_steps):
        true_positions.append(true_positions[-1] + true_velocity)
    
    # Generate noisy measurements
    measurements = [
        p + random.gauss(0, measurement_noise_std) 
        for p in true_positions
    ]
    
    # Run filter
    kf = SimpleKalmanFilter1D(
        initial_position=measurements[0],
        process_noise=0.01,
        measurement_noise=measurement_noise_std ** 2
    )
    
    estimates = []
    uncertainties = []
    
    print("Time | True Pos | Measurement | Estimate | Uncertainty | Error")
    print("-" * 70)
    
    measurement_errors = []
    filter_errors = []
    
    for t in range(time_steps):
        # Predict
        kf.predict()
        
        # Update with measurement
        kf.update(measurements[t])
        
        # Record results
        estimate = kf.get_position()
        uncertainty = kf.get_uncertainty()
        estimates.append(estimate)
        uncertainties.append(uncertainty)
        
        # Calculate errors
        meas_error = abs(measurements[t] - true_positions[t])
        filt_error = abs(estimate - true_positions[t])
        measurement_errors.append(meas_error)
        filter_errors.append(filt_error)
        
        # Print row
        print(f"{t:4d} | {true_positions[t]:8.2f} | {measurements[t]:11.2f} | "
              f"{estimate:8.2f} | {uncertainty:11.2f} | {filt_error:5.2f}")
    
    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print()
    
    # Calculate metrics
    avg_meas_error = sum(measurement_errors) / len(measurement_errors)
    avg_filt_error = sum(filter_errors) / len(filter_errors)
    improvement = (1 - avg_filt_error / avg_meas_error) * 100
    
    print(f"Average measurement error: {avg_meas_error:.3f} meters")
    print(f"Average filter error:      {avg_filt_error:.3f} meters")
    print(f"Improvement:               {improvement:.1f}%")
    print()
    
    # ASCII visualization
    print("=" * 70)
    print("VISUALIZATION (ASCII)")
    print("=" * 70)
    print()
    print("Position estimates over time:")
    print()
    
    # Normalize for display
    min_pos = min(true_positions + measurements + estimates) - 5
    max_pos = max(true_positions + measurements + estimates) + 5
    width = 60
    
    for t in range(time_steps):
        # Normalize positions to screen width
        true_norm = int((true_positions[t] - min_pos) / (max_pos - min_pos) * width)
        meas_norm = int((measurements[t] - min_pos) / (max_pos - min_pos) * width)
        est_norm = int((estimates[t] - min_pos) / (max_pos - min_pos) * width)
        
        # Build display line
        line = [' '] * width
        
        # Mark positions (avoiding overwrites with priority: estimate > measurements > truth)
        if 0 <= true_norm < width:
            line[true_norm] = 'G'  # Ground truth
        if 0 <= meas_norm < width:
            line[meas_norm] = 'M'  # Measurement
        if 0 <= est_norm < width:
            line[est_norm] = 'E'  # Estimate
        
        print(f"t={t:2d} |{''.join(line)}|")
    
    print("     G=Ground truth, M=Measurement, E=Filter Estimate")
    print()
    print("=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print()
    print("1. The filter starts uncertain but quickly converges")
    print("2. Estimates (E) track ground truth (G) better than raw measurements (M)")
    print("3. This happens because the filter learns to weight predictions vs measurements")
    print("4. The Kalman gain automatically computes optimal weighting")
    print()
    print("This same algorithm powers autonomous vehicles, drones, and smartphones!")
    print()


if __name__ == '__main__':
    main()
