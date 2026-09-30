import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from stadium import Stadium

bound_num = 100

wall_width =2.0
wall_height =2.0

position = np.array([0.25 ,0.55])
velocity = np.array([0.5,0.01])

print(np.linalg.norm(velocity))

sinai = Stadium(position,velocity,wall_width,wall_height,bound_num)
# sinai.poincare("blue")
sinai.liner()
