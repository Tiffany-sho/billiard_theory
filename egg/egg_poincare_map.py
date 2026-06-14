import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/egg'))

from setting import egg_poincare_map
from find_intersection_func import find_intersection_func
from find_reflect_direction import find_reflect_direction
# from get_jacobian import get_jacobian

# wall_width_right = 4.0
# wall_width_left = 2.0
# wall_height =3.0

# position_1 = np.array([-0.36 ,0.9])
# velocity_1 = np.array([-0.06 , 0.06])

# fig ,ax = plt.subplots()
# egg_poincare_map(ax,wall_width_right,wall_width_left,wall_height)


def create_poincare_dot(initial_position ,initial_velocity,W_r,W_l,H,color):
    arc_angle = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for i in range(10000):
        intersection = find_intersection_func(p ,v ,W_r,W_l ,H)
        if intersection is None:
            ("交点が見つかりませんでした")
            return
        reflected_v = find_reflect_direction(intersection ,v ,W_r ,W_l ,H )

        set_arc_angle = np.arctan2(intersection[1],intersection[0])

        # jacobian = get_jacobian(W,H,set_arc_angle)
        if intersection[0] == 0:
            n = np.array([0 , np.sign(v[1])])
        elif intersection[0] > 0:
            n = np.array([ ((H /2) ** 2 * intersection[0]) ,(W_r /2) ** 2 * intersection[1]])
        else:
            n = np.array([ ((H /2) ** 2 * intersection[0]) ,(W_l /2) ** 2 * intersection[1]])

        n_norm = n / np.linalg.norm(n)
        v_norm = v / np.linalg.norm(v)

        cross_2d = v_norm[0] * n_norm[1] - v_norm[1] * n_norm[0]
        
        set_reflection_sin = cross_2d 

        p = intersection
        v = reflected_v
        arc_angle.append(set_arc_angle)
        reflection_sin.append(set_reflection_sin)

        if  i != 0 and np.allclose(arc_angle[0] , set_arc_angle) and np.allclose(reflection_sin[0] , set_reflection_sin): 
            print(f"起動周期性あり。{i}回衝突")
            break
        

    plt.scatter(arc_angle,reflection_sin,s=0.1,c=color)
    # fig.savefig(f"ellipse/graph_data/poincare_depend_w_h_arc/poincare_{W,H}.png")

# create_poincare_dot(position_1,velocity_1,wall_width_right,wall_width_left,wall_height,"red" )
# plt.show()