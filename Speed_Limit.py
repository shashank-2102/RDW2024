from Area_Calculator import Calculate_area
#from central_Logic import updateObjectList
class Speed_Limit:
    def __init__(self):
        self._TSpeed = 0
        self._distance = 0
        self.speed_limit_detected = False
    
    def getDistance(self):
        return self._distance
    
    def getTSpeed(self):
        return self._TSpeed
        
        
    # assuming objects by type has all variables  
    def speed_sign(self, objects_by_type, _TSpeed, _distance):
        
        
        #if '10' in objects_by_type_front  && objects_by_type_front['10'][0][3] > 400:
        if objects_by_type['10']:
            self._TSpeed = 10
            self.speed_limit_detected = True
            self._distance =  Calculate_area(['speed sign'
                                             ,objects_by_type['10'][0],objects_by_type['10'][1],
                                             objects_by_type['10'][2],objects_by_type['10'][3]])[0]

        #if '15' in objects_by_type_front  && objects_by_type_front['15'][0][3] > 400:
        elif objects_by_type['15']: #and self.speed_limit_detected == False:
            self._TSpeed = 15
            self.speed_limit_detected = True
            self._distance =  Calculate_area(['speed sign'
                                             ,objects_by_type['15'][0],objects_by_type['15'][1],
                                             objects_by_type['15'][2],objects_by_type['15'][3]])[0]
            
        #if '20' in objects_by_type_front  && objects_by_type_front['20'][0][3] > 400:
        elif objects_by_type['20']: #and self.speed_limit_detected == False:
            self._TSpeed = 20
            self.speed_limit_detected = True
            self._distance =  Calculate_area(['speed sign'
                                             ,objects_by_type['20'][0],objects_by_type['20'][1],
                                             objects_by_type['20'][2],objects_by_type['20'][3]])[0]
        else:
            self.speed_limit_detected = False
            self._TSpeed = _TSpeed
            # if -1 it is not detected
            #self.distance = Distance

        # print(self.tSpeed, self.distance, self.speed_limit_detected)
        #return [self.tSpeed, self.distance, self.speed_limit_detected]
        #updateObjectList(self)
        return [self._TSpeed, self.speed_limit_detected]


# data = {
#     '10':[1, 0.2, 0.4, 0.7],
#     '15':[1, 0.2, 0.4, 0.7],
#     '20':[1, 0.2, 0.4, 0.7]
# }
# speed_limit_instance = Speed_Limit()
# speed_limit_instance.speed_sign(data, 0, 0)