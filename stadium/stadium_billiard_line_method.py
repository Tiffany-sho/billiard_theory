import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig ,ax = plt.subplots()
ball_radius = 0.001
wall_thickness =0.01
wall_width =40.0
wall_half_dismeter =20.0

position = np.array([np.random.rand() *40 - 20,np.random.rand() * 20 - 10])
velocity = np.array([np.random.rand() * 2 - 1, np.random.rand() * 2 - 1])

print("-------------------------------------")
print(f"初期値:{position}")
print(f"初速度:{velocity}")

ax.plot(0, 0)
ax.set_xlim(-wall_width /2 -wall_half_dismeter, wall_width /2 +wall_half_dismeter)
ax.set_ylim(-wall_half_dismeter /2 -5.0, wall_half_dismeter /2 +5.0)

wall_width_x = np.linspace(-wall_width /2 ,wall_width /2 ,100)
wall_circle_y = np.linspace(-wall_half_dismeter /2 , wall_half_dismeter /2 ,100)
right_circle = np.sqrt(((wall_half_dismeter /2) **2 - wall_circle_y ** 2)) 

plt.plot(wall_width_x, [wall_half_dismeter/2 for _ in range(100)] , linewidth = 1,color='black')
plt.plot(wall_width_x, [-wall_half_dismeter/2 for _ in range(100)] , linewidth = 1,color='black')
plt.plot(right_circle + wall_width /2 ,wall_circle_y , linewidth = 1,color='black')
plt.plot(-right_circle - wall_width /2,wall_circle_y , linewidth = 1,color='black')

def find_reflect_direction(intersection,velocity) :

    reflected_velocity = np.array([0.0,0.0])

    if np.abs(intersection[0]) <= wall_width /2 :
        reflected_velocity[0] = velocity[0]
        reflected_velocity[1] = -velocity[1]

    else:
        sita = np.atan((np.abs(intersection[0]) - wall_width/2)/intersection[1])
        rotate_matrix = np.array([[np.cos(2*sita) , -np.sin(2*sita)],[np.sin(2*sita) , -np.cos(2*sita)]])
        reflected_velocity = np.dot(velocity,rotate_matrix)

    return reflected_velocity


def update(frame):

    intersection = find_intersection(position,velocity)

    print("-------------------------------------")
    print(f"位置:{position}")
    print(f"速度:{velocity}")
    print(f"y = {velocity[1] /velocity[0]}x + {-velocity[1] /velocity[0] * position[0] + position[1]}")
    print(intersection)
    plt.plot(position[0],position[1],"o",color = "black")
    plt.plot([intersection[0]],[intersection[1]] , "o",color = "black")

    ordit_x = np.linspace(intersection[0] ,position[0] ,100)
    ordit_y = velocity[1] /velocity[0] * (ordit_x - position[0]) + position[1]

    plt.plot(ordit_x,ordit_y,color = "black")

    position[0] = intersection[0]
    position[1] = intersection[1]

    reflected_velocity = find_reflect_direction(intersection,velocity)

    velocity[0] = reflected_velocity[0]
    velocity[1] = reflected_velocity[1]

ani = FuncAnimation(fig, update, frames=10, interval=500 ,repeat=False)

ax.set_aspect('equal')
plt.show()