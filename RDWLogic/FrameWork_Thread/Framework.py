from FrameWorkSingletonMeta import FrameWorkSingletonMeta

class FrameWork(metaclass=FrameWorkSingletonMeta):

    # All private variables
    __person_detected = False
    __front_car_detected = False
    __traffic_sign_detected = False
    __stopping_line_detected = False
    __obstacle_detected = False
    __traffic_sign_type = []



    def __init__(self, value):
          self.value = value

    # Private method
    def __set_person_detected(self, person_detected):
        self.__person_detected = person_detected

    # Private method
    def __set_front_car_detected(self, front_car_detected):
        self.__front_car_detected = front_car_detected

    # Private method
    def __set_parking_sign_detected(self, parking_sign_detected):
        self.__person_detected = parking_sign_detected

    # Private method
    def __set_traffic_sign_detected(self, parking_sign_detected):
        self.__person_detected = parking_sign_detected

    # Private method
    def __set_traffic_sign_detected_type(self, parking_sign_detected_type):
        self.__person_detected = parking_sign_detected_type


    # Private method
    def __set_obstacle_ahead_detected(self, obstacle_detected):
        self.__obstacle_detected = obstacle_detected

    # Return front view camera image
    def get_front_view(self,):
        return None

    # Return front view camera image
    def get_rear_view(self, ):
        return None

    def main_loop(self):
        return None

    def update_person_detected(self):
        return self.__person_detected


    def update_front_car_detected(self):
        return self.__front_car_detected


    def update_parking_sign_detected(self):
        return self.__person_detected


    def update_traffic_sign_detected(self):
        return self.__traffic_sign_detected

    def update_obstacle_ahead_detected(self,):
        return self.__obstacle_detected




