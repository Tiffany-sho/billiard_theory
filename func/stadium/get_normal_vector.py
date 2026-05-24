import numpy as np

def get_normal_vector(intersection ,wall_width ,wall_height):

    if abs(intersection[1]) == wall_height /2:
        n = np.array([0 ,-np.sign(intersection[1])])
    else:
        if intersection[0] > wall_width /2 :
            center = np.array([wall_width /2 , 0])
        else :
            center = np.array([-wall_width /2 , 0])
        
        n = intersection - center
        n_norm = np.linalg.norm(n)

        n = n / n_norm

    return n