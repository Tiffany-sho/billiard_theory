import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))

from setting import stadium_poincare_map_arc_set
from stadium_liner_system import stadium_liner_system
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction
from get_normal_vector import get_normal_vector
from get_arc_length import get_arc_length

wall_width =2.0
wall_height =1.0

position_1 = np.array([0.01,0.02])
velocity_1 = np.array([-0.05, 0.05])

bound_num = 10000


fig ,ax = plt.subplots()
stadium_poincare_map_arc_set(ax,wall_width,wall_height)

def create_poincare_dot(initial_position ,initial_velocity,W,H,color):

    
    arc_length = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    

    for i in range(bound_num):

        set_arc_length = get_arc_length(p,W,H)

        n = get_normal_vector(p,W,H)

        v_norm = v / np.linalg.norm(v)

        cross_2d = v_norm[0] * n[1] - v_norm[1] * n[0]
        
        set_reflection_sin = cross_2d


        intersection = find_intersection_reversion(p ,v ,W ,H)
        reflected_v = find_reflect_direction(intersection ,v ,W)
        p = intersection
        v = reflected_v
        arc_length.append(set_arc_length)
        reflection_sin.append(set_reflection_sin)

        if  i != 0 and np.allclose(arc_length[0] , set_arc_length) and np.allclose(reflection_sin[0] , set_reflection_sin): 
            print(f"起動周期性あり。{i}回衝突")
            break
        

    plt.scatter(arc_length,reflection_sin,s=0.01,c=color)
    # fig.savefig(f"stadium/graph_data/poincare_depend_w_h_arc/poincare_{W,H}.png")

create_poincare_dot(position_1,velocity_1,wall_width,wall_height ,"red")
# stadium_liner_system(position_1,velocity_1,wall_width,wall_height )
plt.show()