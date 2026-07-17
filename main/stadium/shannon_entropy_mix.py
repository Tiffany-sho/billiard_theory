import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from setting import occupancy_rate_gragh
from stadium import Stadium

wall_width =5.0
wall_height =5.0
sinai_circle_diameter = 2.0

position = np.array([0.5,0.0])
velocity = np.array([0.1 ,0.5])

range_sin = 2.0
range_arc = 2 * (wall_width  + wall_height * np.pi / 2)

divide = 50

fig,ax = plt.subplots()
occupancy_rate_gragh(ax)

all_area =  range_arc * range_sin
part_area = all_area / divide ** 2

for i in range(0,50):
    stadium = Stadium(position ,velocity ,wall_width ,wall_height ,100 + i * 100)
    stadium.shannon_entropy(divide)
ax.axhline(y=-np.log2(part_area/all_area),color = "red" ,linestyle="--")
plt.show()