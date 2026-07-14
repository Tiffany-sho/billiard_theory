import numpy as np

def find_intersection_reversion(point,velocity,W, D) :

    if velocity[0] == 0 and velocity[1] == 0 :
        return point.copy()
    
    if velocity[0] == 0 :
        x = point[0]
        if abs(point[0]) <= W/2:
            y = np.sign(velocity[1]) * D / 2
        elif point[0] < - W /2:
            y = np.sign(velocity[1]) * np.sqrt((D /2) ** 2 - (x + W /2) ** 2)
        else :
            y = np.sign(velocity[1]) * np.sqrt((D /2) ** 2 - (x - W /2) ** 2)

        return np.array([x,y])
    
    if velocity[1] == 0 :
        y = point[1]
        x = - np.sign(y) * np.sqrt((D /2) ** 2 - y ** 2) + np.sign(velocity[0]) * W / 2
       
        return np.array([x,y])
    

    temp_intersection_y = D /2 if velocity[1] > 0 else -D /2
    temp_intersection_t =( temp_intersection_y - point[1] ) / velocity[1]


    if temp_intersection_t >= 0 :
        temp_intersection_x = point[0] + temp_intersection_t * velocity[0]
        if np.abs(temp_intersection_x) <= W /2 :
            return np.array([temp_intersection_x,temp_intersection_y])

        elif temp_intersection_x > W /2 :
            # print("円状交点")
            A_right = velocity[0] ** 2 + velocity[1] ** 2 
            B_right = point[0] * velocity[0] + point[1] * velocity[1]  - W / 2 * velocity[0]
            C_right = point[0] ** 2 + point[1] **2 + W * W /4 - D * D /4 - W * point[0]
            D_right = B_right * B_right - A_right * C_right 
            
            right_t =np.inf
            if D_right >= 0 :
                if B_right == 0 :
                    t1 = np.sqrt(- A_right * C_right) / A_right
                    t2 = C_right / A_right / t1

                else:
                    t1 = (- B_right -np.sign(B_right) * np.sqrt(B_right ** 2 - A_right * C_right)) / A_right
                    t2 = C_right / A_right / t1


                valid_t = [t for t in (t1, t2) if t >= 0]
                if valid_t:
                    right_t = max(valid_t)
                    if point[0] + right_t * velocity[0] < W / 2:
                        right_t = np.inf
                    
                    return point + right_t * velocity

        elif temp_intersection_x <  - W /2 :
            # print("円状交点")
            A_left = velocity[0] ** 2 + velocity[1] ** 2 
            B_left = point[0] * velocity[0] + point[1] * velocity[1]  + W / 2 * velocity[0]
            C_left = point[0] ** 2 + point[1] **2 + W * W /4 - D * D /4 + W * point[0]
            D_left = B_left * B_left - A_left * C_left 
                
            left_t =np.inf
            if D_left >= 0 :
                if B_left == 0 :
                    t1 = np.sqrt(- A_left * C_left) / A_left
                    t2 = C_left / A_left / t1

                else:
                    t1 = (- B_left -np.sign(B_left) * np.sqrt(B_left ** 2 - A_left * C_left)) / A_left
                    t2 = C_left / A_left / t1

                    
                valid_t = [t for t in (t1, t2) if t >= 0]
                if valid_t:
                    left_t = max(valid_t)
                    if point[0] + left_t * velocity[0] > -W / 2:
                        left_t = np.inf
                    
                    return point + left_t * velocity

def find_reflect_direction(intersection,velocity,W) :

    speed = np.linalg.norm(velocity)

    if np.abs(intersection[0]) <= W /2 :
        reflected = np.array([velocity[0] ,-velocity[1]])
    
    else :

        if intersection[0] > W /2 :
            center = np.array([W /2 , 0])
        else :
            center = np.array([-W /2 , 0])
        
        n = intersection - center
        n_norm = np.linalg.norm(n)

        n_hat = n / n_norm

        reflected = velocity - 2 * np.dot(velocity,n_hat) * n_hat

    return reflected / np.linalg.norm(reflected) * speed

def get_normal_vector(intersection ,W ,H):

    if abs(intersection[1]) == H /2:
        n = np.array([0 ,-np.sign(intersection[1])])
    else:
        if intersection[0] > W /2 :
            center = np.array([W /2 , 0])
        else :
            center = np.array([-W /2 , 0])
        
        n = intersection - center
        n_norm = np.linalg.norm(n)

        n = n / n_norm

    return n

def get_arc_length(intersection ,W ,H):

    if abs(intersection[0]) <= W / 2:
        if intersection[1] > 0:
            return intersection[0]
        else:
            if intersection[0] > 0 :
                return  W  + H / 2 * np.pi - intersection[0]
            else:
                return  -W  - H / 2 * np.pi - intersection[0]

    else :
        arc = np.acos(2 * intersection[1] / H) * H / 2
        if intersection[0] > 0 :
            return W / 2 + arc
        else:
            return - W / 2 -arc
