import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/egg'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/calulate'))

from setting import egg_poincare_map ,occupancy_rate_gragh
from find_intersection_func import find_intersection_func
from find_reflect_direction import find_reflect_direction
from create_setting import egg_create_setting

wall_width_right = 3.0
wall_width_left = 4.0
wall_height =2.0


range_arc = 2 * np.pi 
range_sin = 2.0

# position_1 ,velocity_1 = egg_create_setting(0,wall_width_right,wall_width_left,wall_height,range_arc)
position_1 = np.array([1.43 ,0.28])
velocity_1 = np.array([-0.0091 ,-0.0040])
print(position_1,velocity_1)

divide_sin = 100
divide_arc = 100

d_arc_length =  2 * np.pi / divide_sin
d_reflected_sin = range_sin / divide_arc

def create_axis(initial_position ,initial_velocity,W_r,W_l,H,bound_num):
    arc_angle = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    occupancy_index = np.zeros((divide_sin ,divide_arc ))

    for i in range(bound_num):

        set_arc_angle = np.arctan2(p[1],p[0])

        if p[0] == 0:
            n = np.array([0 , np.sign(v[1])])
        elif p[0] > 0:
            n = np.array([ ((H /2) ** 2 * p[0]) ,(W_r /2) ** 2 * p[1]])
        else:
            n = np.array([ ((H /2) ** 2 * p[0]) ,(W_l /2) ** 2 * p[1]])

        n_norm = n / np.linalg.norm(n)
        v_norm = v / np.linalg.norm(v)

        cross_2d = v_norm[0] * n_norm[1] - v_norm[1] * n_norm[0]
        
        set_reflection_sin = cross_2d 

        intersection = find_intersection_func(p ,v ,W_r,W_l ,H)
        reflected_v = find_reflect_direction(intersection ,v ,W_r ,W_l ,H )
        p = intersection
        v = reflected_v
        arc_angle.append(set_arc_angle)
        reflection_sin.append(set_reflection_sin)

        reflected_sin_sign = 1 if set_reflection_sin >= 0 else 0
        arc_length_sign = 1 if set_arc_angle >= 0 else 0

        reflected_sin_index = - int(set_reflection_sin / d_reflected_sin + reflected_sin_sign) +  int( divide_sin / 2 ) 
        arc_length_index =  int(set_arc_angle / d_arc_length + arc_length_sign) + int( divide_arc / 2) - 1

        occupancy_index[reflected_sin_index][arc_length_index] += 1

    return occupancy_index,arc_angle,reflection_sin
    

def create_poincare_occupany_area(W_r,W_l,H,bound_num):

    fig,ax = plt.subplots()
    egg_poincare_map(ax,W_r,W_l,H)

    index ,x ,y = create_axis(position_1 ,velocity_1,W_r,W_l,H,bound_num)

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


def order_bound_num_on_error(W_r,W_l,H,bound_num):

    index ,x ,y = create_axis(position_1 ,velocity_1,W_r,W_l,H,bound_num)

    sum_squared_error = 0
    all_area =  range_arc * range_sin

    for i in range(0,divide_sin):
        for j in range(0,divide_arc):
            sum_squared_error += (index[i][j] / bound_num - d_arc_length * d_reflected_sin / all_area) ** 2
    
    ave_sqrt_error = sum_squared_error / (divide_sin * divide_arc)
    # plt.scatter(bound_num , ave_sqrt_error ,c = "green",s = 5)
    print(f"衝突回数:{bound_num},二乗誤差平均:{ave_sqrt_error}")


def Shannon_entropy(W_r,W_l,H,bound_num):

    index ,x ,y = create_axis(position_1 ,velocity_1,W_r,W_l,H,bound_num)

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

def shannon_entropy_gragh(W_r,W_l,H):

    fig,ax = plt.subplots()
    occupancy_rate_gragh(ax)

    part_area = d_arc_length * d_reflected_sin
    all_area =  range_arc * range_sin

    for i in range(0,200):
        Shannon_entropy(W_r,W_l,H,1000 + i * 100)
    ax.axhline(y=-np.log2(part_area/all_area),color = "red" ,linestyle="--")
    plt.show()

shannon_entropy_gragh(wall_width_right,wall_width_left,wall_height)

# create_poincare_occupany_area(wall_width_right,wall_width_left,wall_height,1000)
# plt.show()