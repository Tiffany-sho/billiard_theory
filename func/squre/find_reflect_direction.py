import numpy as np

def find_reflect_direction(intersection,velocity,W,H) :
    print(np.abs(intersection[0]) )
    print(np.abs(intersection[1]) )
    speed = np.linalg.norm(velocity)
    if np.abs(intersection[0]) == W / 2 :
        reflected = np.array([-velocity[0] ,velocity[1]])
    
    elif np.abs(intersection[1]) == H / 2 :
        reflected = np.array([velocity[0] ,-velocity[1]])


    return reflected / np.linalg.norm(reflected) * speed