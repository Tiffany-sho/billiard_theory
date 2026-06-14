import numpy as np

def find_reflect_direction(intersection,velocity,W_r,W_l,H) :
    speed = np.linalg.norm(velocity)

    if intersection[0] == 0 :
        return np.array([velocity[0] ,-velocity[1]])        

    elif intersection[0] > 0 :

        n = np.array([ ((H /2) ** 2 * intersection[0]) ,(W_r /2) ** 2 * intersection[1]])
        n_norm = np.linalg.norm(n)

        n_hat = n / n_norm

        reflected = velocity - 2 * np.dot(velocity,n_hat) * n_hat

    else:
        n = np.array([ ((H /2) ** 2 * intersection[0]) ,(W_l /2) ** 2 * intersection[1]])
        n_norm = np.linalg.norm(n)

        n_hat = n / n_norm

        reflected = velocity - 2 * np.dot(velocity,n_hat) * n_hat

    return reflected / np.linalg.norm(reflected) * speed

