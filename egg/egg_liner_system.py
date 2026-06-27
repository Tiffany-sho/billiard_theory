import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/egg'))

from setting import egg_set,egg_poincare_map,egg_set_asy
from egg_poincare_map import create_poincare_dot
from find_intersection_func import find_intersection_func 
from find_reflect_direction import find_reflect_direction

max_frame_ordit = 100
max_frame_poincare = 100

wall_width_right = 10.0
wall_width_left = 10.0
wall_height =8.0

focus_plus = np.sqrt((wall_width_right/2) ** 2 - (wall_height/2) ** 2)
focus_minus = -np.sqrt((wall_width_right/2) ** 2 - (wall_height/2) ** 2)

sita = np.random.rand() * 2 * np.pi - np.pi
position_1 = np.array([2.0,0.0])
velocity_1 = np.array([np.cos(sita) , np.sin(sita) ])
# velocity_1 = np.array([0.000  ,np.sin(sita)/100 ])
print(f"初期値:{position_1}")
print(f"初速度:{velocity_1}")

def egg_liner_system(initial_position,initial_velocity,W_r,W_l,H):

    fig ,ax = plt.subplots()
    # egg_set_asy(ax,W_r,W_l,H, np.sqrt(5) / 2)
    egg_set(ax,W_r,W_l,H)
    ax.set_aspect('equal')
    plt.plot([initial_position[0]],[initial_position[1]] , "o",color = "black" ,ms = 3)
    position = initial_position.copy()
    velocity = initial_velocity.copy()

    def update(frame):

        intersection = find_intersection_func(position,velocity,W_r ,W_l, H)
        reflected_velocity = find_reflect_direction(intersection,velocity,W_r,W_l,H)
        plt.plot([intersection[0]],[intersection[1]] , "o",color = "black" ,ms = 3)

        ordit_x = np.linspace(intersection[0] ,position[0] ,100) if intersection[0] - position[0] != 0 else [position[0] for _ in range(100)]
        ordit_y = velocity[1] /velocity[0] * (ordit_x - position[0]) + position[1] if velocity[0] != 0 else np.linspace(intersection[1] ,position[1] ,100)

        plt.plot(ordit_x,ordit_y,color = "black" ,linewidth = 1 ,alpha=0.1)

        L_plus = (velocity[1] * focus_plus + velocity[0] * position[1] -velocity[1] * position[0]) / np.sqrt(velocity[0] ** 2 + velocity[1] ** 2)
        L_minus = (velocity[1] * focus_minus + velocity[0] * position[1] -velocity[1] * position[0]) / np.sqrt(velocity[0] ** 2 + velocity[1] ** 2)

        print(L_plus)
        print(L_minus)
        position[:2] = intersection[:2]
        velocity[:2] = reflected_velocity[:2]



        if  frame != 0 and np.allclose(position[0] , position[:2]) and np.allclose(velocity[0] , velocity[:2]): 
            print(f"起動周期性あり。{frame}回衝突")
            frame = max_frame_ordit
        

    ani = FuncAnimation(fig, update, frames=max_frame_ordit, interval=10 ,repeat=False)

    plt.show()

def egg_poincare_system(initial_position,initial_velocity,W_r,W_l,H):

    fig ,ax = plt.subplots()
    egg_poincare_map(ax,W_r,W_l,H)
    ax.set_aspect('equal')

    position = initial_position.copy()
    velocity = initial_velocity.copy()

    def update(frame):

        intersection = find_intersection_func(position,velocity,W_r ,W_l, H)
        reflected_velocity = find_reflect_direction(intersection,velocity,W_r,W_l,H)

        set_arc_angle = np.arctan2(intersection[1],intersection[0])

        # jacobian = get_jacobian(W_r,W_l,H,set_arc_angle)
        if intersection[0] == 0:
            n = np.array([0 , - np.sign(velocity[1])])
        elif intersection[0] > 0:
            n = np.array([ - ((H /2) ** 2 * intersection[0]) ,- (W_r /2) ** 2 * intersection[1]])
        else:
            n = np.array([ - ((H /2) ** 2 * intersection[0]) ,- (W_l /2) ** 2 * intersection[1]])



        n_norm = n / np.linalg.norm(n)
        v_norm = reflected_velocity / np.linalg.norm(reflected_velocity)

        cross_2d =  v_norm[0] * n_norm[1] - v_norm[1] * n_norm[0]
        
        set_reflection_sin = cross_2d 

        # inner_2d = np.dot(n_norm,v_norm)
        # set_reflection_sin = inner_2d 

        position[:2] = intersection[:2]
        velocity[:2] = reflected_velocity[:2]
        plt.plot([set_arc_angle],[set_reflection_sin] , "o",color = "red" ,ms = 3.0)


    ani = FuncAnimation(fig, update, frames=max_frame_poincare, interval=10 ,repeat=False)

    plt.show()


def get_poincare_map(initial_position,initial_velocity,W_r,W_l,H):

    fig ,ax = plt.subplots()
    egg_poincare_map(ax,W_r,W_l,H)
    create_poincare_dot(initial_position,initial_velocity,W_r,W_l,H,"red")
    plt.show()

# get_poincare_map(position_1,velocity_1,wall_width_right,wall_width_left,wall_height)
# egg_poincare_system(position_1,velocity_1,wall_width_right,wall_width_left,wall_height)
egg_liner_system(position_1,velocity_1,wall_width_right,wall_width_left,wall_height)