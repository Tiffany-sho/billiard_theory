import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))

from setting import wall_width, half_circle_diameter ,stadium_set
from find_intersection_func import find_intersection
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction

fig ,ax = plt.subplots()
stadium_set(ax)

position = np.array([0.0,0.0])
velocity = np.array([3.0 ,4.0])

print("-------------------------------------")
print(f"初期値:{position}")
print(f"初速度:{velocity}")


def update(frame):

    # intersection = find_intersection(position,velocity,wall_width, half_circle_diameter)
    intersection = find_intersection_reversion(position,velocity,wall_width, half_circle_diameter)

    print("-------------------------------------")
    print(f"位置:{position}")
    print(f"速度:{velocity}")
    print(f"y = {velocity[1] /velocity[0]}x + {-velocity[1] /velocity[0] * position[0] + position[1]}")
    print(intersection)
    plt.plot([intersection[0]],[intersection[1]] , "o",color = "black" ,ms = 3)

    ordit_x = np.linspace(intersection[0] ,position[0] ,100)
    ordit_y = velocity[1] /velocity[0] * (ordit_x - position[0]) + position[1]

    plt.plot(ordit_x,ordit_y,color = "black" ,linewidth = 1 ,alpha=0.1)

    position[:2] = intersection[:2]
    reflected_velocity = find_reflect_direction(position,velocity,wall_width)
    velocity[:2] = reflected_velocity[:2]

ani = FuncAnimation(fig, update, frames=10, interval=1000 ,repeat=False)

ax.set_aspect('equal')
plt.show()