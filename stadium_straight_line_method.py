import numpy as np
import matplotlib.pyplot as plt

fig ,ax = plt.subplots()
ball_radius = 0.001
wall_thickness =0.01
wall_width =40.0
wall_half_dismeter =20.0

initial_position = np.array([-25.26516389 , 5.40553205])
initial_velocity = np.array([-0.10999383 ,-0.02071958])

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
    temp_intersection_y = velocity[1]/np.abs(velocity[1]) * wall_half_dismeter /2
    print(temp_intersection_y)

    if np.abs(temp_intersection_x) <= wall_width /2 :
        intersection[0] = temp_intersection_x
        intersection[1] = temp_intersection_y
    elif temp_intersection_x > wall_width /2 :
        a = 1 + incline * incline 
        b = -wall_width /2 - point[0] * incline * incline +  incline * point[1]
        c = wall_width * wall_width /4 + incline * incline * point[0] * point[0] -2 * incline *point[0] * point[1] + point[1] * point[1] - wall_half_dismeter * wall_half_dismeter / 4

        intersection[0] = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
        intersection[1] = velocity[1]/np.abs(velocity[1]) * np.sqrt((wall_half_dismeter /2) ** 2 - (intersection[0] - wall_width /2) **2 )

    elif temp_intersection_x < -wall_width /2 :
        

        a = 1 + incline * incline 
        b = wall_width /2 - point[0] * incline * incline +  incline * point[1]
        c = wall_width * wall_width /4 + incline * incline * point[0] * point[0] -2 * incline *point[0] * point[1] + point[1] * point[1] - wall_half_dismeter * wall_half_dismeter / 4

        print(incline)
        intersection[0] = (-b + velocity[0] /np.abs(velocity[0]) * np.sqrt(b * b -  a * c)) / a
        intersection[1] = velocity[1]/np.abs(velocity[1]) * np.sqrt((wall_half_dismeter /2) ** 2 - (intersection[0] + wall_width /2) ** 2 )
    
    return intersection


# for i in range(10) :

#     position = np.array([np.random.rand() *10 -30,np.random.rand() * 20 - 10])
#     velocity = np.array([np.random.rand() * 2 - 1, np.random.rand() * 2 - 1])
#     intersection = find_intersection(position,velocity)

#     print("-------------------------------------")
#     print(f"初期値:{position}")
#     print(f"初速度:{velocity}")
#     print(f"y = {velocity[1] /velocity[0]}x + {-velocity[1] /velocity[0] * position[0] + position[1]}")
#     print(intersection)

#     plt.plot([intersection[0]],[intersection[1]] , "o")

#     ordit_x = np.linspace(-(wall_width + wall_half_dismeter)/2 ,(wall_width + wall_half_dismeter)/2 ,100)
#     ordit_y = velocity[1] /velocity[0] * (ordit_x - position[0]) + position[1]

#     plt.plot(ordit_x,ordit_y)

    
first_intersection = find_intersection(initial_position,initial_velocity)

print(first_intersection)

plt.plot([first_intersection[0]],[first_intersection[1]] , "o")

ordit_x = np.linspace(-(wall_width + wall_half_dismeter)/2 ,(wall_width + wall_half_dismeter)/2 ,100)
ordit_y = initial_velocity[1] /initial_velocity[0] * (ordit_x - initial_position[0]) + initial_position[1]

plt.plot(ordit_x,ordit_y)

ax.set_aspect('equal')
plt.show()