import numpy as np

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
        
def find_reflect_direction(intersection,velocity,W,H,D) :
    speed = np.linalg.norm(velocity)
    if abs(np.linalg.norm(intersection) - D / 2) < 1e-10:
        n_norm = np.linalg.norm(intersection)
        n_hat = - intersection / n_norm
        reflected = velocity - 2 * np.dot(velocity,n_hat) * n_hat
    elif np.abs(intersection[0]) == W / 2 and np.abs(intersection[1]) == H / 2:

        reflected = np.array([-velocity[0] ,-velocity[1]])
    elif np.abs(intersection[1]) == H / 2 :
        reflected = np.array([velocity[0] ,-velocity[1]])
    
    else:
        reflected = np.array([-velocity[0] ,velocity[1]])

    return reflected / np.linalg.norm(reflected) * speed

def get_n_vector_arc_length(p,W,H,D):
    if abs(np.linalg.norm(p) - D / 2) < 1e-10:
            set_arc_length = D / 2 * (np.arctan2(p[1],p[0])) + np.pi * D / 2 + 2 * (H + W)
            n = np.array([ p[0],  p[1]])
    else:
        if p[1] == H /2 :
            set_arc_length = W / 2 - p[0]
            n = np.array([0.0 , -1.0])
        elif p[0] == - W/ 2 :
            set_arc_length =  W + H / 2 - p[1]
            n = np.array([1.0 , 0.0])
        elif p[1] == - H / 2 :
            set_arc_length =  W + H  + W / 2 + p[0]
            n = np.array([0.0 , 1.0])
        else :
            set_arc_length = W + H + W + H / 2 + p[1]
            n = np.array([-1.0 , 0.0])

    return set_arc_length,n
