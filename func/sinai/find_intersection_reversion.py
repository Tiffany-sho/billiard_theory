import numpy as np

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../calculate'))

def find_intersection_reversion(point ,velocity ,W ,H ,D) :

    if velocity[0] == 0.0 and velocity[1] == 0.0 :
        return point.copy()
    
    if velocity[0] == 0.0 :
        x = point[0]
        if np.abs(x) > D /2  and np.abs(x) < W /2 : 
            y = np.sign(velocity[1]) * H / 2
            return np.array([x,y])
        
        if velocity[1] * point[1] >= 0:
            y = np.sign(velocity[1]) * H / 2

        else:
            y = np.sign(point[1]) * np.sqrt((D /2) ** 2 - x ** 2)

        return np.array([x,y])
    
    if velocity[1] == 0.0 :
        y = point[1]
        if np.abs(y) > D /2  and np.abs(y) < H /2 : 
            x = np.sign(velocity[0]) * W / 2
            return np.array([x,y])
        
        if velocity[0] * point[0] >= 0:
            x = np.sign(velocity[0]) * W / 2

        else:
            x = np.sign(point[0]) * np.sqrt((D /2) ** 2 - y ** 2)

        return np.array([x,y])
    
    A = velocity[0] ** 2 + velocity[1] ** 2
    B = np.dot(velocity,point)
    C = point[0] ** 2 + point[1] ** 2 - (D / 2) ** 2

    if B ** 2 - A * C <= 0 or B >= 0.0 :
        temp_intersection_x = W /2 if velocity[0] > 0 else -W /2
        temp_intersection_tx =( temp_intersection_x - point[0] ) / velocity[0]

        temp_intersection_y = H /2 if velocity[1] > 0 else -H /2
        temp_intersection_ty =( temp_intersection_y - point[1] ) / velocity[1]

        if temp_intersection_tx < temp_intersection_ty :
            return np.array([temp_intersection_x , point[1] + velocity[1] * temp_intersection_tx])

        elif temp_intersection_tx > temp_intersection_ty :
            return np.array([point[0] + velocity[0] * temp_intersection_ty ,temp_intersection_y ])

        else :
            return np.array([temp_intersection_x ,temp_intersection_y])
        
    else:
        # print("円状交点")
        if B == 0 :
            t1 = np.sqrt(- A * C) / A
            t2 = C / A / t1

        else:
            t1 = (- B -np.sign(B) * np.sqrt(B ** 2 - A * C)) / A
            t2 = C / A / t1
        
        valid_t = [t for t in (t1, t2) if t >= 0]

        if valid_t:
            right_t = min(valid_t)
            if (np.linalg.norm(point + right_t * velocity) - D / 2) > 1e-10:
                print("交点未発見エラー")
                right_t = np.inf
            hit = point + right_t * velocity
            hit *= (D / 2) / np.linalg.norm(hit)
            return hit