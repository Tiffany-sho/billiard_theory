import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig ,ax = plt.subplots()
ball_radius = 0.001
wall_thickness =0.01
wall_width =40.0
wall_half_dismeter =20.0

ax.plot(0, 0)
position = np.array([9.0, 0.0])
velocity = np.array([0.015, 0.05])

ax.set_xlim(-wall_width /2 -wall_half_dismeter, wall_width /2 +wall_half_dismeter)
ax.set_ylim(-wall_half_dismeter /2 -5.0, wall_half_dismeter /2 +5.0)

wall_top = patches.Rectangle((-wall_width/2, wall_half_dismeter/2), wall_width, wall_thickness, color='black')
ax.add_patch(wall_top)
wall_bottom = patches.Rectangle((wall_width/2, -wall_half_dismeter/2), -wall_width, wall_thickness, color='black')
ax.add_patch(wall_bottom)
wall_left = patches.Arc(xy=(-wall_width/2, 0),width=wall_half_dismeter, height=wall_half_dismeter ,theta1= 90 , theta2=270 ,linewidth=1, color='black')
ax.add_patch(wall_left)
wall_rigth = patches.Arc(xy=(wall_width/2, 0),width=wall_half_dismeter, height=wall_half_dismeter ,theta1= -90 , theta2=90,linewidth=1, color='black')
ax.add_patch(wall_rigth)

def update(frame):
    global velocity
    position[0] += velocity[0]
    position[1] += velocity[1]

    if  np.abs(position[0]) >= wall_width  / 2 - ball_radius:
        position_r = np.sqrt((np.abs(position[0]) - wall_width/2) ** 2 + position[1] ** 2)
        if position_r >= wall_half_dismeter /2 - ball_radius:
            sita = np.atan((np.abs(position[0]) - wall_width/2)/position[1])
            rotate_matrix = np.array([[np.cos(2*sita) , -np.sin(2*sita)],[np.sin(2*sita) , -np.cos(2*sita)]])
            print(sita)
            print(rotate_matrix)
            velocity = np.dot(velocity,rotate_matrix)

    if np.abs(position[1]) >= wall_half_dismeter / 2 - ball_radius :
        velocity[1] *= -1
    ball = patches.Circle((position[0],position[1]),radius = ball_radius ,color ="black")
    ax.add_patch(ball)

ax.set_aspect('equal')

ani = FuncAnimation(fig, update, frames=10000, interval=0.001 ,repeat=False)

plt.show()