import numpy as np

def find_intersection(point,velocity) :

    intersection = np.array([0.0,0.0])

    if velocity[1] == 0 :
        intersection[1] = point[1]
        intersection[0] = velocity[0] /np.abs(velocity[0]) * np.sqrt((wall_half_dismeter /2) ** 2 - intersection[1] ** 2) + velocity[0] /np.abs(velocity[0]) * wall_width / 2
        return intersection

    incline = velocity[1] /velocity[0]
    temp_intersection_x = (velocity[1]/np.abs(velocity[1]) * wall_half_dismeter /2 - point[1]) / incline + point[0]
    temp_intersection_y = incline * (velocity[0]/np.abs(velocity[0])*(wall_width /2 + wall_half_dismeter /2) - point[0]) + point[1]

    if np.abs(temp_intersection_x) <= wall_width /2 :
        intersection[0] = temp_intersection_x
        intersection[1] = velocity[1]/np.abs(velocity[1]) * wall_half_dismeter /2
    elif temp_intersection_x > wall_width /2 :
        a = 1 + incline * incline 
        b = -wall_width /2 - point[0] * incline * incline +  incline * point[1]
        c = wall_width * wall_width /4 + incline * incline * point[0] * point[0] -2 * incline *point[0] * point[1] + point[1] * point[1] - wall_half_dismeter * wall_half_dismeter / 4
        
        if temp_intersection_y >= 0:
            intersection[0] = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            intersection[1] = np.sqrt((wall_half_dismeter /2) ** 2 - (intersection[0] - wall_width /2) **2 )
        else :
            intersection[0] = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            intersection[1] = - np.sqrt((wall_half_dismeter /2) ** 2 - (intersection[0] - wall_width /2) **2 )

    elif temp_intersection_x < -wall_width /2 :
        
        a = 1 + incline * incline 
        b = wall_width /2 - point[0] * incline * incline +  incline * point[1]
        c = wall_width * wall_width /4 + incline * incline * point[0] * point[0] -2 * incline *point[0] * point[1] + point[1] * point[1] - wall_half_dismeter * wall_half_dismeter / 4

        if temp_intersection_y >= 0:
            intersection[0] = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            intersection[1] = np.sqrt((wall_half_dismeter /2) ** 2 - (intersection[0] + wall_width /2) **2 )
        else :
            intersection[0] = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            intersection[1] = - np.sqrt((wall_half_dismeter /2) ** 2 - (intersection[0] + wall_width /2) **2 )
    
    return intersection