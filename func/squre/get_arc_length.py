import numpy as np

def get_arc_length(intersection ,W ,H):

    if abs(intersection[1]) == H / 2:
        if intersection[1] > 0:
            return intersection[0]
        else:
            if intersection[0] > 0 :
                return  W  + H - intersection[0]
            else:
                return  -W  - H - intersection[0]

    else :
        if intersection[0] > 0 :
            return W / 2 + H / 2 - intersection[1]
        else:
            return - W / 2 -H / 2 + intersection[1]
