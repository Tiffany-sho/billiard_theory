import numpy as np

def egg_create_setting(i,W_r,W_l,H,epoch_per_sita):
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


def stadium_create_setting(i,W,H,epoch_per_arc):
    arc = np.random.rand() * epoch_per_arc  + epoch_per_arc * i - (H * np.pi / 2 + W)

    if abs(arc) <= W /2:
        x = arc
        y = H / 2
    
    elif abs(arc) <= (W + H * np.pi ) / 2:

        if arc > 0 :
            sita = 2 * (arc - W / 2) / H
            x = H / 2 * np.sin(sita) + W / 2
            y = H / 2 * np.cos(sita)
        else:
            sita = 2 * (arc + W / 2) / H
            x = H / 2 * np.sin(sita) - W / 2
            y = H / 2 * np.cos(sita)
        
    else:
        if arc > 0 :
            x = (H * np.pi / 2 + W) - arc
            y = -H /2
        else:
            x = -(H * np.pi / 2 + W) - arc
            y = -H /2

    position = np.array([x, y])

    if abs(x) > W /2 :
        center = np.array([np.sign(x) * W /2 , 0])
        n = center - position
        n_norm = np.linalg.norm(n)
        n_hat = n / n_norm
    else :
        n_hat = np.array([0.0 , - np.sign(y)]) 

    normal_angle = np.arctan2(n_hat[1], n_hat[0])

    phi = np.random.rand() * np.pi - np.pi / 2

    vx = np.cos(normal_angle + phi) 
    vy = np.sin(normal_angle + phi)
    velocity = np.array([vx / 100, vy / 100])

    return position,velocity

def sinai_create_setting(i,W,H,D,epoch_per_arc):
    arc = np.random.rand() * epoch_per_arc  + epoch_per_arc * i - (W  + H + np.pi * D / 2)

    if abs(arc) < H / 2 :
        x = W / 2
        y = arc
    
    elif abs(arc) < W + H / 2 :

        if arc > 0 :
            x = W / 2 - arc +  H / 2
            y = H / 2

        else:
            x = W / 2 + arc + H / 2
            y = -H / 2

    elif abs(arc) < W + H :

        if arc > 0:
            x = - W / 2 
            y = W + H - arc
        else:
            x = - W / 2 
            y = -(W + H) - arc

    else:
        
        if arc > 0:
            circle_arc = arc - (W + H)

        else:
            circle_arc = arc + (W + H)
        
        angle = circle_arc / (D / 2)
        x = D / 2 * np.cos(angle)
        y = D / 2 * np.sin(angle)

    position = np.array([x, y])

    if abs(np.linalg.norm(position) - D / 2) < 1e-10:
        n = np.array([ position[0],  position[1]])
        n_norm = np.linalg.norm(n)
        n_hat = n / n_norm
        
    elif abs(position[0]) == W /2 and abs(position[1]) == H /2:
        n_hat = np.array([- np.sign(position[0]) , - np.sign(position[1])])
    elif abs(position[0] ) == W /2:
        n_hat = np.array([-np.sign(position[0]) , 0])
    else:
        n_hat = np.array([0 ,- np.sign(position[1])])

    normal_angle = np.arctan2(n_hat[1], n_hat[0])

    phi = np.random.rand() * np.pi - np.pi / 2

    vx = np.cos(normal_angle + phi) 
    vy = np.sin(normal_angle + phi)
    velocity = np.array([vx / 100, vy / 100])

    return position,velocity
