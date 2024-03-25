from RT import RT
from FrameWorkSingletonMeta import FrameWorkSingletonMeta
class Pedestrian_Maneouvre:
    
    _distance = 0
    _TSpeed = False
    
    def __init__(self):
        self.pedestrian_sign_detected = False
        self.pedestrian_detected = False
        self.pedestrian_crossing_detected = False
        self.RT = RT()


    def getDistance(self):
        return self._distance
    
    def getTSpeed(self):
        return self._TSpeed
    
        
    def pedestrian_sign_check(self, coordinates):
        x1, y1, x2, y2 = coordinates
        
        #to make sure that we are not looking at a pedestrian sign too far away
        if y1<0.6 and y1>0.2 and x1>0.5:  #relative positions for now
            self.pedestrian_sign_detected = True
        return self.pedestrian_sign_detected
            
    def pedestrian_check(self, coordinates):
        x3, y3, x4, y4 = coordinates
        
        #to make sure that we are not looking at a pedestrian too far away
        if y3<0.6 and y3>0.2 and x3>0.5:  #relative positions for now
            self.pedestrian_detected = True
        return self.pedestrian_detected
    
    def pedestrian_crossing_check(self, coordinates):
        x5, y5, x6, y6 = coordinates
        
        #to make sure that we are not looking at a pedestrian crossing too far away
        if y5<0.6 and y5>0.2 and x5>0.5:  #relative positions for now
            self.pedestrian_crossing_detected = True
        return self.pedestrian_crossing_detected
    
    def pedestrian_logic(self, pedestrian_detected, pedestrian_sign_detected, pedestrian_crossing_detected):
    
        if not pedestrian_detected:
            if False: #self.RT.is_moving():
                pass
            else:
                self._TSpeed =  50
                #self._TSpeed =  self.RT.get_velocity()   #no pedestrian found, keep moving or start moving

        elif pedestrian_sign_detected:   
            if True: #self.RT.is_moving() and y1<0.4:    #arbitrary value
                self._TSpeed = 0
                #self._TSpeed = 0
            elif False: #not self.RT.is_moving():
                pass    #pedestrian found and pedestrian sign found, stop if the car is within a distance
            
        elif pedestrian_crossing_detected:
            if self.RT.is_moving() and y3<0.4:    #arbitrary value
                self._TSpeed = 0
                #self._TSpeed = 0
            elif not self.RT.is_moving():
                pass    #pedestrian found and pedestrian crossing found, stop if the car is within a distance
        
        else:
            print('no pedestrian crossing or pedestrian sign detected')
            pass
        return [self._TSpeed, self._distance]
            
            
                
            
            
    
    

            
     

