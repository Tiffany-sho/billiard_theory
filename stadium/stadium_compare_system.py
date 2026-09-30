import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))

from setting import stadium_set ,basic_colors
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction

wall_width =2.0
half_circle_diameter =2.0

# 粒子の数（ここだけ変えればよい）
particle_num =20

# 全粒子で共通の初期位置
initial_position = np.array([0.25,0.55])
# 初速度: x成分は共通、y成分を 0.010 から 0.001 刻みでずらす
# (10+i)/1000 と整数で割るのは、0.010+0.001*i だと 0.013000000000000001 のように末尾がずれるため
velocity_x =0.5
def velocity_y(i):
    return (10 + i) / 1000

# True にすると粒子ごとに basic_colors で色分けする
use_colors =False

fig ,ax = plt.subplots()
stadium_set(ax,wall_width,half_circle_diameter)

positions_init = [initial_position.copy() for _ in range(particle_num)]
velocities_init = [np.array([velocity_x ,velocity_y(i)]) for i in range(particle_num)]

dots = []
for i in range(particle_num):
    color = basic_colors[i % len(basic_colors)] if use_colors else "black"
    dot, = plt.plot([] ,[] , "o" , color = color ,ms = 3)
    dots.append(dot)

def create_ordit_dot(initial_position ,initial_velocity):

    positions = [initial_position.copy()]
    velocities = [initial_velocity.copy()]
    intersections = []

    p = initial_position.copy()
    v = initial_velocity.copy()

    for _ in range(50):
        intersection = find_intersection_reversion(p ,v ,wall_width ,half_circle_diameter)
        intersections.append(intersection.copy())
        v = find_reflect_direction(intersection ,v ,wall_width)
        p = intersection.copy()
        positions.append(p.copy())
        velocities.append(v.copy())

    ordit_x = []
    ordit_y = []
    for i in range(len(intersections)):

        norm_length = np.linalg.norm(positions[i] - intersections[i])
        norm_velocity = np.linalg.norm(velocities[i])


        time = max(int(norm_length /norm_velocity *10) ,2)

        seg_x = np.linspace(positions[i][0], intersections[i][0] , time )
        seg_y = np.linspace(positions[i][1], intersections[i][1] , time )

        ordit_x.extend(seg_x)
        ordit_y.extend(seg_y)

    return [ordit_x ,ordit_y]

ordits = [create_ordit_dot(positions_init[i] ,velocities_init[i]) for i in range(particle_num)]

frame_num = min(len(ordit[0]) for ordit in ordits)

def update(frame):

    for dot ,ordit in zip(dots ,ordits):
        dot.set_data([ordit[0][frame]],[ordit[1][frame]])

    return dots


ani = FuncAnimation(fig, update, frames=frame_num, interval=10 ,repeat=False ,blit=True)

ax.set_aspect('equal')
plt.show()
