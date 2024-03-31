import numpy as np
import matplotlib.pyplot as plt
from PID_steering import PIDController_steering
#from PID_speed import PIDController_speed


def main():
    # Define PID controller parameters
    kp = 1.3
    ki = 0.1
    kd = 0.2
    setpoint = 0.0
    integral_limit = 5.0
    derivative_filter_tau = 0.1
    
    # Create an instance of the PIDController
    pid_controller = PIDController_steering(kp, ki, kd, setpoint, integral_limit, derivative_filter_tau)
    
    ### Discrete errors
    errors = [8.0, 9.0, 10.0, 11.0, 9.0, 7.0, 3.0, 0.0, -2.0, -4.0]
    
    # Time step
    dt = 0.1
    
    # Process the errors and compute control actions
    for error in errors:
        control_action = pid_controller.update(error, dt)
        print("Error:", error, "Steering angle:", control_action)
    
    ### Continuous errors
    #total_time = 10  # Total simulation time (seconds)
    #dt = 0.01  # Time step (seconds)
    #num_steps = int(total_time / dt)  # Number of time steps
    
    # Time array
    #time = np.linspace(0, total_time, num_steps)
    
    # Error signal
    #error_amplitude = 2.0
    #error_frequency = 1
    #error_signal = error_amplitude * np.sin(2 * np.pi * error_frequency * time)
    
    #decay_constant = 0.8  # Decay constant for the exponential function
    #decay_signal = np.exp(-decay_constant * time)

    # Combine signals (multiply them)
    #combined_signal = error_signal * decay_signal

    # Control actions
    #control_actions = []
    
    #for error in combined_signal:
    #    control_action = pid_controller.update(error, dt)
    #    control_actions.append(control_action)
        
    # Plotting
    #fig, ax1 = plt.subplots(figsize=(10, 6))
    
    #ax1.plot(time, combined_signal, label='Error Signal')
    #ax1.set_xlabel('Time (seconds)')
    #ax1.set_ylabel('Error signal')
    #ax1.set_ylim(-2.4, 2)
    #ax1.tick_params(axis='y', labelcolor='blue')
    
    # Create a secondary y-axis for control actions (in degrees)
    #ax2 = ax1.twinx()
    #ax2.plot(time, control_actions, label='Control Actions (Degrees)', color='red')
    #ax2.set_ylabel('Steering angles (Degrees)', color='red')
    #ax2.set_ylim(-36, 30)
    #ax2.tick_params(axis='y', labelcolor='red')
    
    
    #plt.title('PID Controller Response')
    #plt.grid(True)
    #plt.show()
    
    
if __name__ == "__main__":
    main()