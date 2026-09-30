import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from egg import Egg

bound_num = 100

# 既定値は docs/contracts.md §4
wall_width_right = 6.0
wall_width_left = 3.0
wall_height = 4.0

position = np.array([0.3 ,0.1])
velocity = np.array([0.02 ,0.05]) / np.sqrt(29)

print(np.linalg.norm(velocity))

egg = Egg(position ,velocity ,wall_width_right ,wall_width_left ,wall_height ,bound_num)
egg.poincare("blue")
egg.liner()
