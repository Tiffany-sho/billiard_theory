import numpy as np

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../calculate'))

def find_intersection_reversion(point,velocity,W, H) :

    print("パラメータ法実行")

    if velocity[0] == 0.0 and velocity[1] == 0.0 :
        return point.copy()
    
    if velocity[0] == 0.0 :
        x = point[0]
        y = np.sign(velocity[1]) * H / 2
        return np.array([x,y])
    
    if velocity[1] == 0.0 :
        y = point[1]
        x = np.sign(velocity[0]) * W / 2
        return np.array([x,y])
    
    temp_intersection_x = W /2 if velocity[0] > 0 else -W /2
    temp_intersection_tx =( temp_intersection_x - point[0] ) / velocity[0]

    temp_intersection_y = H /2 if velocity[1] > 0 else -H /2
    temp_intersection_ty =( temp_intersection_y - point[1] ) / velocity[1]

    valid_t = min(temp_intersection_tx,temp_intersection_ty)

    return point + valid_t * velocity
