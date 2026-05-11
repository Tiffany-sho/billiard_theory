import numpy as np
import matplotlib.pyplot as plt

wall_width =4.0
half_circle_diameter =2.0

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