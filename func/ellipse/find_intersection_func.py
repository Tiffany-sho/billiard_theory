import numpy as np

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../calculate'))

from newton_method import newton_method

def find_intersection_func(point,velocity,W, H) :

    newton_method_range = np.sqrt((W + H) ** 2 + H ** 2) / np.linalg.norm(velocity)

    if velocity[0] == 0 and velocity[1] == 0 :
        return point.copy()
    
    A_right = (velocity[0] / (W / 2)) ** 2 + (velocity[1] / (H / 2)) ** 2 
    B_right = point[0] * velocity[0] / (W / 2) ** 2 + point[1] * velocity[1] / (H / 2) ** 2
    C_right = (point[0] / (W / 2)) ** 2 + (point[1] / (H / 2)) ** 2 - 1
    D_right = B_right * B_right - A_right * C_right 
            
    right_t =np.inf
    if D_right >= 0 :
        t1 =newton_method(A_right,2 * B_right,C_right,newton_method_range)
        t2 =newton_method(A_right,2 * B_right,C_right,-newton_method_range)
        # print(-2 * B_right / A_right)

        valid_t = [t for t in (t1, t2) if t >= 0]
        if valid_t:
            right_t = max(valid_t)
            
            return point + right_t * velocity

def find_intersection_format(p,v,W, H) :

    a = W / 2 * v[1]
    b = H / 2 * v[0]
    A_x = a ** 2 - b ** 2 - 2 * v[0] * v[1]
    A_y = - a ** 2 + b ** 2 - 2 * v[0] * v[1]
    B = a ** 2 + b ** 2

    return np.array([p[0] * A_x / B ,p[1] * A_y / B])