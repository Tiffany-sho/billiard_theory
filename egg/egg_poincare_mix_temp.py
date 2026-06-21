import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/calcuate'))

from egg_poincare_map import create_poincare_dot
from create_setting import create_setting
from setting import egg_poincare_map,egg_set,basic_colors

save_dir_poincare = "egg/graph_data/poincare_depend_wr_wl_h_polar"
save_dir_ordit = "egg/graph_data/ordit_depend_wr_wl_h_polar"
os.makedirs(save_dir_poincare, exist_ok=True)
os.makedirs(save_dir_ordit, exist_ok=True)

np.random.shuffle(basic_colors)

epoch = 100
epoch_per_sita = 2 * np.pi / epoch

for a in range(0, 11):
    for b in range(0, 11):

        wall_width_right = round(0.1 * a + 1.0 ,1)
        wall_width_left = round(0.1 * b + 1.0 ,1)
        wall_height = 1.0

        fig_ordit ,ax_ordit = plt.subplots()
        egg_set(ax_ordit,wall_width_right,wall_width_left,wall_height)
        ax_ordit.set_aspect('equal')
        filename_ordit = f"{save_dir_ordit}/ordit_{wall_width_right}_{wall_width_left}_{wall_height}.png"
        fig_ordit.savefig(filename_ordit)
        print(f"画像を保存しました: {filename_ordit}")
        plt.close(fig_ordit)

        fig_poincare ,ax_poincare = plt.subplots()
        egg_poincare_map(ax_poincare,wall_width_right,wall_width_left,wall_height)

        for i in range(0,epoch):
            position,velocity = create_setting(i,wall_width_right,wall_width_left,wall_height,epoch_per_sita)
            create_poincare_dot(position,velocity,wall_width_right,wall_width_left,wall_height ,basic_colors[i%100])

        filename_poincare = f"{save_dir_poincare}/poincare_{wall_width_right}_{wall_width_left}_{wall_height}.png"
        fig_poincare.savefig(filename_poincare ,dpi = 300)
        print(f"画像を保存しました: {filename_poincare}")
        plt.close(fig_poincare)
