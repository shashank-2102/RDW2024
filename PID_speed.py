class PIDController_speed:
    
    def __init__(
        self,
        kp,  # proportional
        ki,  # integral
        kd,  # derivative
        m,
        b,
    ):
        """Initialize the PID controller."""
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.m = m
        self.b = b

        # set initial conditions
        self.v = 0
        self.old_e = 0  # to store error from last step
        self.E = 0  # to store error accumulation
    
    def reset(self):
        """Reset the controller state."""
        self.v = 0
        self.old_e = 0
        self.E = 0

    def update(self, speed_limit, dt):
    # designing PID controller
    # mv_dot + bv = u
    
        e = speed_limit - self.v     # proportional error
        e_dot = e - self.old_e       # error change
        self.E = (self.E + e) * dt    # integral error
        
        u = self.kp * e + self.kd * e_dot + self.ki * self.E
        self.old_e = speed_limit - self.v
        self.v = (u * dt + self.m * self.v) / (self.m + self.b * self.v)
        
        return self.v

