import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))

from setting import initial_position,initial_velocity, wall_width, half_circle_diameter ,poincare_map_set
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction
from get_normal_vector import get_normal_vector
from get_jacobian import get_jacobian

fig ,ax = plt.subplots()
poincare_map_set(ax)


def create_poincare_dot(initial_position ,initial_velocity):

    collision_angle = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for _ in range(1000):
        intersection = find_intersection_reversion(p ,v ,wall_width ,half_circle_diameter)
        reflected_v = find_reflect_direction(intersection ,v ,wall_width)

        set_collision_angle = np.arctan2(intersection[1] ,intersection[0])


        n = get_normal_vector(intersection,wall_width,half_circle_diameter)

        jacobian = get_jacobian(intersection,wall_width,half_circle_diameter,set_collision_angle)
        
        set_reflection_sin = np.cross(v /np.linalg.norm(v) ,n) * jacobian

        p = intersection
        v = reflected_v
        collision_angle.append(set_collision_angle)
        reflection_sin.append(set_reflection_sin)

    plt.scatter(collision_angle,reflection_sin,s=3)

create_poincare_dot(initial_position,initial_velocity)

plt.show()