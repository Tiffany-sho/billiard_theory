import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/squre'))

from setting import squre_set
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction

wall_width =2.0
wall_height =2.0

fig ,ax = plt.subplots()
squre_set(ax,wall_width,wall_height)


position_1 = np.array([0.0,0.0])
position_2 = np.array([0.0,0.0])
position_3 = np.array([0.0,0.0])
position_4 = np.array([0.0,0.0])
position_5 = np.array([0.0,0.0])
position_6 = np.array([0.0,0.0])
position_7 = np.array([0.0,0.0])
position_8 = np.array([0.0,0.0])
position_9 = np.array([0.0,0.0])
position_10 = np.array([0.0,0.0])
position_11 = np.array([0.0,0.0])
position_12 = np.array([0.0,0.0])
position_13 = np.array([0.0,0.0])
velocity_1 = np.array([0.5 ,0.3])
velocity_2 = np.array([0.5 ,0.300001])
velocity_3 = np.array([0.5 ,0.300002])
velocity_4 = np.array([0.5 ,0.300003])
velocity_5 = np.array([0.5 ,0.300004])
velocity_6 = np.array([0.5 ,0.300005])
velocity_7 = np.array([0.5 ,0.300006])
velocity_8 = np.array([0.5 ,0.300007])
velocity_9 = np.array([0.5 ,0.300008])
velocity_10 = np.array([0.5 ,0.300009])
velocity_11 = np.array([0.5 ,0.30001])
velocity_12 = np.array([0.5 ,0.300011])
velocity_13 = np.array([0.5 ,0.300012])


dot_1, = plt.plot([] ,[] , "o" , color = "black" ,ms = 3)
dot_2, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_3, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_4, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_5, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_6, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_7, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_8, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_9, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_10, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_11, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_12, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)
dot_13, = plt.plot([] ,[] , "o" , color = "red" ,ms = 3)

def create_ordit_dot(initial_position ,initial_velocity):

    positions = [initial_position.copy()]
    velocities = [initial_velocity.copy()]
    intersections = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for _ in range(50):
        intersection = find_intersection_reversion(p ,v ,wall_width ,wall_height)
        intersections.append(intersection.copy())
        v = find_reflect_direction(intersection ,v ,wall_width,wall_height)
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
ordit_3 = create_ordit_dot(position_2,velocity_2)
ordit_4 = create_ordit_dot(position_2,velocity_2)
ordit_5 = create_ordit_dot(position_2,velocity_2)
ordit_6 = create_ordit_dot(position_2,velocity_2)
ordit_7 = create_ordit_dot(position_2,velocity_2)
ordit_8 = create_ordit_dot(position_2,velocity_2)
ordit_9 = create_ordit_dot(position_2,velocity_2)
ordit_10 = create_ordit_dot(position_2,velocity_2)
ordit_11 = create_ordit_dot(position_2,velocity_2)
ordit_12 = create_ordit_dot(position_2,velocity_2)
ordit_13 = create_ordit_dot(position_2,velocity_2)

# print(f"ordit_1 length: {len(ordit_1[0])}")
# print(f"ordit_2 length: {len(ordit_2[0])}")

frame_num = min(len(ordit_1[0]),len(ordit_2[0]))

def update(frame):

    dot_1.set_data([ordit_1[0][frame]],[ordit_1[1][frame]])
    dot_2.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_3.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_4.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_5.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_6.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_7.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_8.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_9.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_10.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_11.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_12.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])
    dot_13.set_data([ordit_2[0][frame]],[ordit_2[1][frame]])

    return dot_1, dot_2, dot_3, dot_4, dot_5, dot_6, dot_7, dot_8, dot_9, dot_10, dot_11, dot_12, dot_13, 


ani = FuncAnimation(fig, update, frames=frame_num, interval=10 ,repeat=False ,blit=True)

ax.set_aspect('equal')
plt.show()