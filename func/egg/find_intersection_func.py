import numpy as np

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../calculate'))

def find_intersection_func(point,velocity,W_r ,W_l , H) :

    newton_method_range = np.sqrt((W_r / 2 + W_l / 2 + H) ** 2 + H ** 2) / np.linalg.norm(velocity)

    if velocity[0] == 0 and velocity[1] == 0 :
        return point.copy()
    
    if velocity[0] == 0 :
        x = point[0]
        if point[0] == 0 :
            y = np.sign(velocity[1]) * H / 2
        elif point[0] > 0 :
            y = np.sign(velocity[1]) * H / 2 * np.sqrt(1 - (x / (W_r /2)) ** 2)
        else:
            y = np.sign(velocity[1]) * H / 2 * np.sqrt(1 - (x / (W_l /2)) ** 2)
        return np.array([x ,y ])
    
    if velocity[1] == 0 :
        y = point[1]
        if point[1] == 0 :
            if velocity[0] > 0 :
                x =  W_r / 2
            else:
                x =  - W_l / 2
        elif point[1] > 0 :
            if velocity[0] > 0 :
                x = W_r / 2 * np.sqrt(1 - (y / (H /2)) ** 2)
            else:
                x = - W_l / 2 * np.sqrt(1 - (y / (H /2)) ** 2)
        else:
            if velocity[0] > 0 :
                x =  W_r / 2 * np.sqrt(1 - (y / (H /2)) ** 2)
            else:
                x = - W_l / 2 * np.sqrt(1 - (y / (H /2)) ** 2)
        return np.array([x ,y ])


    
    temp_intersection_y = H /2 if velocity[1] > 0 else -H /2
    temp_intersection_t =( temp_intersection_y - point[1] ) / velocity[1]

    if temp_intersection_t > 0:
        temp_intersection_x = point[0] + temp_intersection_t * velocity[0]
        if temp_intersection_x == 0:
            return np.array([0 , np.sign(velocity[1]) * H / 2])
        elif temp_intersection_x > 0:
            A_right = (velocity[0] / (W_r / 2)) ** 2 + (velocity[1] / (H / 2)) ** 2 
            B_right = point[0] * velocity[0] / (W_r / 2) ** 2 + point[1] * velocity[1] / (H / 2) ** 2
            C_right = (point[0] / (W_r / 2)) ** 2 + (point[1] / (H / 2)) ** 2 - 1
            D_right = B_right * B_right - A_right * C_right 
                    
            right_t =np.inf
            if D_right >= 0 :

                if B_right == 0 :
                    t1 = np.sqrt(- A_right * C_right) / A_right
                    t2 = C_right / A_right / t1

                else:
                    t1 = (- B_right -np.sign(B_right) * np.sqrt(B_right ** 2 - A_right * C_right)) / A_right
                    t2 = C_right / A_right / t1

                valid_t = [t for t in (t1, t2) if t > 0]
                if valid_t:
                    right_t = max(valid_t)
                    
                    return point + right_t * velocity
        
        elif temp_intersection_x < 0:
            A_left = (velocity[0] / (W_l / 2)) ** 2 + (velocity[1] / (H / 2)) ** 2 
            B_left = point[0] * velocity[0] / (W_l / 2) ** 2 + point[1] * velocity[1] / (H / 2) ** 2
            C_left = (point[0] / (W_l / 2)) ** 2 + (point[1] / (H / 2)) ** 2 - 1
            D_left = B_left * B_left - A_left * C_left 
                    
            left_t =np.inf
            if D_left >= 0 :
                if B_left == 0 :
                    t1 = np.sqrt(- A_left * C_left) / A_left
                    t2 = C_left / A_left / t1

                else:
                    t1 = (- B_left -np.sign(B_left) * np.sqrt(B_left ** 2 - A_left * C_left)) / A_left
                    t2 = C_left / A_left / t1

                valid_t = [t for t in (t1, t2) if t > 0]
                if valid_t:
                    left_t = max(valid_t)
                    
                    return point + left_t * velocity

