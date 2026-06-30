import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/sinai'))

from setting import sinai_poincare_map_arc
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction
from get_n_vector_arc_length import get_n_vector_arc_length


wall_width =5.0
wall_height =5.0
sinai_circle_diameter = 2.0

position_1 = np.array([2.0,2.0])
velocity_1 = np.array([0.4, -0.7])

fig ,ax = plt.subplots()
sinai_poincare_map_arc(ax,wall_width,wall_height,sinai_circle_diameter)

def create_poincare_dot(initial_position ,initial_velocity,W,H,D,color):
    arc_length = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for i in range(10000):

        set_arc_length ,n= get_n_vector_arc_length(p,W,H,D)

        n_norm = n / np.linalg.norm(n)
        v_norm = v / np.linalg.norm(v)

        cross_2d = v_norm[0] * n_norm[1] - v_norm[1] * n_norm[0]
        
        set_reflection_sin = cross_2d 

        arc_length.append(set_arc_length)
        reflection_sin.append(set_reflection_sin)

        intersection = find_intersection_reversion(p ,v ,W ,H,D)
        reflected_v = find_reflect_direction(intersection ,v ,W , H,D )
        p = intersection
        v = reflected_v

        if  i != 0 and np.allclose(arc_length[0] , set_arc_length) and np.allclose(reflection_sin[0] , set_reflection_sin): 
            print(f"起動周期性あり。{i}回衝突")
            break
        

    plt.scatter(arc_length,reflection_sin,s=0.05, color=color)
    # fig.savefig(f"ellipse/graph_data/poincare_depend_w_h_arc/poincare_{W,H}.png")

create_poincare_dot(position_1,velocity_1,wall_width,wall_height,sinai_circle_diameter,"red" )
plt.show()
