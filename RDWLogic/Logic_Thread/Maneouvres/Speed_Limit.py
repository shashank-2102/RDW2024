class Speed_Limit:
    tSpeed = 0
    speed_limit_detected = False
   
    def __init__(self):
        pass

    def getTSpeed(self):
        return self.tSpeed
    
    def signal_detected(self):
        return self.speed_limit_detected
