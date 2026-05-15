import numpy as np

def find_reflect_direction(intersection,velocity,W) :

    speed = np.linalg.norm(velocity)

    if np.abs(intersection[0]) <= W /2 :
        reflected = np.array([velocity[0] ,-velocity[1]])
    
    else :

        if intersection[0] > W /2 :
            center = np.array([W /2 , 0])
        else :
            center = np.array([-W /2 , 0])
        
        n = intersection - center
        n_norm = np.linalg.norm(n)

        n_hat = n / n_norm

        reflected = velocity - 2 * np.dot(velocity,n_hat) * n_hat

    return reflected / np.linalg.norm(reflected) * speed