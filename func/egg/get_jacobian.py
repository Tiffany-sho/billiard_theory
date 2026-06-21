import numpy as np

def get_jacobian(W_r ,W_l ,H ,angle):

    if abs(angle) < np.pi / 2 :
        r = np.sqrt((W_r / 2 * np.cos(angle) ) ** 2 + (H / 2 * np.sin(angle)) ** 2 )
        dr_dsita = (H - W_r) * np.sin(2 * angle) / (2 * r)
    
    else :
        r = np.sqrt((W_l / 2 * np.cos(angle) ) ** 2 + (H / 2 * np.sin(angle)) ** 2 )
        dr_dsita = (H - W_l) * np.sin(2 * angle) / (2 * r)

    jacobian = np.sqrt(r ** 2 + dr_dsita ** 2)
    

    return jacobian

