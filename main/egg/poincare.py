import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from egg import Egg

bound_num = 100

# 既定値は docs/contracts.md §4
wall_width_right = 6.0
wall_width_left = 8.0
wall_height = 5.0

position = np.array([0.5 ,0.7])
velocity = np.array([-0.02 ,0.95])
print(np.linalg.norm(velocity))

egg = Egg(position ,velocity ,wall_width_right ,wall_width_left ,wall_height ,bound_num)
egg.poincare("blue")
egg.liner()
