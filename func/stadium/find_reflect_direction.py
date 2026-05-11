import numpy as np


def find_reflect_direction(intersection,velocity,W) :

    if np.abs(intersection[0]) <= W /2 :
        return np.array([velocity[0] ,-velocity[1]])

    if intersection[0] > W /2 :
        center = np.array([W /2 , 0])
    else :
        center = np.array([-W /2 , 0])
    
    n = intersection - center
    n_norm = np.linalg.norm(n)

    n_hat = n / n_norm

    return velocity - 2 * np.dot(velocity,n_hat) * n_hat