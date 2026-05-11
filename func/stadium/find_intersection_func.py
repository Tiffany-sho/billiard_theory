import numpy as np

def find_intersection(point,velocity,W, D) :
    
    print("代入法実行")

    if velocity[1] == 0 :
        y = point[1]
        x = velocity[0] /np.abs(velocity[0]) * np.sqrt((D /2) ** 2 - y ** 2) + velocity[0] /np.abs(velocity[0]) * W / 2

    incline = velocity[1] /velocity[0]
    temp_intersection_x = (velocity[1]/np.abs(velocity[1]) * D /2 - point[1]) / incline + point[0]
    temp_intersection_y = incline * (velocity[0]/np.abs(velocity[0])*(W /2 + D /2) - point[0]) + point[1]

    if np.abs(temp_intersection_x) <= W /2 :
        x = temp_intersection_x
        y = velocity[1]/np.abs(velocity[1]) * D /2
    elif temp_intersection_x > W /2 :
        a = 1 + incline * incline 
        b = -W /2 - point[0] * incline * incline +  incline * point[1]
        c = W * W /4 + incline * incline * point[0] * point[0] -2 * incline *point[0] * point[1] + point[1] * point[1] - D * D / 4
        
        if temp_intersection_y >= 0:
            x = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            y = np.sqrt((D /2) ** 2 - (x - W /2) **2 )
        else :
            x = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            y = - np.sqrt((D /2) ** 2 - (x - W /2) **2 )

    elif temp_intersection_x < -W /2 :
        
        a = 1 + incline * incline 
        b = W /2 - point[0] * incline * incline +  incline * point[1]
        c = W * W /4 + incline * incline * point[0] * point[0] -2 * incline *point[0] * point[1] + point[1] * point[1] - D * D / 4

        if temp_intersection_y >= 0:
            x = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            y = np.sqrt((D /2) ** 2 - (x + W /2) **2 )
        else :
            x = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            y = - np.sqrt((D /2) ** 2 - (x + W /2) **2 )
    
    return np.array([x,y])