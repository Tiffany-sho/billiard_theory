import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/egg'))

from setting import egg_set
from find_intersection_func import find_intersection_func 
from find_reflect_direction import find_reflect_direction

max_frame = 100

wall_width_right = 3.0
wall_width_left = 4.0
wall_height =5.0

position_1 = np.array([-0.36 ,0.9])
velocity_1 = np.array([-0.06 , 0.06])


def stadium_liner_system(initial_position,initial_velocity,W_r,W_l,H):

    fig ,ax = plt.subplots()
    egg_set(ax,W_r,W_l,H)
    position = initial_position.copy()
    velocity = initial_velocity.copy()

    def update(frame):

        intersection = find_intersection_func(position,velocity,W_r ,W_l, H)

        if intersection is None:
            print("交点が見つかりませんでした")
            return
        plt.plot([intersection[0]],[intersection[1]] , "o",color = "black" ,ms = 3)

        ordit_x = np.linspace(intersection[0] ,position[0] ,100) if intersection[0] - position[0] != 0 else [position[0] for _ in range(100)]
        ordit_y = velocity[1] /velocity[0] * (ordit_x - position[0]) + position[1] if velocity[0] != 0 else np.linspace(intersection[1] ,position[1] ,100)

        plt.plot(ordit_x,ordit_y,color = "black" ,linewidth = 1 ,alpha=0.1)

        position[:2] = intersection[:2]
        reflected_velocity = find_reflect_direction(position,velocity,W_r,W_l,H)
        velocity[:2] = reflected_velocity[:2]

        if  frame != 0 and np.allclose(position[0] , position[:2]) and np.allclose(velocity[0] , velocity[:2]): 
            print(f"起動周期性あり。{frame}回衝突")
            frame = max_frame
        

    ani = FuncAnimation(fig, update, frames=max_frame, interval=100 ,repeat=False)

    ax.set_aspect('equal')
    plt.show()


stadium_liner_system(position_1,velocity_1,wall_width_right,wall_width_left,wall_height)
