import numpy as np

def get_normal_vector(intersection ,v ,wall_width ,wall_height):
    if abs(intersection[0]) == wall_width /2 and abs(intersection[1]) == wall_height / 2:
        n = np.array([-v[0] / np.linalg.norm(v) ,-v[1] / np.linalg.norm(v)])
    elif abs(intersection[0]) == wall_width /2:
        n = np.array([-np.sign(intersection[0]) ,0])
    else:
        n = np.array([0 ,-np.sign(intersection[1])])

    return n