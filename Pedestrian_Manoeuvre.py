from RT import RT
from Area_Calculator import Calculate_area
from FrameWorkSingletonMeta import FrameWorkSingletonMeta
#from central_Logic import updateObjectList
class Pedestrian_Maneouvre:
    
    def __init__(self):
        self.pedestrian_detected = False
        self.pedestrian_crossing_detected = False
        self._distance = 0
        self._TSpeed = 0
        self.RT = RT()

    def getDistance(self):
        return self._distance
    
    def getTSpeed(self):
        return self._TSpeed
            
    def pedestrian_check(self, coordinates):
        x1, y1, x2, y2 = coordinates
        
        #to make sure that we are not looking at a pedestrian too far away
        if y1<0.6 and y1>0.2 and x1>0.5:  #relative positions for now
            self.pedestrian_detected = True
        return self.pedestrian_detected
    
    def pedestrian_crossing_check(self, coordinates):
        x3, y3, x4, y4 = coordinates
        
        self._distance = Calculate_area(['zebra crossing',x3,y3,x4,y4])[0]
        #to make sure that we are not looking at a pedestrian crossing too far away
        if y3<0.6 and y3>0.2 and x3>0.5:  #relative positions for now
            self.pedestrian_crossing_detected = True
        return self.pedestrian_crossing_detected
    
    def pedestrian_logic(self, pedestrian_detected, pedestrian_crossing_detected):
    
        if not pedestrian_detected:
            if False: #self.RT.is_moving():
                pass
            else:
                self._TSpeed =  50
                #self._TSpeed =  self.RT.get_velocity()   #no pedestrian found, keep moving or start moving
            
        elif pedestrian_crossing_detected:
            if True:    #arbitrary value
                self._TSpeed = 0
                #self._TSpeed = 0
            elif not self.RT.is_moving():
                pass    #pedestrian found and pedestrian crossing found, stop if the car is within a distance
        
        else:
            print('no pedestrian crossing or pedestrian sign detected')
            pass
        #updateObjectList(self)
        return [self._TSpeed, self._distance]
            
            
                
            
            
    
    

            
     

