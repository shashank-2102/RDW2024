class Speed_Limit:
   
    def __init__(self):
        self.tSpeed = 0
        self.distance = 0
        self.speed_limit_detected = False
    
    def getDistance(self):
        return self._distance
    
    def getTSpeed(self):
        return self._TSpeed
        
    # assuming objects by type has all variables  
    def speed_sign(self, objects_by_type, tSpeed, Distance):
        
        
        #if '10' in objects_by_type_front  && objects_by_type_front['10'][0][3] > 400:
        if objects_by_type['10']:
            self.tSpeed = 10
            self.speed_limit_detected = True
            self.distance = 0
        #if '15' in objects_by_type_front  && objects_by_type_front['15'][0][3] > 400:
        elif objects_by_type['15'] and self.speed_limit_detected == False:
            self.tSpeed = 15
            self.speed_limit_detected = True
            self.distance = 0
        #if '20' in objects_by_type_front  && objects_by_type_front['20'][0][3] > 400:
        elif objects_by_type['20'] and self.speed_limit_detected == False:
            self.tSpeed = 20
            self.speed_limit_detected = True
            self.distance = 0
        else:
            self.speed_limit_detected = False
            self.tSpeed = tSpeed
            # if -1 it is not detected
            self.distance = Distance
        return (self.speed_limit_detected, self.tSpeed, self.distance)
