import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/squre'))

from setting import wall_width, wall_heigth ,squre_set
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction

fig ,ax = plt.subplots()
squre_set(ax)


position_1 = np.array([0.0,0.0])
position_2 = np.array([0.0,0.0])
velocity_1 = np.array([0.5 ,0.3])
velocity_2 = np.array([0.5 ,0.3001])

dot_1, = plt.plot([] ,[] , "o" , color = "black" ,ms = 3)
dot_2, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)

def create_ordit_dot(initial_position ,initial_velocity):

    positions = [initial_position.copy()]
    velocities = [initial_velocity.copy()]
    intersections = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for _ in range(50):
        intersection = find_intersection_reversion(p ,v ,wall_width ,wall_heigth)
        intersections.append(intersection.copy())
        v = find_reflect_direction(intersection ,v ,wall_width,wall_heigth)
        p = intersection.copy()
        positions.append(p.copy())
        velocities.append(v.copy())


    ordit_x = []
    ordit_y = []
    for i in range(len(intersections)):

        norm_length = np.linalg.norm(positions[i] - intersections[i]) 
        norm_velocity = np.linalg.norm(velocities[i])


        time = max(int(norm_length /norm_velocity *10) ,2)

        seg_x = np.linspace(positions[i][0], intersections[i][0] , time )
        seg_y = np.linspace(positions[i][1], intersections[i][1] , time )

        ordit_x.extend(seg_x)
        ordit_y.extend(seg_y)

    return [ordit_x ,ordit_y]

ordit_1 = create_ordit_dot(position_1,velocity_1)
ordit_2 = create_ordit_dot(position_2,velocity_2)

print(f"ordit_1 length: {len(ordit_1[0])}")
print(f"ordit_2 length: {len(ordit_2[0])}")

frame_num = min(len(ordit_1[0]),len(ordit_2[0]))

def update(frame):

    dot_1.set_data([ordit_1[0][frame]],[ordit_1[1][frame]])
    dot_2.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])

    return dot_1, dot_2


ani = FuncAnimation(fig, update, frames=frame_num, interval=10 ,repeat=False ,blit=True)

ax.set_aspect('equal')
plt.show()