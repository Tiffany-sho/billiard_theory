import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig ,ax = plt.subplots()
ball_radius = 0.05
wall_thickness =0.01
wall_width =40.0
wall_heigth =20.0

ax.plot(0, 0)
position = np.array([0.0, 0.0])
velocity = np.array([-0.01, 0.01])

ax.set_xlim(-wall_width /2 -5.0, wall_width /2 +5.0)
ax.set_ylim(-wall_heigth /2 -5.0, wall_heigth /2 +5.0)

wall_top = patches.Rectangle((-wall_width/2, wall_heigth/2), wall_width, wall_thickness, color='black')
ax.add_patch(wall_top)
wall_bottom = patches.Rectangle((wall_width/2, -wall_heigth/2), -wall_width, wall_thickness, color='black')
ax.add_patch(wall_bottom)
wall_left = patches.Rectangle((-wall_width/2, -wall_heigth/2), wall_thickness, wall_heigth, color='black')
ax.add_patch(wall_left)
wall_rigth = patches.Rectangle((wall_width/2, wall_heigth/2), wall_thickness, -wall_heigth, color='black')
ax.add_patch(wall_rigth)

def update(frame):
    position[0] += velocity[0]
    position[1] += velocity[1]

    if np.abs(round(position[0],5)) == wall_width  / 2 - ball_radius:
        velocity[0] *= -1
    if np.abs(round(position[1],5)) == wall_heigth / 2 - ball_radius :
        velocity[1] *= -1
    ball = patches.Circle((position[0],position[1]),radius = ball_radius ,color ="black")
    ax.add_patch(ball)

ax.set_aspect('equal')

ani = FuncAnimation(fig, update, frames=100, interval=0.1 ,repeat=False)

plt.show()