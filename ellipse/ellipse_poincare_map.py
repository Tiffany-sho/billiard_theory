import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/ellipse'))

from setting import stadium_poincare_map_arc_set
from find_intersection_func import find_intersection_func
from find_reflect_direction import find_reflect_direction
from get_jacobian import get_jacobian

wall_width =2.0
wall_height =2.0

position_1 = np.array([0.0,0.3])
velocity_1 = np.array([-0.05, 0.01])


def create_poincare_dot(initial_position ,initial_velocity,W,H):

    fig ,ax = plt.subplots()
    stadium_poincare_map_arc_set(ax,W,H)
    arc_angle = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for i in range(3000):
        intersection = find_intersection_func(p ,v ,W ,H)
        reflected_v = find_reflect_direction(intersection ,v ,W,H)

        set_arc_angle = np.arctan2(intersection[1],intersection[0])

        jacobian = get_jacobian(W,H,set_arc_angle)

        n = np.array([ ((H /2) ** 2 * intersection[0]) ,(W /2) ** 2 * intersection[1]])

        v_norm = v / np.linalg.norm(v)

        cross_2d = v_norm[0] * n[1] - v_norm[1] * n[0]
        
        set_reflection_sin = cross_2d *jacobian


        p = intersection
        v = reflected_v
        arc_angle.append(set_arc_angle)
        reflection_sin.append(set_reflection_sin)

        if  i != 0 and np.allclose(arc_angle[0] , set_arc_angle) and np.allclose(reflection_sin[0] , set_reflection_sin): 
            print(f"起動周期性あり。{i}回衝突")
            break
        

    plt.scatter(arc_angle,reflection_sin,s=3)
    # fig.savefig(f"ellipse/graph_data/poincare_depend_w_h_arc/poincare_{W,H}.png")

create_poincare_dot(position_1,velocity_1,wall_width,wall_height )
plt.show()