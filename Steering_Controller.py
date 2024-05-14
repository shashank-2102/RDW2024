import numpy as np

class Controller():
    def __init__(
        self,   
    ):
        self.wheel_base = 1.686
        self.lookahead = 3
        self.lookahead_Rear = 4
        
    def feedforward(self, polynomial):
        x1, x2, x3, x4 = polynomial
        x_pos = 1200
        first_derivative = 3 * x1 * x_pos ** 2 + 2 * x2 * x_pos + x3
        second_derivative = 6 * x1 * x_pos + 2 * x2
        ki = second_derivative/(1 + first_derivative)
        dff = ki * self.wheel_base
        
        return dff

    def feedback(self, angle, lateral_error):
        k1 = 2 * self.wheel_base / self.lookahead_Rear #
        k2 = k1 * self.lookahead
        dfi = - k1 * lateral_error + k2 * angle
        return dfi