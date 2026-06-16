import numpy as np

def create_setting(i,W_r,W_l,H,epoch_per_sita):
    theta = np.random.rand() * epoch_per_sita  + epoch_per_sita * i - np.pi

    if abs(theta) < np.pi / 2:
        a = W_r / 2
    else:
        a = W_l / 2
    b = H / 2

    x = a * np.cos(theta)
    y = b * np.sin(theta)
    position = np.array([x, y])

    nx = -x / (a**2)
    ny = -y / (b**2)
    normal_length = np.sqrt(nx**2 + ny**2)

    nx_norm = nx / normal_length
    ny_norm = ny / normal_length

    normal_angle = np.arctan2(ny_norm, nx_norm)

    phi = np.random.rand() * np.pi - np.pi / 2

    vx = np.cos(normal_angle + phi) 
    vy = np.sin(normal_angle + phi)
    velocity = np.array([vx / 100, vy / 100])

    return position,velocity