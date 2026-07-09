import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))

from setting import poincare_map_set
from stadium_liner_system import stadium_liner_system
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction
from get_normal_vector import get_normal_vector
from get_jacobian import get_jacobian

wall_width =2.0
wall_height =2.0

position_1 = np.array([1 / np.sqrt(2) + 1.0 ,1 / np.sqrt(2)])
velocity_1 = np.array([-0.05, 0.00])

# fig ,ax = plt.subplots()
# poincare_map_set(ax,wall_width,wall_height)

def create_poincare_dot(initial_position ,initial_velocity,W,H,color):

    
    collision_angle = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for i in range(0,30):

        set_collision_angle = np.arctan2(p[1] ,p[0])
        n = get_normal_vector(p,W,H)

        jacobian = get_jacobian(p,W,H,set_collision_angle)

        v_norm = v / np.linalg.norm(v)

        cross_2d = v_norm[0] * n[1] - v_norm[1] * n[0]
        
        set_reflection_sin = cross_2d * jacobian

        intersection = find_intersection_reversion(p ,v ,W ,H)
        reflected_v = find_reflect_direction(intersection ,v ,W)

        p = intersection
        v = reflected_v
        
        collision_angle.append(set_collision_angle)
        reflection_sin.append(set_reflection_sin)

    plt.scatter(collision_angle,reflection_sin,s=3,c=color)

create_poincare_dot(position_1,velocity_1,wall_width,wall_height ,"red")
stadium_liner_system(position_1,velocity_1,wall_width,wall_height )
plt.show()