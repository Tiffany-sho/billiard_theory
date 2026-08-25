import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from setting import stadium_set,stadium_poincare_map_arc_set
from stadium_func import find_intersection_reversion ,find_reflect_direction ,get_arc_length ,get_normal_vector

class Stadium:
    def __init__(self ,position ,velocity ,W ,H ,bound_num):
        self.positions = [position.copy()]
        self.velocities = [velocity.copy()]
        self.width = W
        self.height = H
        self.bound_num = bound_num

        p = position.copy()
        v = velocity.copy()

        for _ in range(bound_num):

            intersection = find_intersection_reversion(p ,v ,W , H )
            p[:2] = intersection[:2]
            reflected_velocity = find_reflect_direction(p ,v ,W  )
            v[:2] = reflected_velocity[:2]

            self.positions.append(p.copy())
            self.velocities.append(v.copy())

        self.range_sin = 2.0
        self.range_arc = 2 * (W  + H / 2 * np.pi )


    def liner(self):

        fig ,ax = plt.subplots()
        stadium_set(ax ,self.width ,self.height )

        # 高速化(2026-08-25): 以前は for ループで1点ずつ append していた。
        #   positions は (bound_num + 1, 2) の配列そのものなので、まとめて取り出す。
        p = np.asarray(self.positions)
        p_x = p[:, 0]
        p_y = p[:, 1]

        def update(frame):
            plt.plot([p_x[frame]],[p_y[frame]] , "o",color = "black" ,ms = 3)

            # 高速化(2026-08-25): 衝突と衝突の間は直線なので、端点2つで同じ図になる。
            #   以前は linspace で 100 点に分割して描いていた（点数が50倍）。
            #   さらに「x が変化しないなら同じ値を100個並べる」という分岐もあったが、
            #   np.linspace(a, a, 100) は普通に動くので、もともと不要な分岐だった。
            plt.plot([p_x[frame], p_x[frame + 1]], [p_y[frame], p_y[frame + 1]],
                     color = "black" ,linewidth = 1 ,alpha=0.1)

        # ani をローカル変数に束縛しておくのは必須。参照が消えると matplotlib が
        # アニメーションを破棄してしまう（plt.show() がブロックする間だけ生きている）。
        ani = FuncAnimation(fig, update, frames=len(self.positions) - 1, interval=100 ,repeat=False )

        ax.set_aspect('equal')
        plt.show()

    def poincare(self,color):

        arc_length = []
        reflection_sin = []

        # 修正(2026-08-25): 以前は range(self.bound_num) だった。
        #   positions[0] は「初期位置」であって衝突点ではない（内点のことが多い）。
        #   それを断面に混ぜたうえで、最後の衝突 positions[bound_num] を捨てていた。
        #   例: main/stadium/poincare.py の初期値 [0.5, 0.0] は内点だが、
        #       get_arc_length はエラーを出さず 12.354 という無意味な値を返していた。
        #   衝突点は positions[1] 〜 positions[bound_num] なので range(1, bound_num + 1)。
        for i in range(1, self.bound_num + 1):

            set_arc_length = get_arc_length(self.positions[i],self.width,self.height)

            n = get_normal_vector(self.positions[i],self.width,self.height)

            v_norm = self.velocities[i] / np.linalg.norm(self.velocities[i])

            cross_2d = v_norm[0] * n[1] - v_norm[1] * n[0]
            
            set_reflection_sin = cross_2d

            arc_length.append(set_arc_length)
            reflection_sin.append(set_reflection_sin)

        plt.scatter(arc_length,reflection_sin,s=0.05, color=color)

    def create_occupany_area(self,divide,start = 0,end = None):
        """[start, end) の衝突を (s, sinφ) 平面の divide x divide 格子に集計する。

        高速化(2026-08-25): 以前は毎回 range(self.bound_num) を最初から数え直していた。
          shannon_entropy_mix のように衝突回数を増やしながら繰り返し呼ぶ使い方では
          同じ点を何度も数えることになり、全体の仕事量が O(N^2) になっていた。
          区間を指定できるようにして、呼び出し側が差分だけ足せるようにした。
          引数を省略したときの挙動は従来どおり range(0, bound_num) で変わらない。
        """
        if end is None:
            end = self.bound_num

        d_reflected_sin = self.range_sin / divide
        d_arc_length = self.range_arc / divide
        occupancy_index = np.zeros((divide ,divide))

        # TODO(未修正): poincare() と同じ off-by-one がここにも残っている。
        #   start の既定値が 0 なので positions[0](初期位置・衝突点ではない)を1個数え、
        #   最後の衝突 positions[bound_num] を捨てている。
        #   エントロピー周りの修正(divide が無視される件・端のビンが範囲外に出る件)と
        #   まとめて直すべきなので、ここでは意図的に手を付けていない。
        for i in range(start, end):

            set_arc_length = get_arc_length(self.positions[i],self.width,self.height)

            n = get_normal_vector(self.positions[i],self.width,self.height)

            v_norm = self.velocities[i] / np.linalg.norm(self.velocities[i])

            cross_2d = v_norm[0] * n[1] - v_norm[1] * n[0]
            
            set_reflection_sin = cross_2d

            reflected_sin_sign = 1 if set_reflection_sin >= 0 else 0
            arc_length_sign = 1 if set_arc_length >= 0 else 0

            reflected_sin_index = - int(set_reflection_sin / d_reflected_sin + reflected_sin_sign) +  int( divide / 2 ) 
            arc_length_index =  int(set_arc_length / d_arc_length + arc_length_sign) + int( divide / 2) - 1
            
            occupancy_index[reflected_sin_index][arc_length_index] += 1

        return occupancy_index
    
    def paint_occupany_area(self,divide):

        fig_1,ax_1 = plt.subplots()
        stadium_poincare_map_arc_set(ax_1,wall_width,wall_height)

        d_reflected_sin = self.range_sin / divide
        d_arc_length = self.range_arc / divide

        index = self.create_occupany_area(50)

        max_value = index.max()
        
        for i in range(0,divide):
            range_sin_min = self.range_sin / 2 - d_reflected_sin * i
            range_sin_max = self.range_sin / 2 - d_reflected_sin * (i + 1)
            for j in range(0,divide):
                range_arc_min = - self.range_arc / 2 + d_arc_length* j
                range_arc_max = - self.range_arc / 2 + d_arc_length * (j + 1)

                alpha = index[i][j] / max_value
                plt.fill_between([range_arc_min, range_arc_max],range_sin_min, range_sin_max, color="green", alpha=alpha)
        plt.show()

    def shannon_entropy_value(self,occupancy_index,n_samples):
        """集計済みヒストグラムからシャノンエントロピー[bit]を返す（描画も print もしない）。

        高速化(2026-08-25): 以前は shannon_entropy の中で divide x divide の
          二重 for ループを回して1セルずつ足していた。500回呼ぶと 125 万回の
          Python ループになる。numpy でまとめて計算する。
          0 のセルを除くのは 0 * log2(0) を避けるため（従来の continue と同じ意味）。

        分離した理由: 集計(create_occupany_area)・計算(ここ)・描画を分けておくと、
          衝突回数を増やしながらの繰り返しで集計だけを差分更新できる。
        """
        p = occupancy_index[occupancy_index > 0] / n_samples
        return float(-np.sum(p * np.log2(p)))

    def shannon_entropy(self,divide):
        # 注意(2026-08-25): このメソッドには未修正のバグが2つ残っている。
        #   ・引数 divide を無視して create_occupany_area(50) を決め打ちしている
        #   ・そのくせ下の二重ループは range(divide) を回るので、divide != 50 だと
        #     集計と合計の範囲が食い違う（divide > 50 なら IndexError）
        #   衝突回数を振って比べる用途では main/*/shannon_entropy_mix.py 側の
        #   create_occupany_area + shannon_entropy_value の組み合わせを使うこと。
        #   そちらは差分集計なので桁違いに速く、divide も正しく効く。

        index = self.create_occupany_area(50)

        d_reflected_sin = self.range_sin / divide
        d_arc_length = self.range_arc / divide

        shannon_entropy = 0
        part_area = d_arc_length * d_reflected_sin
        all_area =  self.range_arc * self.range_sin

        for i in range(0,divide ):
            for j in range(0,divide ):

                if index[i][j] == 0 :
                    continue
                shannon_entropy += (index[i][j] / self.bound_num) * np.log2(index[i][j] / self.bound_num)
        
        plt.scatter(np.log2(self.bound_num) , -shannon_entropy ,c = "green",s = 5)
        print(f"最大シャノンエントロピー:{-np.log2(part_area/all_area)}")
        print(f"衝突回数:{self.bound_num},シャノンエントロピー:{-shannon_entropy}")
