import numpy as np


esp = 1.0e-14

def newton_method (a ,b ,c ,range):

    d = b * b -4 * a * c
    if d >= 0 :
        init_fx = range
        error = a * init_fx ** 2 + b * init_fx + c
        x = init_fx
        while error > esp :
            # print(error)
            new_x = (a * x ** 2 - c) /(2 * a * x + b )
            x = new_x
            error = a * x ** 2 + b * x + c

        return x
 