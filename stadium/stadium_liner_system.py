import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))

from setting import stadium_set
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction

max_frame = 100

def stadium_liner_system(initial_position,initial_velocity,W,H):

    print("処理開始")

    fig ,ax = plt.subplots()
    stadium_set(ax,W,H)

    position = initial_position.copy()
    velocity = initial_velocity.copy()

    def update(frame):

        intersection = find_intersection_reversion(position,velocity,W, H)
        plt.plot([intersection[0]],[intersection[1]] , "o",color = "black" ,ms = 3)

        ordit_x = np.linspace(intersection[0] ,position[0] ,100) if intersection[0] - position[0] != 0 else [position[0] for _ in range(100)]
        ordit_y = velocity[1] /velocity[0] * (ordit_x - position[0]) + position[1] if velocity[0] != 0 else np.linspace(intersection[1] ,position[1] ,100)

        plt.plot(ordit_x,ordit_y,color = "black" ,linewidth = 1 ,alpha=0.1)

        position[:2] = intersection[:2]
        reflected_velocity = find_reflect_direction(position,velocity,W)
        velocity[:2] = reflected_velocity[:2]

    ani = FuncAnimation(fig, update, frames=max_frame, interval=1 ,repeat=False)


    ax.set_aspect('equal')
    plt.show()
    print("処理終了")
