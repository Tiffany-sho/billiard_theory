import numpy as np

def get_jacobian(W_r ,W_l ,H ,angle):

    if abs(angle) < np.pi / 2 :
        j = np.sqrt((W_r / 2 * np.sin(angle) ) ** 2 + (H / 2 * np.cos(angle)) ** 2 )
    
    else :
        j = np.sqrt((W_l / 2 * np.sin(angle) ) ** 2 + (H / 2 * np.cos(angle)) ** 2 )

    jacobian = np.sqrt(j)
    

    return jacobian

