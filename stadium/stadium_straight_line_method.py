import numpy as np
import matplotlib.pyplot as plt
from setting import wall_width , wall_half_dismeter

basic_colors = ['red', 'blue', 'green', 'orange', 'purple', 'black', 'cyan', 'magenta']

fig ,ax = plt.subplots()

initial_position = np.array([-29.73045506 ,0.18269073],dtype=np.float64)
initial_velocity = np.array([-0.99300254 , 0.29991922] ,dtype=np.float64)

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

def find_intersection(point,velocity) :

    intersection = np.array([0.0,0.0])

    if velocity[1] == 0 :
        intersection[1] = point[1]
        intersection[0] = velocity[0] /np.abs(velocity[0]) * np.sqrt((wall_half_dismeter /2) ** 2 - intersection[1] ** 2) + velocity[0] /np.abs(velocity[0]) * wall_width / 2
        return intersection

    incline = velocity[1] /velocity[0]
    temp_intersection_x = (velocity[1]/np.abs(velocity[1]) * wall_half_dismeter /2 - point[1]) / incline + point[0]
    temp_intersection_y = incline * (velocity[0]/np.abs(velocity[0])*(wall_width /2 + wall_half_dismeter /2) - point[0]) + point[1]

    if np.abs(temp_intersection_x) <= wall_width /2 :
        intersection[0] = temp_intersection_x
        intersection[1] = velocity[1]/np.abs(velocity[1]) * wall_half_dismeter /2
    elif temp_intersection_x > wall_width /2 :
        a = 1 + incline * incline 
        b = -wall_width /2 - point[0] * incline * incline +  incline * point[1]
        c = wall_width * wall_width /4 + incline * incline * point[0] * point[0] -2 * incline *point[0] * point[1] + point[1] * point[1] - wall_half_dismeter * wall_half_dismeter / 4
        
        if temp_intersection_y >= 0:
            intersection[0] = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            intersection[1] = np.sqrt((wall_half_dismeter /2) ** 2 - (intersection[0] - wall_width /2) **2 )
        else :
            intersection[0] = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            intersection[1] = - np.sqrt((wall_half_dismeter /2) ** 2 - (intersection[0] - wall_width /2) **2 )

        error = (intersection[0] - wall_width /2) ** 2 + intersection[1] ** 2 - (wall_half_dismeter /2 ) ** 2
        print("error_right_circle")
        print(error)

    elif temp_intersection_x < -wall_width /2 :
        
        a = 1 + incline * incline 
        b = wall_width /2 - point[0] * incline * incline +  incline * point[1]
        c = wall_width * wall_width /4 + incline * incline * point[0] * point[0] -2 * incline *point[0] * point[1] + point[1] * point[1] - wall_half_dismeter * wall_half_dismeter / 4

        if temp_intersection_y >= 0:
            intersection[0] = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            intersection[1] = np.sqrt((wall_half_dismeter /2) ** 2 - (intersection[0] + wall_width /2) **2 )
        else :
            intersection[0] = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
            intersection[1] = - np.sqrt((wall_half_dismeter /2) ** 2 - (intersection[0] + wall_width /2) **2 )

        error = (intersection[0] + wall_width /2) ** 2 + intersection[1] ** 2 - (wall_half_dismeter /2 ) ** 2
        print("error_left_circle")
        print(error)
    
    return intersection


for i in range(10) :

    position = np.array([np.random.rand() *40 - 20,np.random.rand() * 20 - 10])
    velocity = np.array([np.random.rand() * 2 - 1, np.random.rand() * 2 - 1])
    intersection = find_intersection(position,velocity)

    # print("-------------------------------------")
    # print(f"初期値:{position}")
    # print(f"初速度:{velocity}")
    # print(f"y = {velocity[1] /velocity[0]}x + {-velocity[1] /velocity[0] * position[0] + position[1]}")
    # print(intersection)
    plt.plot(position[0],position[1],"o", color = basic_colors[i % 8 ])
    plt.plot([intersection[0]],[intersection[1]] , "o" ,color = basic_colors[i % 8 ])

    ordit_x = np.linspace(velocity[0] /np.abs(velocity[0])*(wall_width + wall_half_dismeter)/2 ,position[0] ,100)
    ordit_y = velocity[1] /velocity[0] * (ordit_x - position[0]) + position[1]

    plt.plot(ordit_x,ordit_y ,color = basic_colors[i % 8 ])

    
# first_intersection = find_intersection(initial_position,initial_velocity)

# print(first_intersection)

# plt.plot([initial_position[0]],[initial_position[1]] , "o")
# plt.plot([first_intersection[0]],[first_intersection[1]] , "o")

# ordit_x = np.linspace(-(wall_width + wall_half_dismeter)/2 ,(wall_width + wall_half_dismeter)/2 ,100)
# ordit_y = initial_velocity[1] /initial_velocity[0] * (ordit_x - initial_position[0]) + initial_position[1]

# plt.plot(ordit_x,ordit_y)

ax.set_aspect('equal')
plt.show()