from matplotlib import pyplot as plt
import numpy as np
from PID_speed import PIDController_speed

def main():
    # Define PID controller parameters
    kp = 1200  # controller constants, subject to change
    ki = 770
    kd = 1
    m = 700  # vehicle mass
    b = 0.15  # vehicle drag coefficient
    
    # Create an instance of the PIDController
    pid_controller = PIDController_speed(kp, ki, kd, m, b)
    
    time = np.arange(0, 60, 1)
    velocity = np.zeros([60], dtype = float)
    vr = np.zeros([60], dtype = float)
    
    for i in range(1, 60):
        # speed limit at time i
        if i < 10:
            vr[i] = 10
        elif i < 30:
            vr[i] = 15
        elif i < 40:
            vr[i] = 20
        else:
            vr[i] = 10
    
    dt = 0.2 # updating time interval, to be changed
    for i in range(1, 60):
        velocity[i] = pid_controller.update(vr[i], dt)
    
    # plot the reference velocity lines
    vr_arr = np.zeros([60], dtype = float) + 15
    plt.plot(time, vr_arr, 'g''--', lw = 2)
    vr_arr = np.zeros([60], dtype = float) + 20
    plt.plot(time, vr_arr, 'g''--', lw = 2)
    vr_arr = np.zeros([60], dtype = float) + 10
    plt.plot(time, vr_arr, 'g''--', lw = 2)
    
    title='''Speed PID controller response
    '''
    plt.title(title)
    plt.xlabel("time")
    plt.ylabel("velocity")
    plt.grid()
    plt.plot(time, velocity)
    plt.show()

if __name__ == "__main__":
    main()
    