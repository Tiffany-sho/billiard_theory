import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/squre'))

from setting import wall_width, wall_height ,poincare_map_set
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction

fig ,ax = plt.subplots()
poincare_map_set(ax)

position_1 = np.array([0.0,0.5])
velocity_1 = np.array([-0.03, -0.05])

def create_poincare_dot(initial_position ,initial_velocity):


    collision_angle = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for _ in range(50):
        intersection = find_intersection_reversion(p ,v ,wall_width ,wall_height)
        reflected_v = find_reflect_direction(intersection ,v ,wall_width,wall_height)

        set_collision_angle = np.arctan2(intersection[1] ,intersection[0])

        if np.isclose(abs(intersection[0]), wall_width /2) and np.isclose(abs(intersection[1]), wall_height /2):
            print("==========================")
            n = np.array([-v[0] / np.linalg.norm(v) ,-v[1] / np.linalg.norm(v)])
        elif np.isclose(abs(intersection[0]), wall_width /2):
            n = np.array([-np.sign(intersection[0]) ,0])
        else:
            n = np.array([0 ,-np.sign(intersection[1])])
        
        set_reflection_sin = np.cross(v /np.linalg.norm(v) ,n)
        print(v)
        print(n)
        print(set_reflection_sin)

        p = intersection
        v = reflected_v
        collision_angle.append(set_collision_angle)
        reflection_sin.append(set_reflection_sin)

    plt.scatter(collision_angle,reflection_sin)

create_poincare_dot(position_1,velocity_1)

print(np.acos(-1/np.sqrt(2))*360/2/np.pi)

plt.show()