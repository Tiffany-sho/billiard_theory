import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from create_setting import egg_create_setting
from setting import egg_poincare_map_arc,basic_colors
from egg import Egg

wall_width_right = 6.0
wall_width_left = 8.0
wall_height = 4.0

bound_num = 1000

epoch = 100
# 初期値は弧長ではなく媒介変数の角度 [-π, π) を epoch 等分して撒く
# （断面の横軸は弧長 s。撒き方とは別物）
epoch_per_sita = 2 * np.pi / epoch

fig ,ax = plt.subplots()
egg_poincare_map_arc(ax ,wall_width_right ,wall_width_left ,wall_height)

for i in range(0,epoch):

    position,velocity = egg_create_setting(i ,wall_width_right ,wall_width_left ,wall_height ,epoch_per_sita)
    print(f"初期値:{position}")
    print(f"初速度:{velocity}")
    egg = Egg(position ,velocity ,wall_width_right ,wall_width_left ,wall_height ,bound_num)
    egg.poincare(basic_colors[i])

plt.show()
