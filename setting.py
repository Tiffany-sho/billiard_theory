import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

basic_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

def squre_set(ax,W,H) :
    ax.plot(0, 0)
    ax.set_xlim(-W /2 -1.0, W /2 + 1.0)
    ax.set_ylim(-H /2 -1.0, H /2 + 1.0)

    W_x = np.linspace(-W /2 ,W /2 ,100)
    wall_heigth_y = np.linspace(-H /2 ,H /2 ,100)

    plt.plot(W_x, [H/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot(W_x, [-H/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot([W/2 for _ in range(100)] ,wall_heigth_y , linewidth = 1,color='black')
    plt.plot([-W/2 for _ in range(100)] ,wall_heigth_y , linewidth = 1,color='black')

def stadium_set(ax,W,H) :

    ax.plot(0, 0)
    ax.set_xlim(-W /2 -H, W /2 +H)
    ax.set_ylim(-H /2 -1.0, H /2 + 1.0)

    W_x = np.linspace(-W /2 ,W /2 ,100)
    wall_circle_y = np.linspace(-H /2 , H /2 ,1000000)
    right_circle = np.sqrt(((H /2) **2 - wall_circle_y ** 2)) 

    plt.plot(W_x, [H/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot(W_x, [-H/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot(right_circle + W /2 ,wall_circle_y , linewidth = 1,color='black')
    plt.plot(-right_circle - W /2,wall_circle_y , linewidth = 1,color='black')

def sinai_set(ax,W,H,D) :
    ax.plot(0, 0)
    ax.set_xlim(-W /2 -1.0, W /2 + 1.0)
    ax.set_ylim(-H /2 -1.0, H /2 + 1.0)

    W_x = np.linspace(-W /2 ,W /2 ,100)
    wall_heigth_y = np.linspace(-H /2 ,H /2 ,100)

    plt.plot(W_x, [H/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot(W_x, [-H/2 for _ in range(100)] , linewidth = 1,color='black')
    plt.plot([W/2 for _ in range(100)] ,wall_heigth_y , linewidth = 1,color='black')
    plt.plot([-W/2 for _ in range(100)] ,wall_heigth_y , linewidth = 1,color='black')

    sinai_circle_x = np.linspace(-D /2 , D /2 ,10000)
    sinai_up_circle_y = np.sqrt(((D /2) **2 - sinai_circle_x ** 2)) 
    sinai_down_circle_y = -np.sqrt(((D /2) **2 - sinai_circle_x ** 2))

    plt.plot(sinai_circle_x ,sinai_up_circle_y , linewidth = 1,color='black')
    plt.plot(sinai_circle_x,sinai_down_circle_y , linewidth = 1,color='black')

def ellipse_set(ax,W,H) :
    ax.plot(0, 0)
    ax.set_xlim(-W /2 -1.0, W /2 + 1.0)
    ax.set_ylim(-H /2 -1.0, H /2 + 1.0)

    x = np.linspace(-W /2 ,W /2 ,10000)
    y = (H /2) * np.sqrt(1 - (x / (W / 2)) ** 2)

    plt.plot(x,y,linewidth = 1,color='black')
    plt.plot(x,-y,linewidth = 1,color='black')

    

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

def stadium_poincare_map_arc_set(ax,W,H):
    ax.set_title(f"W = {W},H = {H}")
    ax.axvline(x=W/2,color = "red" ,linestyle="--")
    ax.axvline(x=-W/2,color = "red" ,linestyle="--")
    ax.axvline(x=W/2 + H/2*np.pi,color = "red" ,linestyle="--")
    ax.axvline(x=-W/2 - H/2*np.pi,color = "red" ,linestyle="--")
    ax.plot(0, 0)
    ax.set_xlim(-(W + H * np.pi / 2), W + H * np.pi / 2)

def squrt_poincare_map_arc_set(ax,W,H):
    ax.set_title(f"W = {W},H = {H}")
    ax.axvline(x=W/2,color = "red" ,linestyle="--")
    ax.axvline(x=-W/2,color = "red" ,linestyle="--")
    ax.axvline(x=W/2 + H,color = "red" ,linestyle="--")
    ax.axvline(x=-W/2 - H,color = "red" ,linestyle="--")
    ax.plot(0, 0)
    ax.set_xlim(-(W + H ), W + H )
