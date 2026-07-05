import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/sinai'))

from setting import sinai_poincare_map
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction


wall_width =5.0
wall_height =5.0
sinai_circle_diameter = 0.5

position_1 = np.array([2.0,2.0])
velocity_1 = np.array([0.4, -0.7])

fig ,ax = plt.subplots()
sinai_poincare_map(ax,wall_width,wall_height,sinai_circle_diameter)

def create_poincare_dot(initial_position ,initial_velocity,W,H,D,color):
    arc_angle = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for i in range(10000):


        # jacobian = get_jacobian(W_r,W_l,H,set_arc_angle)
        if abs(np.linalg.norm(p) - D / 2) < 1e-10:
            set_arc_angle = np.arctan2(p[1],p[0]) + np.pi
            n = np.array([ p[0],  p[1]])
        else:
            set_arc_angle = np.arctan2(p[1],p[0]) + 3 * np.pi
            if abs(p[0]) == W /2 and abs(p[1]) == H /2:
                n = np.array([- np.sign(p[0]) , - np.sign(p[1])])
            elif abs(p[0] ) == W /2:
                n = np.array([-np.sign(p[0]) , 0])
            else:
                n = np.array([0 ,- np.sign(p[1])])

        n_norm = n / np.linalg.norm(n)
        v_norm = v / np.linalg.norm(v)

        cross_2d = v_norm[0] * n_norm[1] - v_norm[1] * n_norm[0]
        
        set_reflection_sin = cross_2d 

        arc_angle.append(set_arc_angle)
        reflection_sin.append(set_reflection_sin)

        intersection = find_intersection_reversion(p ,v ,W ,H, D)
        reflected_v = find_reflect_direction(intersection ,v ,W , H, D)
        p = intersection
        v = reflected_v

        if  i != 0 and np.allclose(arc_angle[0] , set_arc_angle) and np.allclose(reflection_sin[0] , set_reflection_sin): 
            print(f"起動周期性あり。{i}回衝突")
            break
        

    plt.scatter(arc_angle,reflection_sin,s=0.05, color=color)
    # fig.savefig(f"ellipse/graph_data/poincare_depend_w_h_arc/poincare_{W,H}.png")

create_poincare_dot(position_1,velocity_1,wall_width,wall_height,sinai_circle_diameter,"red" )
plt.show()
