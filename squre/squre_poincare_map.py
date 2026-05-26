import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/squre'))

from setting import squrt_poincare_map_arc_set
from squre_liner_system import squre_line_system
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction
from get_normal_vector import get_normal_vector
# from get_jacobian import get_jacobian
from get_arc_length import get_arc_length

wall_width =1.0
wall_height =2.0

position_1 = np.array([0.0,0.5])
velocity_1 = np.array([-0.031, -0.051])

def create_poincare_dot(initial_position ,initial_velocity ,W ,H):

    fig ,ax = plt.subplots()
    squrt_poincare_map_arc_set(ax ,W ,H)

    collision_angle = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for _ in range(50):
        intersection = find_intersection_reversion(p ,v ,W ,H)
        reflected_v = find_reflect_direction(intersection ,v ,W,H)

        set_arc_length = get_arc_length(intersection,W,H)

        n = get_normal_vector(intersection,v,W,H)

        # jacobian = get_jacobian(intersection,W,H,set_collision_angle)
        
        set_reflection_sin = np.cross(v /np.linalg.norm(v) ,n) 
        p = intersection
        v = reflected_v
        collision_angle.append(set_arc_length)
        reflection_sin.append(set_reflection_sin)

    plt.scatter(collision_angle,reflection_sin)

create_poincare_dot(position_1,velocity_1 ,wall_width ,wall_height)
squre_line_system(position_1,velocity_1 ,wall_width ,wall_height)

plt.show()