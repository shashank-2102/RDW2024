from Distance_Calculator import Calculate_area
from RT import RT

class Traffic_Light:
    _distance = 0
    _TSpeed = 0
    
    def __init__(self):
        # Logic
        self.__lane_keeping_maneouvre = None
        self.RT = RT()

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
                if self.RT.is_moving_TF: ###this needs to be changed to a function that can get the velocity of the car
                    pass

                else:
                    self._TSpeed = 10
                #if car is not moving, find last speed limit and tell car to go at that speed limit

            elif color == "red":
                if not self.RT.is_moving_TF:
                    pass
                elif self.RT.is_moving_TF and y1<0.4: #arbitrary value
                    self._TSpeed = 0

            else:
                print('the color of the traffic light is neither green or red') #debuging statement
            
            self._distance = Calculate_area(['traffic light',x1,y1,x2,y2])[0]
            
            #print(self._TSpeed, self._distance)
            return [self._TSpeed, self._distance]
        


# traffic_light_instance = Traffic_Light()
# color2 = "green"
# coordinates2 = [0.6, 0.3, 0.7, 0.5]
# traffic_light_instance.TL_Logic(color2, coordinates2)
# print(traffic_light_instance.TL_Logic(color2, coordinates2))