import numpy as np

def get_normal_vector(intersection ,W ,H):

    if abs(intersection[1]) == H /2:
        n = np.array([0 ,-np.sign(intersection[1])])
    else:
        if intersection[0] > W /2 :
            center = np.array([W /2 , 0])
        else :
            center = np.array([-W /2 , 0])
        
        n = intersection - center
        n_norm = np.linalg.norm(n)

        n = n / n_norm

    return n