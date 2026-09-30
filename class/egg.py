import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from setting import egg_set
from egg_func import find_intersection_func ,find_reflect_direction ,get_normal_vector ,get_arc_length ,egg_arc_range

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

        # 横軸は弧長 s ∈ (-L/2, L/2]。原点は右頂点、反時計回りが正（docs/contracts.md §2-5）
        half_arc ,_ = egg_arc_range(W_r ,W_l ,H)
        self.range_sin = 2.0
        self.range_arc = 2 * half_arc


    def liner(self):

        fig ,ax = plt.subplots()
        egg_set(ax ,self.width_right ,self.width_left ,self.height )

        p = np.asarray(self.positions)
        p_x = p[:, 0]
        p_y = p[:, 1]

        def update(frame):
            plt.plot([p_x[frame]],[p_y[frame]] , "o",color = "black" ,ms = 3)

            plt.plot([p_x[frame], p_x[frame + 1]], [p_y[frame], p_y[frame + 1]],
                     color = "black" ,linewidth = 1 ,alpha=0.1)

        # ani をローカル変数に束縛しておくのは必須。参照が消えると matplotlib が
        # アニメーションを破棄してしまう（plt.show() がブロックする間だけ生きている）。
        ani = FuncAnimation(fig, update, frames=len(self.positions) - 1, interval=100 ,repeat=False )

        ax.set_aspect('equal')
        plt.show()

    def poincare(self,color):
        # 変更(2026-09-30): 以前はここで figure を作って plt.show() していた。
        #   それだと重ね描き(main/egg/poincare_mix.py)で1本ごとに別ウィンドウになるので、
        #   Sinai / Stadium と同じく「今の ax に点を足すだけ」にした。
        #   軸の設定(setting.py: egg_poincare_map_arc)と plt.show() は呼び出し側で行う。

        arc_length = []
        reflection_sin = []

        for i in range(1, self.bound_num + 1):

            set_arc_length = get_arc_length(self.positions[i] ,self.width_right ,self.width_left ,self.height)

            n = get_normal_vector(self.positions[i] ,self.width_right ,self.width_left ,self.height)

            n_norm = n / np.linalg.norm(n)
            v_norm = self.velocities[i] / np.linalg.norm(self.velocities[i])

            cross_2d = v_norm[0] * n_norm[1] - v_norm[1] * n_norm[0]
            
            set_reflection_sin = cross_2d 

            arc_length.append(set_arc_length)
            reflection_sin.append(set_reflection_sin)

        plt.scatter(arc_length,reflection_sin,s=0.05, color=color)

    def create_occupany_area(self,divide,start = 0,end = None):
        """[start, end) の衝突を (s, sinφ) 平面の divide x divide 格子に集計する。

        格子の切り方は Stadium と同じ（横軸が原点対称なので + divide/2 でずらす）。
        """
        if end is None:
            end = self.bound_num

        d_reflected_sin = self.range_sin / divide
        d_arc_length = self.range_arc / divide
        occupancy_index = np.zeros((divide ,divide))

        # TODO(未修正): Stadium / Sinai と同じ off-by-one と端のビンの問題がここにもある。
        #   start の既定値が 0 なので positions[0](初期位置・衝突点ではない)を1個数え、
        #   最後の衝突 positions[bound_num] を捨てている。
        #   s == L/2（左頂点）ちょうどだと列 index が divide になり IndexError、
        #   sinφ == 1 ちょうどだと行 index が -1 になり最終行に黙って入る。
        #   3形状まとめて直すべきなので、ここでは Stadium と同じ式に揃えてある。
        for i in range(start, end):

            set_arc_length = get_arc_length(self.positions[i] ,self.width_right ,self.width_left ,self.height)

            n = get_normal_vector(self.positions[i] ,self.width_right ,self.width_left ,self.height)

            n_norm = n / np.linalg.norm(n)
            v_norm = self.velocities[i] / np.linalg.norm(self.velocities[i])

            cross_2d = v_norm[0] * n_norm[1] - v_norm[1] * n_norm[0]

            set_reflection_sin = cross_2d

            reflected_sin_sign = 1 if set_reflection_sin >= 0 else 0
            arc_length_sign = 1 if set_arc_length >= 0 else 0

            reflected_sin_index = - int(set_reflection_sin / d_reflected_sin + reflected_sin_sign) +  int( divide / 2 )
            arc_length_index =  int(set_arc_length / d_arc_length + arc_length_sign) + int( divide / 2) - 1

            occupancy_index[reflected_sin_index][arc_length_index] += 1

        return occupancy_index

    def shannon_entropy_value(self,occupancy_index,n_samples):
        """集計済みヒストグラムからシャノンエントロピー[bit]を返す（描画も print もしない）。
        """
        p = occupancy_index[occupancy_index > 0] / n_samples
        return float(-np.sum(p * np.log2(p)))

