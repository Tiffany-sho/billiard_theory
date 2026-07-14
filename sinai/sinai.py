import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/sinai'))

from setting import sinai_set,sinai_poincare_map_arc,occupancy_rate_gragh
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction
from get_n_vector_arc_length import get_n_vector_arc_length
from create_setting import sinai_create_setting

max_frame = 10000

wall_width =5.0
wall_height =5.0
sinai_circle_diameter = 1.0

position_1 = np.array([0.5,0.0])
velocity_1 = np.array([10.1 ,0.1])

class Sinai:
    def __init__(self ,position ,velocity ,W ,H ,D ,bound_num):
        self.positions = [position.copy()]
        self.velocities = [velocity.copy()]
        self.width = W
        self.height = H
        self.dismeter = D
        self.bound_num = bound_num

        p = position.copy()
        v = velocity.copy()

        for _ in range(bound_num):

            intersection = find_intersection_reversion(p ,v ,W , H ,D )
            p[:2] = intersection[:2]
            reflected_velocity = find_reflect_direction(p ,v ,W , H ,D )
            v[:2] = reflected_velocity[:2]

            self.positions.append(p.copy())
            self.velocities.append(v.copy())

        self.range_sin = 2.0
        self.range_arc = 2 * (W  + H + np.pi * D / 2)


    def liner(self):

        fig ,ax = plt.subplots()
        sinai_set(ax ,self.width ,self.height ,self.dismeter )

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
        sinai_poincare_map_arc(ax,self.width ,self.height ,self.dismeter )

        arc_length = []
        reflection_sin = []
        
        for i in range(self.bound_num):

            set_arc_length ,n= get_n_vector_arc_length(self.positions[i],self.width ,self.height ,self.dismeter )

            n_norm = n / np.linalg.norm(n)
            v_norm = self.velocities[i] / np.linalg.norm(self.velocities[i])

            cross_2d = v_norm[0] * n_norm[1] - v_norm[1] * n_norm[0]
            
            set_reflection_sin = cross_2d 

            arc_length.append(set_arc_length)
            reflection_sin.append(set_reflection_sin)

        plt.scatter(arc_length,reflection_sin,s=0.05, color=color)
        plt.show()

    def create_occupany_area(self,divide):

        d_reflected_sin = self.range_sin / divide
        d_arc_length = self.range_arc / divide
        occupancy_index = np.zeros((divide ,divide))

        
        for i in range(self.bound_num):

            set_arc_length ,n= get_n_vector_arc_length(self.positions[i],self.width ,self.height ,self.dismeter )

            n_norm = n / np.linalg.norm(n)
            v_norm = self.velocities[i] / np.linalg.norm(self.velocities[i])

            cross_2d = v_norm[0] * n_norm[1] - v_norm[1] * n_norm[0]
            
            set_reflection_sin = cross_2d 

            reflected_sin_sign = 1 if set_reflection_sin >= 0 else 0
            arc_length_sign = 1 if set_arc_length >= 0 else 0

            reflected_sin_index = - int(set_reflection_sin / d_reflected_sin + reflected_sin_sign) +  int( divide / 2 ) 
            arc_length_index =  int(set_arc_length / d_arc_length + arc_length_sign) - 1
            
            occupancy_index[reflected_sin_index][arc_length_index] += 1

        return occupancy_index
    
    def paint_occupany_area(self,divide):

        fig_1,ax_1 = plt.subplots()
        sinai_poincare_map_arc(ax_1,wall_width,wall_height,sinai_circle_diameter)

        d_reflected_sin = self.range_sin / divide
        d_arc_length = self.range_arc / divide

        index = self.create_occupany_area(50)

        max_value = index.max()
        
        for i in range(0,divide):
            range_sin_min = self.range_sin / 2 - d_reflected_sin * i
            range_sin_max = self.range_sin / 2 - d_reflected_sin * (i + 1)
            for j in range(0,divide):
                range_arc_min = d_arc_length* j
                range_arc_max = d_arc_length * (j + 1)

                alpha = index[i][j] / max_value
                plt.fill_between([range_arc_min, range_arc_max],range_sin_min, range_sin_max, color="green", alpha=alpha)
        plt.show()

    def shannon_entropy(self,divide):

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


sinai_1 = Sinai(position_1,velocity_1,wall_width,wall_height,sinai_circle_diameter,max_frame)

sinai_1.shannon_entropy(50)