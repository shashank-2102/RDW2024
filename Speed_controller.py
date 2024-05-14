class Controller_speed:
    
    def __init__(self):

        self.v = [0]   # speed output
        self.a = [0]    # acceleration output
        self.t = 0      # specific time
        self.time = 0   # total time
        self.speed_limit = [0]    # new detected speed limit
        self.cases = 0            
        self.i = 1
        self.error = 0
    
    def reset(self):
        """Reset the controller state."""
        self.v = [0]
        self.a = [0]
        self.t = 0
        self.time = 0
        self.speed_limit = [0]
        self.cases = 0
        self.i = 1
        self.error = 0
    
    # update new speed_limit
    def update(self, speed_limit, dt):
        import numpy as np
        
        self.speed_limit.append(speed_limit)
        if self.speed_limit[self.i] != self.speed_limit[self.i-1]:
            self.error = self.speed_limit[self.i] - self.v[self.i-1]
        
            if self.v[self.i-1] == self.speed_limit[self.i]:
                self.v.append(self.v[self.i-1])
                self.a.append(0)
                
            else:
                if self.error > 0:
                    if self.a[self.i-1] == 0:
                        if self.error <= 2.25:
                            self.time = 2 * (np.sqrt(self.error))
                            self.a.append(dt * 1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 1       # self.error>0, a(self.i-1)=0, self.error<=2.25, case 1
                            
                        else:
                            self.time = 3 + (self.error-2.25)/1.5
                            self.a.append(dt * 1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 2       # self.error>0, a(self.i-1)=0, self.error>2.25, case 2
                            
                    elif self.a[self.i-1] > 0:
                        if self.error == 0.5 * (self.a[self.i-1])**2:
                            self.time = self.a[self.i-1] * 1
                            self.a.append(self.a[self.i-1] - dt*1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 3       # self.error>0, a(self.i-1)>0, self.error=0.5*a(self.i-1)^2, case 3
                        
                        elif self.error < 0.5 * (self.a[self.i-1])**2:
                            self.time = self.a[self.i-1] + 2 * np.sqrt(0.5 * (self.a[self.i-1])**2 - self.error)
                            self.a.append(self.a[self.i-1] - dt*1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 4       # self.error>0, a(self.i-1)>0, self.error<0.5*a(self.i-1)^2, case 4
                        
                        else:
                            if self.a[self.i-1] == 1.5:
                                self.time = 1.5 + (self.error-1.125)/1.5
                                self.a.append(self.a[self.i-1])
                                self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                                self.t = dt
                                self.cases = 5       # self.error>0, a(self.i-1)=1.5, self.error>0.5*a(self.i-1)^2, case 5
                            elif self.error <= 0.5 * (self.a[self.i-1]+1.5) * (1.5-self.a[self.i-1]) + 1.125:
                                self.time = 2 * np.sqrt(self.error + 0.5 * (self.a[self.i-1])**2) - self.a[self.i-1]
                                self.a.append(self.a[self.i-1] + dt*1)
                                self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                                self.t = dt
                                self.cases = 6       # self.error>0, a(self.i-1)>0, self.error<=0.5 * (self.a[self.i-1]+1.5) * (1.5-self.a[self.i-1]) + 1.125, case 6
                            else:
                                self.time = 3 - self.a[self.i-1] + (self.error - (0.5 * (self.a[self.i-1]+1.5) * (1.5-self.a[self.i-1]) - 1.125))/1.5
                                self.a.append(self.a[self.i-1] + dt*1)
                                self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                                self.t = dt
                                self.cases = 7       # self.error>0, a(self.i-1)>0, self.error>0.5*(self.a[self.i-1]+1.5)*(1.5-self.a[self.i-1])+1.125, case 7
                    
                    else:
                        if self.error <= 2.25 - 0.5 * (self.a[self.i-1])**2:
                            self.time = 2 * np.sqrt(self.error + 0.5 * (self.a[self.i-1])**2) - self.a[self.i-1]
                            self.a.append(self.a[self.i-1] + dt*1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 8       # self.error>0, a(self.i-1)<0, self.error<=2.25-0.5*(self.a[self.i-1])**2, case 8
                        else:
                            self.time = 3 + (self.error + 0.5 * (self.a[self.i-1])**2 - 2.25)/1.5 - self.a[self.i-1]
                            self.a.append(self.a[self.i-1] + dt*1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 9       # self.error>0, a(self.i-1)<0, self.error>2.25-0.5*(self.a[self.i-1])**2, case 9
                            
                        
                else:
                    if self.a[self.i-1] == 0:
                        if self.error >= -2.25:
                            self.time = 2 * (np.sqrt(-self.error))
                            self.a.append(-dt * 1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 10       # self.error<0, a(self.i-1)=0, self.error>=-2.25, case 10
                            
                        else:
                            self.time = 3 + (-self.error-2.25)/1.5
                            self.a.append(-dt * 1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 11       # self.error<0, a(self.i-1)=0, self.error<-2.25, case 11
                            
                    elif self.a[self.i-1] < 0:
                        if self.error == -0.5 * (self.a[self.i-1])**2:
                            self.time = -self.a[self.i-1] * 1
                            self.a.append(self.a[self.i-1] + dt*1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 12       # self.error<0, a(self.i-1)<0, self.error=-0.5*a(self.i-1)^2, case 12
                        
                        elif self.error > -0.5 * (self.a[self.i-1])**2:
                            self.time = -self.a[self.i-1] + 2 * np.sqrt(0.5 * (self.a[self.i-1])**2 + self.error)
                            self.a.append(self.a[self.i-1] + dt*1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 13       # self.error<0, a(self.i-1)<0, self.error>-0.5*a(self.i-1)^2, case 13
                        
                        else:
                            if self.a[self.i-1] == -1.5:
                                self.time = 1.5 + (-self.error-1.125)/1.5
                                self.a.append(self.a[self.i-1])
                                self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                                self.t = dt
                                self.cases = 14       # self.error<0, a(self.i-1)=-1.5, self.error<-0.5*a(self.i-1)^2, case 14
                            elif self.error >= -0.5 * (-self.a[self.i-1]+1.5) * (1.5+self.a[self.i-1]) - 1.125:
                                self.time = 2 * np.sqrt(-self.error + 0.5 * (self.a[self.i-1])**2) + self.a[self.i-1]
                                self.a.append(self.a[self.i-1] - dt*1)
                                self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                                self.t = dt
                                self.cases = 15       # self.error<0, a(self.i-1)<0, self.error>=-0.5 * (self.a[self.i-1]+1.5) * (1.5-self.a[self.i-1]) - 1.125, case 15
                            else:
                                self.time = 3 + self.a[self.i-1] + (-self.error - (0.5 * (-self.a[self.i-1]+1.5) * (1.5+self.a[self.i-1]) - 1.125))/1.5
                                self.a.append(self.a[self.i-1] - dt*1)
                                self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                                self.t = dt
                                self.cases = 16       # self.error<0, a(self.i-1)<0, self.error<-0.5 * (self.a[self.i-1]+1.5) * (1.5-self.a[self.i-1]) - 1.125, case 16
                                
                    else:
                        if self.error >= -2.25 + 0.5 * (self.a[self.i-1])**2:
                            self.time = 2 * np.sqrt(-self.error + 0.5 * (self.a[self.i-1])**2) + self.a[self.i-1]
                            self.a.append(self.a[self.i-1] - dt*1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 17       # self.error<0, a(self.i-1)>0, self.error>=-2.25+0.5*(self.a[self.i-1])**2, case 17
                        else:
                            self.time = 3 + (-self.error + 0.5 * (self.a[self.i-1])**2 - 2.25)/1.5 + self.a[self.i-1]
                            self.a.append(self.a[self.i-1] - dt*1)
                            self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                            self.t = dt
                            self.cases = 18       # self.error>0, a(self.i-1)>0, self.error<-2.25+0.5*(self.a[self.i-1])**2, case 18
                        
        else:
            if self.cases == 1:
                if self.t <= 0.5 * self.time:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= self.time:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 2:
                if self.t <= 1.5:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= (self.time - 1.5):
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1])
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= self.time:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
                
            elif self.cases == 3:
                if self.t <= self.time:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 4:
                if self.t <= self.a[self.i-1] + np.sqrt(0.5 * (self.a[self.i-1])**2 - self.error):
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= self.a[self.i-1] + 2 * np.sqrt(0.5 * (self.a[self.i-1])**2 - self.error):
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 5:
                if self.t <= (self.error-1.125)/1.5:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1])
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 1.5 + (self.error-1.125)/1.5:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 6:
                if self.t <= np.sqrt(self.error + 0.5 * (self.a[self.i-1])**2) - self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 2 * np.sqrt(self.error + 0.5 * (self.a[self.i-1])**2) - self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 7:
                if self.t <= 1.5 - self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 1.5 - self.a[self.i-1] + (self.error - (0.5 * (self.a[self.i-1]+1.5) * (1.5-self.a[self.i-1]) - 1.125))/1.5:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1])
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 3 - self.a[self.i-1] + (self.error - (0.5 * (self.a[self.i-1]+1.5) * (1.5-self.a[self.i-1]) - 1.125))/1.5:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
                    
            elif self.cases == 8:
                if self.t <= np.sqrt(self.error + 0.5 * (self.a[self.i-1])**2) - self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 2 * np.sqrt(self.error + 0.5 * (self.a[self.i-1])**2) - self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 9:
                if self.t <= 1.5 - self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 1.5 + (self.error + 0.5 * (self.a[self.i-1])**2 - 2.25)/1.5 - self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1])
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 3 + (self.error + 0.5 * (self.a[self.i-1])**2 - 2.25)/1.5 - self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
                    
            if self.cases == 10:
                if self.t <= 0.5 * self.time:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= self.time:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 11:
                if self.t <= 1.5:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= (self.time - 1.5):
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1])
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= self.time:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
                
            elif self.cases == 12:
                if self.t <= self.time:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 13:
                if self.t <= -self.a[self.i-1] + np.sqrt(0.5 * (self.a[self.i-1])**2 + self.error):
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= -self.a[self.i-1] + 2 * np.sqrt(0.5 * (self.a[self.i-1])**2 + self.error):
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 14:
                if self.t <= (-self.error-1.125)/1.5:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1])
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 1.5 + (-self.error-1.125)/1.5:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 15:
                if self.t <= np.sqrt(-self.error + 0.5 * (self.a[self.i-1])**2) + self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 2 * np.sqrt(-self.error + 0.5 * (self.a[self.i-1])**2) + self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 16:
                if self.t <= 1.5 + self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 1.5 + self.a[self.i-1] + (-self.error-(0.5 * (-self.a[self.i-1]+1.5) * (1.5+self.a[self.i-1]) - 1.125))/1.5:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1])
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 3 + self.a[self.i-1] + (-self.error-(0.5 * (-self.a[self.i-1]+1.5) * (1.5+self.a[self.i-1]) - 1.125))/1.5:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
                    
            elif self.cases == 17:
                if self.t <= np.sqrt(-self.error + 0.5 * (self.a[self.i-1])**2) + self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 2 * np.sqrt(-self.error + 0.5 * (self.a[self.i-1])**2) + self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
            elif self.cases == 18:
                if self.t <= 1.5 + self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] - dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 1.5 + (-self.error + 0.5 * (self.a[self.i-1])**2 - 2.25)/1.5 + self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1])
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                elif self.t <= 3 + (-self.error + 0.5 * (self.a[self.i-1])**2 - 2.25)/1.5 + self.a[self.i-1]:
                    self.t = self.t + dt
                    self.a.append(self.a[self.i-1] + dt*1)
                    self.v.append(self.v[self.i-1] + self.a[self.i]*dt)
                else:
                    self.t = self.t + dt
                    self.a.append(0)
                    self.v.append(self.v[self.i-1])
            
        self.i = self.i + 1
        return self.v[self.i-1], self.a[self.i-1]