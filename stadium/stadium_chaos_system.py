import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../func/stadium'))

from setting import wall_width, half_circle_diameter ,stadium_set
from find_intersection_reversion import find_intersection_reversion
from find_reflect_direction import find_reflect_direction

fig ,ax = plt.subplots()
stadium_set(ax)

position = np.array([0.0,0.0])
velocity = np.array([9.0 ,0.0001])

dot, = plt.plot([] ,[] , "o" , color = "black" ,ms = 3)

positions = [position.copy()]
velocities = [velocity.copy()]
intersections = []

p = position.copy()
v = velocity.copy()

for _ in range(1000):
    intersection = find_intersection_reversion(p ,v ,wall_width ,half_circle_diameter)
    intersections.append(intersection.copy())
    v = find_reflect_direction(intersection ,v ,wall_width)
    p = intersection.copy()
    positions.append(p.copy())
    velocities.append(v.copy())


ordit_x = []
ordit_y = []
for i in range(len(intersections)):

    divide_x = int(abs((positions[i][0] - intersections[i][0]) / velocities[i][0]) *100) if velocities[i][0] != 0.0 else None
    divide_y = int(abs((positions[i][1] - intersections[i][1]) / velocities[i][1]) *100) if velocities[i][1] != 0.0 else None

    if divide_x and divide_y :
    
        seg_x = np.linspace(positions[i][0], intersections[i][0] , divide_x )
        seg_y = np.linspace(positions[i][1], intersections[i][1] , divide_y )

    else:
        divide_num = divide_x if divide_x else divide_y

        seg_x = np.linspace(positions[i][0], intersections[i][0] , divide_num )
        seg_y = np.linspace(positions[i][1], intersections[i][1] , divide_num )

    ordit_x.extend(seg_x)
    ordit_y.extend(seg_y)

def update(frame):

    dot.set_data([ordit_x[frame]],[ordit_y[frame]])

    return dot,


ani = FuncAnimation(fig, update, frames=1000, interval=10 ,repeat=False ,blit=True)

ax.set_aspect('equal')
plt.show()