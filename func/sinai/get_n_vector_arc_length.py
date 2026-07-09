import numpy as np

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
