import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/calcuate'))

from egg_poincare_map import create_poincare_dot
from create_setting import create_setting
from setting import egg_poincare_map,egg_set,basic_colors

start_time = time.time()

wall_width_right = 4.0
wall_width_left = 6.0
wall_height =7.0

epoch = 100

c = np.linspace(0, 1, epoch)
cmap = plt.get_cmap('turbo') 
colors_rgba = cmap(c)

epoch_per_sita = 2 * np.pi / epoch

fig ,ax = plt.subplots()
# egg_poincare_map(ax,wall_width_right,wall_width_left,wall_height)
egg_set(ax,wall_width_right,wall_width_left,wall_height)


for i in range(0,epoch):

    position,velocity = create_setting(i,wall_width_right,wall_width_left,wall_height,epoch_per_sita)
    print(f"初期値:{position}")
    print(f"初速度:{velocity}")
    create_poincare_dot(position,velocity,wall_width_right,wall_width_left,wall_height ,colors_rgba[i])

end_time = time.time()
print(f"処理時間: {end_time - start_time:.4f} 秒")
plt.show()

