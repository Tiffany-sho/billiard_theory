import numpy as np

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

def get_position(sum_arc ,arc_length ,W ,H):

    if abs(arc_length) <= W /2:
        return np.array([arc_length , H /2])
    
    elif abs(arc_length) <= (W + H * np.pi ) / 2:

        if arc_length > 0 :
            sita = 2 * (arc_length - W / 2) / H
            return np.array([H / 2 * np.sin(sita) + W / 2 , H / 2 * np.cos(sita)])
        else:
            sita = 2 * (arc_length + W / 2) / H
            return np.array([H / 2 * np.sin(sita) - W / 2 ,  H / 2 * np.cos(sita)])
        
    else:
        if arc_length > 0 :
            return np.array([sum_arc /2 - arc_length , -H /2])
        else:
            return np.array([-sum_arc /2 - arc_length , -H /2])