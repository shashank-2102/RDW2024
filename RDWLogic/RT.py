from RDWLogic.RTSingletonMeta import RTSingletonMeta

class RT(metaclass=RTSingletonMeta):
    # write code that makes a private variable
    # called value and set it to None
    __value = None
    def __init__(self):
        pass

    def get_velocity(self):
        return 15

    def set_velocity(self, velocity):
        return 0

    def is_moving(self):
        return True

    def stop(self):
        return 0

    def get_front_facing_view(self):
        return 0

    def get_rear_facing_view(self):
        return 0

    def is_velocity_equal(self, velocity):
        if self.getVelocity() == velocity:
            return True
        return False

    def relieve_throttle(self):
        return 0

    def apply_brake(self):
        return 0

    def steer(self, direction):
        return 0



