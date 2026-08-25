import numpy as np
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../class'))

from stadium import Stadium

bound_num = 35

wall_width =5.0
wall_height =5.0

position = np.array([0.5  ,0.0])
velocity = np.array([0.02/np.sqrt(29),0.05/np.sqrt(29)])

print(np.linalg.norm(velocity))

sinai = Stadium(position,velocity,wall_width,wall_height,bound_num)
sinai.poincare("blue")
sinai.liner()
