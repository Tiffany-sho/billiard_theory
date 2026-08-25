import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from setting import egg_set,egg_poincare_map
from egg_func import find_intersection_func ,find_reflect_direction ,get_normal_vector

class Egg:
    def __init__(self ,position ,velocity ,W_r ,W_l ,H ,bound_num):
        self.positions = [position.copy()]
        self.velocities = [velocity.copy()]
        self.width_right = W_r
        self.width_left = W_l
        self.height = H
        self.bound_num = bound_num

        p = position.copy()
        v = velocity.copy()

        for _ in range(bound_num):

            intersection = find_intersection_func(p ,v ,W_r ,W_l ,H )
            p[:2] = intersection[:2]
            reflected_velocity = find_reflect_direction(p ,v ,W_r ,W_l ,H )
            v[:2] = reflected_velocity[:2]

            self.positions.append(p.copy())
            self.velocities.append(v.copy())


    def liner(self):

        fig ,ax = plt.subplots()
        egg_set(ax ,self.width_right ,self.width_left ,self.height )

        p_x = []
        p_y = []
        for i in range(len(self.positions)):

            p_x.append(self.positions[i][0])
            p_y.append(self.positions[i][1])

        
        def update(frame):
            plt.plot([p_x[frame]],[p_y[frame]] , "o",color = "black" ,ms = 3)
            ordit_x = np.linspace(p_x[frame] ,p_x[frame + 1] ,100) if p_x[frame] - p_x[frame + 1] != 0 else [p_x[frame + 1] for _ in range(100)]
            ordit_y = np.linspace(p_y[frame] ,p_y[frame + 1] ,100) if p_y[frame] - p_y[frame + 1] != 0 else [p_y[frame + 1] for _ in range(100)]

            plt.plot(ordit_x,ordit_y,color = "black" ,linewidth = 1 ,alpha=0.1)


        ani = FuncAnimation(fig, update, frames=len(self.positions) - 1, interval=100 ,repeat=False )   

        ax.set_aspect('equal')
        plt.show()

    def poincare(self,color):

        fig ,ax = plt.subplots()
        egg_poincare_map(ax,self.width_right ,self.width_left ,self.height)

        arc_length = []
        reflection_sin = []

        # 修正(2026-08-25): 以前は range(self.bound_num) だった。
        #   positions[0] は「初期位置」であって衝突点ではない（内点のことが多い）。
        #   それを断面に混ぜたうえで、最後の衝突 positions[bound_num] を捨てていた。
        #   衝突点は positions[1] 〜 positions[bound_num] なので range(1, bound_num + 1)。
        #
        # 修正(2026-08-25): 法線を egg_func.get_normal_vector に一元化し、内向きへ揃えた。
        #   以前はここに外向きの勾配 ∇F ∝ (b²x, a²y) がインラインで書かれており、
        #   内向きに統一されたスタジアム/シナイと符号規約が逆だった（この断面だけ上下反転）。
        #   x == 0 を (0, sign(vy)) と速度で場合分けしていた枝も併せて解消している。
        #   詳細は class/egg_func.py: get_normal_vector のコメント。
        for i in range(1, self.bound_num + 1):

            set_arc_angle = np.arctan2(self.positions[i][1],self.positions[i][0])

            # jacobian = get_jacobian(W_r,W_l,H,set_arc_angle)
            n = get_normal_vector(self.positions[i] ,self.width_right ,self.width_left ,self.height)

            n_norm = n / np.linalg.norm(n)
            v_norm = self.velocities[i] / np.linalg.norm(self.velocities[i])

            cross_2d = v_norm[0] * n_norm[1] - v_norm[1] * n_norm[0]
            
            set_reflection_sin = cross_2d 

            arc_length.append(set_arc_angle)
            reflection_sin.append(set_reflection_sin)

        plt.scatter(arc_length,reflection_sin,s=0.05, color=color)
        plt.show()

