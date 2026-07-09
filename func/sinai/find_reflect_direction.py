import numpy as np

def find_reflect_direction(intersection,velocity,W,H,D) :
    speed = np.linalg.norm(velocity)
    if abs(np.linalg.norm(intersection) - D / 2) < 1e-10:
        n_norm = np.linalg.norm(intersection)
        n_hat = - intersection / n_norm
        reflected = velocity - 2 * np.dot(velocity,n_hat) * n_hat
    elif np.abs(intersection[0]) == W / 2 and np.abs(intersection[1]) == H / 2:

        reflected = np.array([-velocity[0] ,-velocity[1]])
    elif np.abs(intersection[1]) == H / 2 :
        reflected = np.array([velocity[0] ,-velocity[1]])
    
    else:
        reflected = np.array([-velocity[0] ,velocity[1]])

    return reflected / np.linalg.norm(reflected) * speed
