class PIDController_steering:
    def __init__(
        self,
        kp,
        ki,
        kd,
        setpoint=0,  # Point on the center line
        integral_limit=None,   # Boundary distance, to ensure error accumulation within the lane boundary
        derivative_filter_tau=0.0,
    ):
        """Initialize the PID controller with gains, setpoint, and enhancements."""
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.setpoint = setpoint  # Desired setpoint

        self.integral_limit = (
            integral_limit  # Limit for the integral term
        )
        self.derivative_filter_tau = (
            derivative_filter_tau  # Time constant for derivative low-pass filter
        )

        self.last_error = 0.0  # Last error value
        self.integral = 0.0  # Integral of error
        self.derivative_filtered = 0.0  # Filtered derivative

    def reset(self):
        """Reset the controller state."""
        self.last_error = 0.0
        self.integral = 0.0
        self.derivative_filtered = 0.0

    def update(self, current_value, dt):
        """Update the PID controller with enhancements."""
        # Calculate error
        error = self.setpoint - current_value

        # Proportional term
        P = self.kp * error

        # Integral term with anti-windup
        self.integral = self.integral + error * dt
        if self.integral_limit is not None:
            self.integral = max(
                min(self.integral, self.integral_limit), -self.integral_limit
            )
        I = self.ki * self.integral

        # Derivative term with filtering
        derivative_raw = (error - self.last_error) / dt
        self.derivative_filtered += (
            (derivative_raw - self.derivative_filtered)
            * dt
            / (self.derivative_filter_tau + dt)
            if self.derivative_filter_tau > 0
            else derivative_raw
        )
        D = self.kd * self.derivative_filtered

        # Remember last error for next derivative calculation
        self.last_error = error

        # Calculate total control output
        control_action = P + I + D
        steering_angle = control_action #*2   # Scale the control actions

        return steering_angle
