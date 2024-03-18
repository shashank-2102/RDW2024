# from Distance_Calculator import Calculate_area
from RT import RT
class Traffic_Light:
    _distance = 0
    _TSpeed = 0
    def __init__(self):
        # Logic
        self.__lane_keeping_maneouvre = None
        self.RT = RT()

    def MEW(self):
        return self._TSpeed

    def getTSpeed(self):
        return self._TSpeed

    def getDistance(self):
        return self._distance
    
    #color: green, red
    #coordiantes: [x1,y1,x2,y2]
    def  TL_Logic(self, color, coordinates):
        x1,y1,x2,y2 = coordinates
        #position check (make sure that we are not looking at a traffic light too far away)

        if y1 < 0.6 and y1 > 0.2 and x1 > 0.5: #relative positions for now

            if color == "green":
                if self.RT.is_moving(): ###this needs to be changed to a function that can get the velocity of the car

                    pass

                else:

                    self._TSpeed = 10
                    self.RT.get_velocity()
                #if car is not moving, find last speed limit and tell car to go at that speed limit

            elif color == "red":
                if not self.RT.is_moving():
                    pass

                elif self.RT.is_moving() and y1<0.4: #arbitrary value
                    self._TSpeed = 10
                print(y1)
            else:
                print('the color of the traffic light is neither green or red') #debuging statement
            self._distance = Calculate_area(['traffic light',x1,y1,x2,y2])
            return self._TSpeed, self._distance
        



