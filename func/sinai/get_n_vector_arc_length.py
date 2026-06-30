import numpy as np

def get_n_vector_arc_length(p,W,H,D):
    if abs(np.linalg.norm(p) - D / 2) < 1e-10:
            sign = 1.0 if p[1] == 0 else np.sign(p[1])
            set_arc_length = D / 2 * (np.arctan2(p[1],p[0])) + sign * (H + W)
            n = np.array([ p[0],  p[1]])
    else:
        if p[0] == W /2 :
            set_arc_length = p[1]
        elif abs(p[1]) == H / 2 :
            set_arc_length = p[1] + np.sign(p[1]) * ( W /2 - p[0])
        else :
            sign = 1.0 if p[1] == 0 else np.sign(p[1])
            set_arc_length =  sign * ( H  + W ) - p[1]

        if abs(p[0]) == W /2 and abs(p[1]) == H /2:
            n = np.array([- np.sign(p[0]) , - np.sign(p[1])])
        elif abs(p[0] ) == W /2:
            n = np.array([-np.sign(p[0]) , 0])
        else:
            n = np.array([0 ,- np.sign(p[1])])

    return set_arc_length,n
