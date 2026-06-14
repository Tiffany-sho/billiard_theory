import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from egg_poincare_map import create_poincare_dot
from setting import egg_poincare_map,basic_colors

save_dir = "egg/graph_data/poincare_depend_wr_wl_h_polar"
os.makedirs(save_dir, exist_ok=True)

for a in range(1,4):
    for b in range(1,4):
        if b <= a:
            continue
        for c in range(1,4):

            wall_width_right = float(a)
            wall_width_left = float(b)
            wall_height =float(c)

            fig ,ax = plt.subplots()
            egg_poincare_map(ax,wall_width_right,wall_width_left,wall_height)

            for i in range(0,50):
                arc = np.random.rand() * 2 * np.pi - np.pi 
                if abs(arc) < np.pi / 2:
                    position = np.array([wall_width_right / 2 * np.cos(arc) ,wall_height / 2 * np.sin(arc)])
                else:
                    position = np.array([wall_width_left / 2 * np.cos(arc) ,wall_height / 2 * np.sin(arc)])

                velocity = np.array([(np.random.rand() *2 -1) / 100 ,(np.random.rand() *2 -1) / 100])
                print(f"初期値:{position}")
                print(f"初速度:{velocity}")
                create_poincare_dot(position,velocity,wall_width_right,wall_width_left,wall_height ,basic_colors[i%7])

            filename = f"{save_dir}/poincare_{wall_width_right}_{wall_width_left}_{wall_height}.png"
            fig.savefig(filename)
            print(f"画像を保存しました: {filename}")

            plt.close(fig)

# plt.show()
