import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from create_setting import sinai_create_setting
from setting import sinai_poincare_map_arc,basic_colors
from sinai import Sinai

wall_width =5.0
wall_height =5.0
sinai_circle_diameter = 2.0

bound_num = 1000

epoch = 100
epoch_per_arc = 2 * (wall_width  + wall_height + np.pi * sinai_circle_diameter / 2) / epoch

fig ,ax = plt.subplots()
sinai_poincare_map_arc(ax,wall_width,wall_height,sinai_circle_diameter)

for i in range(0,epoch):

    position,velocity = sinai_create_setting(i,wall_width,wall_height,sinai_circle_diameter,epoch_per_arc)
    print(f"初期値:{position}")
    print(f"初速度:{velocity}")
    sinai = Sinai(position,velocity,wall_width,wall_height,sinai_circle_diameter,bound_num)
    sinai.poincare(basic_colors[i])

plt.show()