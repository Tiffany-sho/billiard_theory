import numpy as np
import matplotlib.pyplot as plt

wall_width =2.0
wall_heigth =2.0
half_circle_diameter =1.0

initial_position = np.array([0.0 ,0.5 / np.sqrt(2)])
initial_velocity = np.array([0.002, 0.0])

def squre_set(ax) :
    ax.plot(0, 0)
    ax.set_xlim(-wall_width /2 -1.0, wall_width /2 + 1.0)
    ax.set_ylim(-wall_heigth /2 -1.0, wall_heigth /2 + 1.0)

    wall_width_x = np.linspace(-wall_width /2 ,wall_width /2 ,100)
    wall_heigth_y = np.linspace(-wall_heigth /2 ,wall_heigth /2 ,100)

    plt.plot(wall_width_x, [wall_heigth/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot(wall_width_x, [-wall_heigth/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot([wall_width/2 for _ in range(100)] ,wall_heigth_y , linewidth = 1,color='black')
    plt.plot([-wall_width/2 for _ in range(100)] ,wall_heigth_y , linewidth = 1,color='black')

def stadium_set(ax) :

    ax.plot(0, 0)
    ax.set_xlim(-wall_width /2 -half_circle_diameter, wall_width /2 +half_circle_diameter)
    ax.set_ylim(-half_circle_diameter /2 -1.0, half_circle_diameter /2 + 1.0)

    wall_width_x = np.linspace(-wall_width /2 ,wall_width /2 ,100)
    wall_circle_y = np.linspace(-half_circle_diameter /2 , half_circle_diameter /2 ,1000000)
    right_circle = np.sqrt(((half_circle_diameter /2) **2 - wall_circle_y ** 2)) 

    plt.plot(wall_width_x, [half_circle_diameter/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot(wall_width_x, [-half_circle_diameter/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot(right_circle + wall_width /2 ,wall_circle_y , linewidth = 1,color='black')
    plt.plot(-right_circle - wall_width /2,wall_circle_y , linewidth = 1,color='black')