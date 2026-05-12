import numpy as np

def find_intersection_reversion(point,velocity,W, D) :

    print("パラメータ法実行")

    if velocity[0] == 0 and velocity[1] == 0 :
        return point.copy()
    
    if velocity[0] == 0 :
        x = point[0]
        y = velocity[1] /np.abs(velocity[1]) * D / 2
        return np.array([x,y])

    if velocity[1] == 0 :
        y = point[1]
        x = velocity[0] /np.abs(velocity[0]) * np.sqrt((D /2) ** 2 - y ** 2) + velocity[0] /np.abs(velocity[0]) * W / 2
        return np.array([x,y])

    temp_intersection_y = D /2 if velocity[1] > 0 else -D /2
    temp_intersection_t =( temp_intersection_y - point[1] ) / velocity[1]


    if temp_intersection_t >= 0 :
        temp_intersection_x = point[0] + temp_intersection_t * velocity[0]
        if np.abs(temp_intersection_x) <= W /2 :
            return np.array([temp_intersection_x,temp_intersection_y])

        elif temp_intersection_x > W /2 :
            A_right = velocity[0] ** 2 + velocity[1] ** 2 
            B_right = point[0] * velocity[0] + point[1] * velocity[1]  - W / 2 * velocity[0]
            C_right = point[0] ** 2 + point[1] **2 + W * W /4 - D * D /4 - W * point[0]
            D_right = B_right * B_right - A_right * C_right 
            
            right_t =np.inf
            if D_right >= 0 :
                t1 = (- B_right - np.sqrt(D_right)) / A_right
                t2 = (- B_right + np.sqrt(D_right)) / A_right

                valid_t = [t for t in (t1, t2) if t >= 0]
                if valid_t:
                    right_t = max(valid_t) 
                    if point[0] + right_t * velocity[0] < W / 2:
                        right_t = np.inf
                    
                    return point + right_t * velocity

        elif temp_intersection_x <  - W /2 :
            A_left = velocity[0] ** 2 + velocity[1] ** 2 
            B_left = point[0] * velocity[0] + point[1] * velocity[1]  + W / 2 * velocity[0]
            C_left = point[0] ** 2 + point[1] **2 + W * W /4 - D * D /4 + W * point[0]
            D_left = B_left * B_left - A_left * C_left 
                
            left_t =np.inf
            if D_left >= 0 :
                t1 = (- B_left - np.sqrt(D_left)) / A_left
                t2 = (- B_left + np.sqrt(D_left)) / A_left

                valid_t = [t for t in (t1, t2) if t >= 0]
                if valid_t:
                    left_t = max(valid_t) 
                    if point[0] + left_t * velocity[0] > -W / 2:
                        print(point[0] + left_t * velocity[0])
                        left_t = np.inf

                    return point + left_t * velocity
