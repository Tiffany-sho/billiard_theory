import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from setting import wall_width, wall_height ,squre_set

fig ,ax = plt.subplots()
squre_set(ax)

position = np.array([0.0,0.0])
velocity = np.array([0.0,0.1])

dot, = plt.plot([] ,[] , "o" , color = "black" ,ms = 3)

def init():
    dot.set_data([], [])
    return dot,

def update(frame):

    position[0] += velocity[0]
    position[1] += velocity[1]

    if np.abs(round(position[0],5)) == wall_width /2 :
        velocity[0] *= -1
    if np.abs(round(position[1],5)) == wall_height /2 :
        velocity[1] *= -1

    dot.set_data([position[0]], [position[1]])
    return dot,

ani = FuncAnimation(fig, update, frames=1000, init_func=init,interval=50 ,repeat=False,blit=True)

ax.set_aspect('equal')
plt.show()