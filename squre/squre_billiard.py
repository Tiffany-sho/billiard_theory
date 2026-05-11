import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig ,ax = plt.subplots()
ax.plot(0, 0)
position = np.array([0.0, 0.0])
velocity = np.array([-0.05, 0.02])

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

ax.plot([4, 4], [4, -4],color="black",linewidth = 1.0)
ax.plot([4, -4], [-4, -4],color="black",linewidth = 1.0)
ax.plot([-4, -4], [-4, 4],color="black",linewidth = 1.0)
ax.plot([-4, 4], [4, 4],color="black",linewidth = 1.0)

dot, = plt.plot([], [], "o" , markersize=4.0)

def update(frame):
    position[0] += velocity[0]
    position[1] += velocity[1]

    if np.abs(round(position[0],5)) == 4.00 :
        velocity[0] *= -1
    if np.abs(round(position[1],5)) == 4.00 :
        velocity[1] *= -1
    dot.set_data([position[0]], [position[1]])
    return dot,

ani = FuncAnimation(fig, update, frames=1000, interval=50 ,repeat=False,blit=True)
plt.show()