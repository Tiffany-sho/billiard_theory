import numpy as np
import matplotlib.pyplot as plt
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))

from stadium_poincare_map_arc import create_poincare_dot
from setting import stadium_poincare_map_arc_set,stadium_set,basic_colors
from get_arc_length import get_position



wall_width = 2.0
wall_height =2.0

sum_arc = 2 * wall_width + wall_height * np.pi

fig ,ax = plt.subplots()
stadium_poincare_map_arc_set(ax,wall_width,wall_height)

for i in range(0,7):
    arc = np.random.rand() * sum_arc - sum_arc / 2
    position = get_position(sum_arc,arc,wall_width,wall_height)
    velocity = np.array([(np.random.rand() *2 -1) / 100 ,(np.random.rand() *2 -1) / 100])
    create_poincare_dot(position,velocity,wall_width,wall_height ,basic_colors[i])

plt.show()