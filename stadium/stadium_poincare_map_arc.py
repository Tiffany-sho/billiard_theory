import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from decimal import Decimal

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))

from setting import initial_position,initial_velocity, wall_width, half_circle_diameter ,stadium_poincare_map_arc_set
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction
from get_normal_vector import get_normal_vector
from get_arc_length import get_arc_length



def create_poincare_dot(initial_position ,initial_velocity,W,H):

    fig ,ax = plt.subplots()
    stadium_poincare_map_arc_set(ax,W,H)
    arc_length = []
    reflection_sin = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for _ in range(3000):
        intersection = find_intersection_reversion(p ,v ,W ,H)
        reflected_v = find_reflect_direction(intersection ,v ,W)

        set_arc_length = get_arc_length(intersection,W,H)

        n = get_normal_vector(intersection,W,H)

        set_reflection_sin = np.cross(v /np.linalg.norm(v) ,n)

        p = intersection
        v = reflected_v
        arc_length.append(set_arc_length)
        reflection_sin.append(set_reflection_sin)

    plt.scatter(arc_length,reflection_sin,s=3)
    # fig.savefig(f"stadium/graph_data/poincare_depend_w_h_arc/poincare_{W,H}.png")


# for i in range(0,6):
#     for j in range (0,6):
#         create_poincare_dot(initial_position,initial_velocity,1 + i * 0.2 ,1 + j * 0.2)

create_poincare_dot(initial_position,initial_velocity,1 ,1 )
plt.show()