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
