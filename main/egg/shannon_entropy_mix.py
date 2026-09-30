import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from setting import occupancy_rate_gragh
from egg import Egg

wall_width_right = 6.0
wall_width_left = 3.0
wall_height = 4.0

position = np.array([0.3 ,0.1])
velocity = np.array([0.02 ,0.05]) / np.sqrt(29)

divide = 50

epoch = 50
step = 100
bound_num_max = epoch * step

fig,ax = plt.subplots()
occupancy_rate_gragh(ax)

billiard = Egg(position ,velocity ,wall_width_right ,wall_width_left ,wall_height ,bound_num_max)

# 横軸は弧長 s ∈ (-L/2, L/2]。幅は Egg が持っている
all_area =  billiard.range_arc * billiard.range_sin
part_area = all_area / divide ** 2

# ヒストグラムは差分更新にする（増えた step 点ぶんだけ足す）。
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
