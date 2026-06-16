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

epoch = 100

c = np.linspace(0, 1, epoch)
cmap = plt.get_cmap('turbo') 
colors_rgba = cmap(c)

epoch_per_sita = 2 * np.pi / epoch

for a in range(1, 3):
    for b in range(1, 3):
        for c in range(1, 3):

            wall_width_right = float(a)
            wall_width_left = float(b)
            wall_height = float(c)

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
                print("初期値を設定中...") 
                position,velocity = create_setting(i,wall_width_right,wall_width_left,wall_height,epoch_per_sita)
                print("ポアンカレ断面を作成中...")
                create_poincare_dot(position,velocity,wall_width_right,wall_width_left,wall_height ,colors_rgba[i])

            filename_poincare = f"{save_dir_poincare}/poincare_{wall_width_right}_{wall_width_left}_{wall_height}.png"
            fig_poincare.savefig(filename_poincare ,dpi = 300)
            print(f"画像を保存しました: {filename_poincare}")
            plt.close(fig_poincare)

# plt.show()
