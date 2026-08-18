import numpy as np 


position = np.array([0.0, 0.0, 10.0 ])
target = np.array([5.0, 0.0, 12.0 ])
error = target - position 
print (f"Error:{error} ")
print (f" magnitude: {np.linalg.norm(error)} ")


kp = 2 
command = kp * error
print(f"Command: {command}")

