class Traffic_Sign_Maneouvre:
    def __init__(self):
        self.color = "green"
        self.position = [0,0,0,0]

        #input color, [x1,y1,x2,y2]
        
        #position check (make sure that we are not looking at a traffic light too far away)
        if y1<0.6 and y1>0.2 and x1>0.5: #relative positions for now
            if self.color="green":
                if is_moving():
                    continue
                else:
                    set_velocity(self, get_velocity(self))
                #if car is not moving, find last speed limit and tell car to go at that speed limit

            elif self.color="red":
                if not is_moving():
                    continue
                elif is_moving() and y1<0.4: #arbitrary value
                    stop()
            else:
            print('the color of the traffic light is neither green or red') #debuging statement
            return
