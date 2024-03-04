class Pedestrian_Maneouvre:
    
    _distance = 0
    _TSpeed = False
    
    def __init__(self):
        self.pedestrian_sign_detected = False
        self.pedestrian_detected = False
        self.pedestrian_crossing_detected = False


    def getDistance(self):
        return self._distance
    
    def getTSpeed(self):
        return self._TSpeed
    
        
    def pedestrian_sign(self):
        
        #to make sure that we are not looking at a pedestrian sign too far away
        if y1<0.6 and y1>0.2 and x1>0.5:  #relative positions for now
            self.pedestrian_sign_detected = True
            
    def pedestrian(self):
        
        #to make sure that we are not looking at a pedestrian too far away
        if y2<0.6 and y2>0.2 and x2>0.5:  #relative positions for now
            self.pedestrian_detected = True
    
    def pedestrian_crossing(self):
        
        #to make sure that we are not looking at a pedestrian crossing too far away
        if y3<0.6 and y3>0.2 and x3>0.5:  #relative positions for now
            self.pedestrian_crossing_detected = True
    
    def pedestrian_logic(self):
    
        if not self.pedestrian_detected:
            if is_moving():
                continue
            else:
                self._TSpeed =  get_velocity(self)   #no pedestrian found, keep moving or start moving
        
        elif self.pedestrian_sign_detected:   
            if is_moving() and y1<0.4:    #arbitrary value
                self._TSpeed = 0
            elif not is_moving():
                continue    #pedestrian found and pedestrian sign found, stop if the car is within a distance
            
        elif self.pedestrian_crossing_detected:
            if is_moving() and y3<0.4:    #arbitrary value
                self._TSpeed = 0
            elif not is_moving():
                continue    #pedestrian found and pedestrian crossing found, stop if the car is within a distance
        
        else:
            print('no pedestrian crossing or pedestrian sign detected')
            continue
        return self._TSpeed, self._distance
            
            
                
            
            
    
    

            
     

