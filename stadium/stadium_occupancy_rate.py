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

wall_width =1.0
wall_height =1.0

position_1 = np.array([0.01,0.02])
velocity_1 = np.array([-0.05, 0.05])

bound_num = 10000

range_sin = 2.0
range_arc = 2 * (wall_width  + wall_height * np.pi / 2)

d_arc_length = range_arc/ 2 / 20
d_reflected_sin = 0.1

arc_length_box = int((wall_width * 2 + wall_height * np.pi) / d_arc_length)
reflected_sin_box = int(2.0 / d_reflected_sin)

print(f"縦幅:{d_reflected_sin}横幅:{d_arc_length}")
print(f"縦:{reflected_sin_box }横:{arc_length_box }")

fig ,ax = plt.subplots()
stadium_poincare_map_arc_set(ax,wall_width,wall_height)

def create_poincare_occupany(initial_position ,initial_velocity,W,H,color):

    
    arc_length = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    occupancy_index = np.zeros((reflected_sin_box ,arc_length_box ))

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
        reflected_sin_sign = 1 if set_reflection_sin >= 0 else 0
        arc_length_sign = 1 if set_arc_length >= 0 else 0

        reflected_sin_index = - int(set_reflection_sin / d_reflected_sin + reflected_sin_sign) +  int( reflected_sin_box / 2 ) 
        arc_length_index =  int(set_arc_length / d_arc_length + arc_length_sign) + int( arc_length_box / 2) - 1

        occupancy_index[reflected_sin_index][arc_length_index] += 1

    # plt.scatter(arc_length,reflection_sin,s=1,c=color)

    max_value = occupancy_index.max()
    
    for i in range(0,reflected_sin_box):
        range_sin_min = range_sin / 2 - d_reflected_sin * i
        range_sin_max = range_sin / 2 - d_reflected_sin * (i + 1)
        for j in range(0,arc_length_box):
            range_arc_min = - range_arc / 2 + d_arc_length* j
            range_arc_max = - range_arc / 2 + d_arc_length * (j + 1)

            alpha = occupancy_index[i][j] / max_value
            print(f"単位占有率:{occupancy_index[i][j] / d_arc_length / d_reflected_sin}")
            plt.fill_between([range_arc_min, range_arc_max],range_sin_min, range_sin_max, color="green", alpha=alpha)

    sum_squared_error = 0
    ave_occupancy = bound_num / (range_arc * range_sin)


    for i in range(0,reflected_sin_box):
        for j in range(0,arc_length_box):
            sum_squared_error += (occupancy_index[i][j] / bound_num - d_arc_length * d_reflected_sin / ave_occupancy) ** 2
    
    print(f"二乗誤差平均:{sum_squared_error / (reflected_sin_box * arc_length_box)}")


    print(f"全体占有率:{bound_num / (range_arc * range_sin)}")
    # fig.savefig(f"stadium/graph_data/poincare_depend_w_h_arc/poincare_{W,H}.png")

create_poincare_occupany(position_1,velocity_1,wall_width,wall_height ,"red")
# stadium_liner_system(position_1,velocity_1,wall_width,wall_height )
plt.show()