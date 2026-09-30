import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from sinai import Sinai

bound_num = 100

wall_width =5.0
wall_height =5.0
sinai_circle_diameter = 2.0

position = np.array([1.2  ,-2.5])
velocity = np.array([0.02,0.05])

print(np.linalg.norm(velocity))

sinai = Sinai(position,velocity,wall_width,wall_height,sinai_circle_diameter,bound_num)
# sinai.poincare("blue")
sinai.liner()
