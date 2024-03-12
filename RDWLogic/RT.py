from RDWLogic.RTSingletonMeta import RTSingletonMeta

class RT(metaclass=RTSingletonMeta):
    # write code that makes a private variable
    # called value and set it to None
    __value = None
    velocity = 0
    is_moving_TF = False
    def __init__(self, velocity=0, is_moving=False):
        self.velocity = velocity
        self.is_moving_TF = is_moving
        pass

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        return 0

    def is_moving(self):
        return self.is_moving

    def stop(self):
        return 0

    def get_front_facing_view(self):
        return 0

    def get_rear_facing_view(self):
        return 0

    def is_velocity_equal(self, velocity):
        if self.get_velocity() == velocity:
            return True
        return False

    def relieve_throttle(self):
        return 0

    def apply_brake(self):
        return 0

    def steer(self, direction):
        return 0



