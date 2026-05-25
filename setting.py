import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

wall_width =1.0
wall_height =1.0

half_circle_diameter =1.0

sinai_wall_height = 2.0
sinai_circle_diameter = 1.0

initial_position = np.array([0.0 ,0.4])
initial_velocity = np.array([0.01, 0.01])

def squre_set(ax) :
    ax.plot(0, 0)
    ax.set_xlim(-wall_width /2 -1.0, wall_width /2 + 1.0)
    ax.set_ylim(-wall_height /2 -1.0, wall_height /2 + 1.0)

    wall_width_x = np.linspace(-wall_width /2 ,wall_width /2 ,100)
    wall_heigth_y = np.linspace(-wall_height /2 ,wall_height /2 ,100)

    plt.plot(wall_width_x, [wall_height/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot(wall_width_x, [-wall_height/2 for _ in range(100)] , linewidth = 1,color='black')
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

def sinai_set(ax) :
    ax.plot(0, 0)
    ax.set_xlim(-wall_width /2 -1.0, wall_width /2 + 1.0)
    ax.set_ylim(-sinai_wall_height /2 -1.0, sinai_wall_height /2 + 1.0)

    wall_width_x = np.linspace(-wall_width /2 ,wall_width /2 ,100)
    wall_heigth_y = np.linspace(-sinai_wall_height /2 ,sinai_wall_height /2 ,100)

    plt.plot(wall_width_x, [sinai_wall_height/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot(wall_width_x, [-sinai_wall_height/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot([wall_width/2 for _ in range(100)] ,wall_heigth_y , linewidth = 1,color='black')
    plt.plot([-wall_width/2 for _ in range(100)] ,wall_heigth_y , linewidth = 1,color='black')

    sinai_circle_x = np.linspace(-sinai_circle_diameter /2 , sinai_circle_diameter /2 ,10000)
    sinai_up_circle_y = np.sqrt(((half_circle_diameter /2) **2 - sinai_circle_x ** 2)) 
    sinai_down_circle_y = -np.sqrt(((half_circle_diameter /2) **2 - sinai_circle_x ** 2))

    plt.plot(sinai_circle_x ,sinai_up_circle_y , linewidth = 1,color='black')
    plt.plot(sinai_circle_x,sinai_down_circle_y , linewidth = 1,color='black')

def poincare_map_set(ax,W,H):

    ax.set_title(f"W = {W},H = {H}")

    ax.plot(0, 0)
    ax.set_xlim(-np.acos(-1), np.acos(-1))

    ax.axvline(x=np.atan2(H,W),color = "red" ,linestyle="--",label = "atan(W/H)")
    ax.axvline(x=-np.atan2(H,W),color = "red" ,linestyle="--",label = "-atan(W/H)")
    ax.axvline(x=np.atan2(H,W) - np.pi,color = "red" ,linestyle="--",label = "atan(W/H)")
    ax.axvline(x=-np.atan2(H,W) + np.pi,color = "red" ,linestyle="--",label = "-atan(W/H)")

    ax.set_xticks([-np.pi,-3*np.pi/4, -np.pi/2,-np.pi/4, 0,np.pi/4, np.pi/2,3*np.pi/4, np.pi])
    ax.set_xticklabels([r'$-\pi$',r'$-3\pi/4$', r'$-\pi/2$',r'$-\pi/4$', r'$0$',r'$\pi/4$', r'$\pi/2$',r'$-3\pi/4$', r'$\pi$'])

def poincare_map_arc_set(ax):
    ax.plot(0, 0)
    ax.set_xlim(-(wall_width + half_circle_diameter * np.pi / 2), wall_width + half_circle_diameter * np.pi / 2)
