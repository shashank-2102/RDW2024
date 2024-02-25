class Pedestrian_Maneouvre:
    def __init__(self):
        self.pedestrian_sign_detected = False
        self.pedestrian_detected = False
        self.pedestrian_crossing_detected = False
        
    def pedestrian_sign(self):
        
        #to make sure that we are not looking at a pedestrian sign too far away
        if y1<0.6 and y1>0.2 and x1>0.5:  #relative positions for now
            self.pedestrian_sign_detected = True
            
    def pedestrian(self):
        
        #to make sure that we are not looking at a pedestrian too far away
        if y1<0.6 and y1>0.2 and x1>0.5:  #relative positions for now
            self.pedestrian_detected = True
    
    def pedestrian_crossing(self):
        
        #to make sure that we are not looking at a pedestrian crossing too far away
        if y1<0.6 and y1>0.2 and x1>0.5:  #relative positions for now
            self.pedestrian_crossing_detected = True
    
    def pedestrian_manoeuvre(self):
    
        if not self.pedestrian_detected:
            if is_moving():
                continue
            else:
                set_velocity(self, get_velocity(self))   #no pedestrian found, keep moving or start moving
        
        elif self.pedestrian_sign_detected:   
            if is_moving() and y1<0.4:    #arbitrary value
                stop()
            elif not is_moving():
                continue    #pedestrian found and pedestrian sign found, stop if the car is within a distance
            
        elif self.pedestrian_crossing_detected:
            if is_moving() and y1<0.4:    #arbitrary value
                stop()
            elif not is_moving():
                continue    #pedestrian found and pedestrian crossing found, stop if the car is within a distance
        
        else:
            print('no pedestrian crossing or pedestrian sign detected')
            continue
        return
            
            
                
            
            
    
    

            
     

