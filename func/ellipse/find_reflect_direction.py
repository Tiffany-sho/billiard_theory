import numpy as np

def find_reflect_direction(intersection,velocity,W,H) :
    speed = np.linalg.norm(velocity)

    n = np.array([ ((H /2) ** 2 * intersection[0]) ,(W /2) ** 2 * intersection[1]])
    n_norm = np.linalg.norm(n)

    n_hat = n / n_norm

    reflected = velocity - 2 * np.dot(velocity,n_hat) * n_hat

    return reflected / np.linalg.norm(reflected) * speed