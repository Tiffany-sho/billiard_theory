import numpy as np

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../calculate'))

from vertical_vector import vertical_vector

def find_intersection_reversion(point ,velocity ,W ,H ,D) :

    print("パラメータ法実行")

    if velocity[0] == 0.0 and velocity[1] == 0.0 :
        return point.copy()
    
    if velocity[0] == 0.0 :
        x = point[0]
        if np.abs(x) > (W - D) /2  and np.abs(x) < W /2 : 
            y = np.sign(velocity[1]) * H / 2
            return np.array([x,y])
        
        if velocity[1] * point[1] >= 0:
            y = np.sign(velocity[1]) * H / 2

        else:
            y = np.sign(point[1]) * np.sqrt((D /2) ** 2 - x ** 2)

        return np.array([x,y])
    
    if velocity[1] == 0.0 :
        y = point[1]
        if np.abs(y) > (H - D) /2  and np.abs(y) < H /2 : 
            x = np.sign(velocity[0]) * W / 2
            return np.array([x,y])
        
        if velocity[0] * point[0] >= 0:
            x = np.sign(velocity[0]) * W / 2

        else:
            x = np.sign(point[0]) * np.sqrt((D /2) ** 2 - y ** 2)

        return np.array([x,y])
    
    vertical_velocity = vertical_vector(velocity)

    length = np.abs(np.dot(vertical_velocity ,point)) / np.linalg.norm(velocity)
    if length > D /2 or np.dot(velocity ,point) > 0:

        print("Wall")
        temp_intersection_x = W /2 if velocity[0] > 0 else -W /2
        temp_intersection_tx =( temp_intersection_x - point[0] ) / velocity[0]

        temp_intersection_y = H /2 if velocity[1] > 0 else -H /2
        temp_intersection_ty =( temp_intersection_y - point[1] ) / velocity[1]

        if temp_intersection_tx < temp_intersection_ty :
            return np.array([temp_intersection_x , point[1] + velocity[1] * temp_intersection_tx])

        elif temp_intersection_tx > temp_intersection_ty :
            return np.array([point[0] + velocity[0] * temp_intersection_ty ,temp_intersection_y ])

        else :
            return np.array([temp_intersection_tx ,temp_intersection_ty])
        
    else:
        HI = np.sqrt((D /2) ** 2 - length ** 2)
        v_hat = velocity / np.linalg.norm(velocity)
        n_hat = vertical_velocity / np.linalg.norm(vertical_velocity)
        signed_length = np.dot(n_hat, point) 
        intersection_p1 = n_hat * signed_length + v_hat * HI
        intersection_p2 = n_hat * signed_length - v_hat * HI
        if np.linalg.norm(intersection_p1 -point) < np.linalg.norm(intersection_p2 -point) :
            return intersection_p1 * (D / 2) / np.linalg.norm(intersection_p1)
        else :
            return intersection_p2 * (D / 2) / np.linalg.norm(intersection_p2)
