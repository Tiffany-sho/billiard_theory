import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/calulate'))

from setting import stadium_poincare_map_arc_set,occupancy_rate_gragh
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction
from get_normal_vector import get_normal_vector
from get_arc_length import get_arc_length
from create_setting import stadium_create_setting

wall_width =1.0
wall_height =3.0

range_sin = 2.0
range_arc = 2 * (wall_width  + wall_height * np.pi / 2)


position_1,velocity_1 = stadium_create_setting(0,wall_width,wall_height,range_arc)
# position_1 = np.array([0.37462786 ,1. ])
# velocity_1 = np.array([ -0.00594382 ,-0.00804183])
print(position_1,velocity_1)

divide_sin = 50
divide_arc = 50

d_reflected_sin = range_sin / divide_sin
d_arc_length = range_arc / divide_arc

def create_axis(initial_position ,initial_velocity,W,H,bound_num):

    arc_length = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    occupancy_index = np.zeros((divide_sin ,divide_arc ))

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

        reflected_sin_sign = 1 if set_reflection_sin >= 0 else 0
        arc_length_sign = 1 if set_arc_length >= 0 else 0

        reflected_sin_index = - int(set_reflection_sin / d_reflected_sin + reflected_sin_sign) +  int( divide_sin / 2 ) 
        arc_length_index =  int(set_arc_length / d_arc_length + arc_length_sign) + int( divide_arc / 2) - 1

        occupancy_index[reflected_sin_index][arc_length_index] += 1

    return occupancy_index,arc_length,reflection_sin

def create_poincare_occupany_area(W,H,bound_num):

    fig_1,ax_1 = plt.subplots()
    stadium_poincare_map_arc_set(ax_1,wall_width,wall_height)

    index ,x ,y = create_axis(position_1 ,velocity_1,W,H,bound_num)

    plt.scatter(x,y,s=1,c="red")

    max_value = index.max()
    
    for i in range(0,divide_sin):
        range_sin_min = range_sin / 2 - d_reflected_sin * i
        range_sin_max = range_sin / 2 - d_reflected_sin * (i + 1)
        for j in range(0,divide_arc):
            range_arc_min = - range_arc / 2 + d_arc_length* j
            range_arc_max = - range_arc / 2 + d_arc_length * (j + 1)

            alpha = index[i][j] / max_value
            plt.fill_between([range_arc_min, range_arc_max],range_sin_min, range_sin_max, color="green", alpha=alpha)


def order_bound_num_on_error(W,H,bound_num):

    # fig_1,ax_1 = plt.subplots()
    # occupancy_rate_gragh(ax_1)

    index ,x ,y = create_axis(position_1 ,velocity_1,W,H,bound_num)

    sum_squared_error = 0
    all_area =  range_arc * range_sin

    for i in range(0,divide_sin):
        for j in range(0,divide_arc):
            sum_squared_error += (index[i][j] / bound_num - d_arc_length * d_reflected_sin / all_area) ** 2
    
    ave_sqrt_error = sum_squared_error / (divide_sin * divide_arc)
    # plt.scatter(bound_num , ave_sqrt_error ,c = "green",s = 5)
    print(f"衝突回数:{bound_num},二乗誤差平均:{ave_sqrt_error}")

def Shannon_entropy(W,H,bound_num):

    index ,x ,y = create_axis(position_1 ,velocity_1,W,H,bound_num)

    shannon_entropy = 0
    part_area = d_arc_length * d_reflected_sin
    all_area =  range_arc * range_sin

    for i in range(0,divide_sin ):
        for j in range(0,divide_arc ):

            if index[i][j] == 0 :
                continue
            shannon_entropy += (index[i][j] / bound_num) * np.log2(index[i][j] / bound_num)
    
    plt.scatter(bound_num , -shannon_entropy ,c = "green",s = 5)
    print(f"最大シャノンエントロピー:{-np.log2(part_area/all_area)}")
    print(f"衝突回数:{bound_num},シャノンエントロピー:{-shannon_entropy}")

# create_poincare_occupany_area(wall_width,wall_height,10000)

def shannon_entropy_gragh(W,H):

    fig,ax = plt.subplots()
    occupancy_rate_gragh(ax)

    part_area = d_arc_length * d_reflected_sin
    all_area =  range_arc * range_sin

    for i in range(0,200):
        Shannon_entropy(W,H,1000 + i * 100)
    ax.axhline(y=-np.log2(part_area/all_area),color = "red" ,linestyle="--")
    plt.show()

shannon_entropy_gragh(wall_width,wall_height)

plt.show()