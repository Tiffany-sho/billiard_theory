import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ellipse_poincare_map import create_poincare_dot
from setting import ellipse_poincare_map,basic_colors

wall_width = 4.0
wall_height =3.0

fig ,ax = plt.subplots()
ellipse_poincare_map(ax,wall_width,wall_height)

for i in range(0,100):
    arc = np.random.rand() * 2 * np.pi - np.pi 
    position = np.array([wall_width / 2 * np.cos(arc) ,wall_height / 2 * np.sin(arc)])
    velocity = np.array([(np.random.rand() *2 -1) / 100 ,(np.random.rand() *2 -1) / 100])
    print(f"初期値:{position}")
    print(f"初速度:{velocity}")
    create_poincare_dot(position,velocity,wall_width,wall_height ,basic_colors[i%8])

plt.show()
