import numpy as np

def find_reflect_direction(intersection,velocity,W,H) :
    speed = np.linalg.norm(velocity)
    if np.abs(intersection[0]) == W /2  and np.abs(intersection[1]) == H /2 :
        # 修正(2026-08-25): 以前は np.array([0, 0]) を返していた。
        #   直後の reflected / np.linalg.norm(reflected) が 0/0 になり、
        #   速度が NaN になって以降の軌道が全部壊れていた（黙って進む）。
        #   角は2辺の法線が同時に効くため反射が一意に定まらない measure-zero の場合。
        #   class/sinai_func.py: find_reflect_direction が同じ状況で採っている
        #   「来た道を戻る」に揃える。
        reflected = np.array([-velocity[0] ,-velocity[1]])

    elif np.abs(intersection[0]) == W /2  :
        reflected = np.array([-velocity[0] ,velocity[1]])
    
    else:
        reflected = np.array([velocity[0] ,-velocity[1]])

    return reflected / np.linalg.norm(reflected) * speed