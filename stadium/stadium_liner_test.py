import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))

from setting import wall_width, half_circle_diameter ,initial_position ,initial_velocity,stadium_set
from find_intersection_func import find_intersection
from find_intersection_reversion import find_intersection_reversion

basic_colors = ['red', 'blue', 'green', 'orange', 'purple', 'black', 'cyan', 'magenta']

fig ,ax = plt.subplots()
stadium_set(ax)

print("-------------------------------------")
print(f"初期値:{initial_position}")
print(f"初速度:{initial_velocity}")


for i in range(20) :

    position = np.array([np.random.rand() *wall_width - wall_width /2,np.random.rand() * half_circle_diameter - half_circle_diameter/2])
    velocity = np.array([np.random.rand() * 2 - 1, np.random.rand() * 2 - 1])
    intersection = find_intersection(position,velocity,wall_width, half_circle_diameter)
    intersection_reversion = find_intersection_reversion(position,velocity,wall_width, half_circle_diameter)

    print("-------------------------------------")
    print(f"初期値:{position}")
    print(f"初速度:{velocity}")
    print(f"y = {velocity[1] /velocity[0]}x + {-velocity[1] /velocity[0] * position[0] + position[1]}")
    print(f"代入法{intersection}")
    print(f"パラメータ法{intersection_reversion}")
    plt.plot(position[0],position[1],"o", color = basic_colors[i % 8])
    plt.plot([intersection[0]],[intersection[1]] , "o" ,color = basic_colors[i % 8])
    plt.plot([intersection_reversion[0]],[intersection_reversion[1]] , "o" ,color = basic_colors[i % 8] ,mfc = "white")

    ordit_x = np.linspace(velocity[0] /np.abs(velocity[0])*(wall_width + half_circle_diameter)/2 ,position[0] ,100)
    ordit_y = velocity[1] /velocity[0] * (ordit_x - position[0]) + position[1]

    plt.plot(ordit_x,ordit_y ,color = basic_colors[i % 8])

    
# first_intersection = find_intersection(initial_position,initial_velocity,wall_width, half_circle_diameter)

# print(first_intersection)

# plt.plot([initial_position[0]],[initial_position[1]] , "o")
# plt.plot([first_intersection[0]],[first_intersection[1]] , "o")

# ordit_x = np.linspace(-(wall_width + half_circle_diameter)/2 ,(wall_width + half_circle_diameter)/2 ,100)
# ordit_y = initial_velocity[1] /initial_velocity[0] * (ordit_x - initial_position[0]) + initial_position[1]

# plt.plot(ordit_x,ordit_y)

ax.set_aspect('equal')
plt.show()