import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from create_setting import sinai_create_setting
from setting import sinai_poincare_map_arc,basic_colors
from sinai import Sinai

bound_num = 25

wall_width =5.0
wall_height =5.0
sinai_circle_diameter = 1.0

position = np.array([0.5 / np.sqrt(5) ,1.0 / np.sqrt(5)])
velocity = np.array([0.01 ,0.02])

sinai = Sinai(position,velocity,wall_width,wall_height,sinai_circle_diameter,bound_num)
# sinai.poincare("blue")
sinai.liner()
