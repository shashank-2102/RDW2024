from Area_Calculator import Calculate_area
#from central_Logic import updateObjectList
class Speed_Limit:
    def __init__(self):
        self._TSpeed = 0
        self._distance = 0
    
    def getDistance(self):
        return self._distance
    
    def getTSpeed(self):
        return self._TSpeed
        
        
    # assuming objects by type has all variables  
    def speed_sign(self, speed, coords):
        if len(coords) != 4:
            print("NO COORDS")
        else:                
                
            #if '10' in objects_by_type_front  && objects_by_type_front['10'][0][3] > 400:
            if speed == 10:
                self._TSpeed = 10
                self._distance =  Calculate_area(['speed sign'
                                                ,coords[0],coords[1],
                                                coords[2],coords[3]])[0]

            #if '15' in objects_by_type_front  && objects_by_type_front['15'][0][3] > 400:
            elif speed == 15:
                self._TSpeed = 15
                self._distance =  Calculate_area(['speed sign'
                                                ,coords[0],coords[1],
                                                coords[2],coords[3]])[0]
                
            #if '20' in objects_by_type_front  && objects_by_type_front['20'][0][3] > 400:
            elif speed == 20:
                self._TSpeed = 20
                self._distance =  Calculate_area(['speed sign'
                                                ,coords[0],coords[1],
                                                coords[2],coords[3]])[0]
            else:
                self.speed_limit_detected = False
                # if -1 it is not detected
                #self.distance = Distance

            # print(self.tSpeed, self.distance, self.speed_limit_detected)
            #return [self.tSpeed, self.distance, self.speed_limit_detected]
            #updateObjectList(self)
            return [self._TSpeed, self._distance]


# data = {
#     '10':[1, 0.2, 0.4, 0.7],
#     '15':[1, 0.2, 0.4, 0.7],
#     '20':[1, 0.2, 0.4, 0.7]
# }
# speed_limit_instance = Speed_Limit()
# speed_limit_instance.speed_sign(data, 0, 0)