import numpy as np
import matplotlib.pyplot as plt
from Speed_controller import Controller_speed
import central_Logic

def speed():
    speed_controller = Controller_speed()

    tSpeed = 0               #central_Logic.finalFunction()[0] * 1000 / 3600
    overtaking_mode = central_Logic.finalFunction()[2]
    e_STOP = central_Logic.finalFunction()[3]
                    
    #total_time = 15  # Total simulation time (seconds)
    dt = 0.01  # Time step (seconds)
    #num_steps = int(total_time / dt)  # Number of time steps
                    
    #time = np.linspace(0, total_time, num_steps)
    #speed_limit = np.where(time < 3.5, 2.7, np.where(time < 9, 0, 0))
                    
    # Control actions
    velocity = []
    acceleration = []
        
    v, a = speed_controller.update(tSpeed, dt)
    velocity.append(v)  # Append velocity to velocity array
    acceleration.append(a)
    
    return [v*3600/1000, overtaking_mode, e_STOP]
                     
    #for speed in speed_limit:

        #v, a = speed_controller.update(speed, dt)  # Get velocity and acceleration from update function
        #velocity.append(v)  # Append velocity to velocity array
        #acceleration.append(a)
                
# Plotting
#plt.figure(figsize=(10, 6))
#plt.plot(time, speed_limit, label='speed limit')
#plt.plot(time, acceleration, label='Acceleration')
#plt.plot(time, velocity, label='Velocity')
#plt.xlabel('Time (seconds)')
#plt.ylabel('Value')
#plt.title('Response')
#plt.legend()
#plt.grid(True)
#plt.show()