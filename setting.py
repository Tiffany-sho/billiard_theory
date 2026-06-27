import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

basic_colors = [
  "#FF0000", "#FF1C1C", "#FF3838", "#FF5555", "#FF7171", "#FF8D8D", "#FFAAAA", "#FFC6C6", "#FFE2E2", "#FF007F",
  "#FF4500", "#FF5714", "#FF6928", "#FF7B3C", "#FF8D50", "#FF9F64", "#FFA500", "#D2691E", "#A0522D", "#8B4513",
  "#FFD700", "#FFDB19", "#FFDF33", "#FFE34D", "#FFE766", "#FFEB80", "#FFEF99", "#FFF3B2", "#FFF7CC", "#FFFF00",
  "#ADFF2F", "#A0F02A", "#93E225", "#86D320", "#79C51B", "#6CB616", "#5FA811", "#52990C", "#458B07", "#32CD32",
  "#00FF00", "#00E600", "#00CC00", "#00B300", "#009900", "#008000", "#006600", "#004D00", "#003300", "#228B22",
  "#00FA9A", "#00FF7F", "#20B2AA", "#2E8B57", "#3CB371", "#008B8B", "#008080", "#00CED1", "#48D1CC", "#40E0D0",
  "#00FFFF", "#19FFFF", "#33FFFF", "#4DFFFF", "#66FFFF", "#80FFFF", "#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF",
  "#0000FF", "#0000E6", "#0000CC", "#0000B3", "#000099", "#000080", "#000066", "#4169E1", "#0000CD", "#00008B",
  "#8A2BE2", "#9400D3", "#9932CC", "#8B008B", "#800080", "#4B0082", "#483D8B", "#6A5ACD", "#7B68EE", "#9370DB",
  "#FF00FF", "#EE00EE", "#DD00DD", "#CC00CC", "#BB00BB", "#AA00AA", "#C71585", "#FF1493", "#FF69B4", "#DB7093"
]

def squre_set(ax,W,H) :
    ax.set_title(f"W = {W},H = {H}")
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
    ax.set_title(f"W = {W},H = {H}")
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
    ax.set_title(f"W = {W},H = {H} D = {D}")
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
    ax.set_title(f"W = {W},H = {H}")
    ax.plot(0, 0)
    ax.set_xlim(-W /2 -1.0, W /2 + 1.0)
    ax.set_ylim(-H /2 -1.0, H /2 + 1.0)

    x = np.linspace(-W /2 ,W /2 ,10000)
    y = (H /2) * np.sqrt(1 - (x / (W / 2)) ** 2)

    plt.plot(x,y,linewidth = 1,color='black')
    plt.plot(x,-y,linewidth = 1,color='black')

def egg_set(ax,W_r,W_l,H) :
    ax.set_title(f"W_r = {W_r},W_l = {W_l},H = {H}")
    ax.plot(0, 0)
    ax.set_xlim(-W_l /2 -1.0, W_r /2 + 1.0)
    ax.set_ylim(-H /2 -1.0, H /2 + 1.0)

    x_l = np.linspace(-W_l /2 ,0 ,10000)
    y_l = (H /2) * np.sqrt(1 - (x_l / (W_l / 2)) ** 2)
    x_r = np.linspace(0 ,W_r/2 ,10000)
    y_r = (H /2) * np.sqrt(1 - (x_r / (W_r / 2)) ** 2)

    focus_r = np.array([np.sqrt((W_r/2) ** 2 - (H/2) ** 2),0]) if W_r > H else np.array([[0 , 0],[np.sqrt(- (W_r/2) ** 2 + (H/2) ** 2) , -np.sqrt(- (W_r/2) ** 2 + (H/2) ** 2)]]) 
    focus_l = np.array([-np.sqrt((W_l/2) ** 2 - (H/2) ** 2),0]) if W_l > H else np.array([0,np.sqrt(- (W_l/2) ** 2 + (H/2) ** 2)]) 

    plt.scatter(focus_r[0],focus_r[1],s=10.0, color="blue")
    plt.scatter(focus_l[0],focus_l[1],s=10.0, color="red")

    plt.plot(x_l,y_l,linewidth = 1,color='black')
    plt.plot(x_l,-y_l,linewidth = 1,color='black')
    
    plt.plot(x_r,y_r,linewidth = 1,color='black')
    plt.plot(x_r,-y_r,linewidth = 1,color='black')

    plt.xlabel("x")
    plt.ylabel("y")

    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)

def egg_set_asy(ax,W_r,W_l,H,v) :
    ax.set_title(f"W_r = {W_r},W_l = {W_l},H = {H}")
    ax.plot(0, 0)
    ax.set_xlim(-W_l /2 -1.0, W_r /2 + 1.0)
    ax.set_ylim(-H /2 -1.0, H /2 + 1.0)

    x_l = np.linspace(-W_l /2 ,0 ,10000)
    y_l = (H /2) * np.sqrt(1 - (x_l / (W_l / 2)) ** 2)
    x_r = np.linspace(0 ,W_r/2 ,10000)
    y_r = (H /2) * np.sqrt(1 - (x_r / (W_r / 2)) ** 2)

    focus_r = np.array([np.sqrt((W_r/2) ** 2 - (H/2) ** 2),0]) if W_r > H else np.array([[0 , 0],[np.sqrt(- (W_r/2) ** 2 + (H/2) ** 2) , -np.sqrt(- (W_r/2) ** 2 + (H/2) ** 2)]]) 
    focus_l = np.array([-np.sqrt((W_l/2) ** 2 - (H/2) ** 2),0]) if W_l > H else np.array([0,np.sqrt(- (W_l/2) ** 2 + (H/2) ** 2)]) 

    x_asy_plus = np.linspace(-W_l /2 ,W_r /2 ,100)
    y_asy_plus = v * x_asy_plus
    x_asy_minus = np.linspace(-W_l /2 ,W_r /2 ,100)
    y_asy_minus = -v * x_asy_minus

    plt.scatter(focus_r[0],focus_r[1],s=10.0, color="blue")
    plt.scatter(focus_l[0],focus_l[1],s=10.0, color="red")

    plt.plot(x_l,y_l,linewidth = 1,color='black')
    plt.plot(x_l,-y_l,linewidth = 1,color='black')
    
    plt.plot(x_r,y_r,linewidth = 1,color='black')
    plt.plot(x_r,-y_r,linewidth = 1,color='black')

    plt.plot(x_asy_plus,y_asy_plus,linewidth = 1,color='black')
    plt.plot(x_asy_minus,y_asy_minus,linewidth = 1,color='black')

    plt.xlabel("x")
    plt.ylabel("y")

    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)

    

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

def ellipse_poincare_map(ax,W,H):
    ax.set_title(f"W = {W},H = {H}")
    ax.axvline(x=np.pi/2,color = "red" ,linestyle="--")
    ax.axvline(x=-np.pi/2,color = "red" ,linestyle="--")
    ax.plot(0, 0)
    ax.set_xlim(-(np.pi ), np.pi )
    ax.set_ylim(-(1 ), 1 )

def egg_poincare_map(ax,W_r,W_l,H):
    ax.set_title(f"W_r = {W_r},W_l = {W_l},H = {H}")
    ax.axvline(x=np.pi/2,color = "red" ,linestyle="--")
    ax.axvline(x=-np.pi/2,color = "red" ,linestyle="--")
    ax.plot(0, 0)
    ax.set_xlim(-np.pi , np.pi )
    ax.set_ylim(-1 , 1 )