import numpy as np

def get_jacobian(W ,H ,angle):

    r = np.sqrt(W / 2 * np.cos(angle) ** 2 + H / 2 * np.sin(angle) ** 2)

    dr_dsita = np.sin(2 * angle) * (- W ** 2 + H ** 2) / (8 * r)

    jacobian = np.sqrt(r ** 2 + dr_dsita ** 2)
    

    return jacobian

