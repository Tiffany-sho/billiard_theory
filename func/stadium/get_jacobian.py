import numpy as np

def get_jacobian(intersection ,W ,H ,angle):

    if np.abs(intersection[0]) <= W /2:
        return H / 2 / np.sin(angle) ** 2

    elif intersection[0] > W / 2 :
        D = (H / 2) ** 2 - (W / 2 * np.sin(angle)) ** 2
        r = W / 2 * np.cos(angle) + np.sqrt(D)
        dr_dsita = - W / 2 * np.sin(angle) - (W / 2) ** 2 * np.sin(angle) * np.cos(angle) / np.sqrt(D)
    
    else :
        D = (H / 2) ** 2 - (W / 2 * np.sin(angle)) ** 2
        r = - W / 2 * np.cos(angle) + np.sqrt(D)
        dr_dsita = W / 2 * np.sin(angle) - (W / 2) ** 2 * np.sin(angle) * np.cos(angle) / np.sqrt(D)

    jacobian = np.sqrt(r ** 2 + dr_dsita ** 2)
    

    return jacobian

