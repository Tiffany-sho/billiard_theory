import numpy as np

def get_jacobian(intersection ,W ,H ,angle):

    if np.abs(intersection[1]) == H /2  :
        jacobian =  W / 2 / np.cos(angle) ** 2
    
    else:
       jacobian =  H / 2 / np.sin(angle) ** 2

    return jacobian

