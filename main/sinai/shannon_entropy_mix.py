import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from setting import occupancy_rate_gragh
from sinai import Sinai

wall_width =5.0
wall_height =5.0
sinai_circle_diameter = 2.0

position = np.array([0.5,0.0])
velocity = np.array([0.1 ,0.5])

range_sin = 2.0
range_arc = 2 * (wall_width  + wall_height + np.pi * sinai_circle_diameter / 2)

divide = 50

epoch = 500
step = 100
bound_num_max = epoch * step

fig,ax = plt.subplots()
occupancy_rate_gragh(ax)

all_area =  range_arc * range_sin
part_area = all_area / divide ** 2

billiard = Sinai(position ,velocity ,wall_width ,wall_height ,sinai_circle_diameter ,bound_num_max)

# ヒストグラムは差分更新にする。
#   毎回 0 から数え直すと集計だけで合計 12,525,000 点ぶんのループになるが、
#   増えた step 点ぶんだけ足せば合計 50,000 点で済む。
occupancy_index = np.zeros((divide ,divide))
counted = 0

print(f"max_shannon_entropy:{-np.log2(part_area/all_area)}")

for i in range(0,epoch):
    bound_num = (i + 1) * step

    occupancy_index += billiard.create_occupany_area(divide ,start = counted ,end = bound_num)
    counted = bound_num

    entropy = billiard.shannon_entropy_value(occupancy_index ,bound_num)

    ax.scatter(np.log2(bound_num) ,entropy ,c = "green" ,s = 5)
    print(f"bound_num:{bound_num},shannon_entropy:{entropy}")

ax.axhline(y=-np.log2(part_area/all_area),color = "red" ,linestyle="--")
plt.show()