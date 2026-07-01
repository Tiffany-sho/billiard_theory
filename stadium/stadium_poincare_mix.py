import numpy as np
import matplotlib.pyplot as plt
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/calcuate'))

from stadium_poincare_map_arc import create_poincare_dot
from setting import stadium_poincare_map_arc_set,stadium_set,basic_colors
from create_setting import stadium_create_setting



wall_width = 2.0
wall_height =2.0

epoch = 100
epoch_per_arc = (2 * wall_width + wall_height * np.pi) / epoch

fig ,ax = plt.subplots()
stadium_poincare_map_arc_set(ax,wall_width,wall_height)

for i in range(0,epoch):

    position,velocity = stadium_create_setting(i,wall_width,wall_height,epoch_per_arc)
    print(f"初期値:{position}")
    print(f"初速度:{velocity}")
    create_poincare_dot(position,velocity,wall_width,wall_height ,basic_colors[i])

plt.show()