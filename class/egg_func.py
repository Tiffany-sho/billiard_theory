import math

import numpy as np

from vector_func import norm2


def find_intersection_func(point,velocity,W_r ,W_l , H) :

    if velocity[0] == 0 and velocity[1] == 0 :
        return point.copy()
    
    if velocity[0] == 0 :
        x = point[0]
        if point[0] == 0 :
            y = np.sign(velocity[1]) * H / 2
        elif point[0] > 0 :
            y = np.sign(velocity[1]) * H / 2 * np.sqrt(1 - (x / (W_r /2)) ** 2)
        else:
            y = np.sign(velocity[1]) * H / 2 * np.sqrt(1 - (x / (W_l /2)) ** 2)
        return np.array([x ,y ])
    
    if velocity[1] == 0 :
        y = point[1]
        if point[1] == 0 :
            if velocity[0] > 0 :
                x =  W_r / 2
            else:
                x =  - W_l / 2
        elif point[1] > 0 :
            if velocity[0] > 0 :
                x = W_r / 2 * np.sqrt(1 - (y / (H /2)) ** 2)
            else:
                x = - W_l / 2 * np.sqrt(1 - (y / (H /2)) ** 2)
        else:
            if velocity[0] > 0 :
                x =  W_r / 2 * np.sqrt(1 - (y / (H /2)) ** 2)
            else:
                x = - W_l / 2 * np.sqrt(1 - (y / (H /2)) ** 2)
        return np.array([x ,y ])


    
    temp_intersection_y = H /2 if velocity[1] > 0 else -H /2
    temp_intersection_t =( temp_intersection_y - point[1] ) / velocity[1]

    if temp_intersection_t > 0:
        temp_intersection_x = point[0] + temp_intersection_t * velocity[0]
        if temp_intersection_x == 0:
            return np.array([0 , np.sign(velocity[1]) * H / 2])
        elif temp_intersection_x > 0:
            A_right = (velocity[0] / (W_r / 2)) ** 2 + (velocity[1] / (H / 2)) ** 2 
            B_right = point[0] * velocity[0] / (W_r / 2) ** 2 + point[1] * velocity[1] / (H / 2) ** 2
            C_right = (point[0] / (W_r / 2)) ** 2 + (point[1] / (H / 2)) ** 2 - 1
            D_right = B_right ** 2 - A_right * C_right


            right_t =np.inf
            if D_right >= 0 :

                if B_right == 0 :
                    t1 = np.sqrt(- A_right * C_right) / A_right
                    t2 = C_right / A_right / t1

                else:
                    # 高速化: 判別式は直前の D_right で計算済み。
                    #   以前は同じ式を np.sqrt の中で書き直して2回計算していた。
                    t1 = (- B_right -np.sign(B_right) * np.sqrt(D_right)) / A_right
                    t2 = C_right / A_right / t1

                valid_t = [t for t in (t1, t2) if t > 0]
                if valid_t:
                    right_t = max(valid_t)
                    
                    return point + right_t * velocity
        
        elif temp_intersection_x < 0:
            A_left = (velocity[0] / (W_l / 2)) ** 2 + (velocity[1] / (H / 2)) ** 2 
            B_left = point[0] * velocity[0] / (W_l / 2) ** 2 + point[1] * velocity[1] / (H / 2) ** 2
            C_left = (point[0] / (W_l / 2)) ** 2 + (point[1] / (H / 2)) ** 2 - 1
            # 修正: 右側と同じ理由で ** 2 に統一（x*x と x**2 のずれ対策）。
            D_left = B_left ** 2 - A_left * C_left


            left_t =np.inf
            if D_left >= 0 :
                if B_left == 0 :
                    t1 = np.sqrt(- A_left * C_left) / A_left
                    t2 = C_left / A_left / t1

                else:
                    # 高速化: 判別式は直前の D_left で計算済み（右側と同じ理由）。
                    t1 = (- B_left -np.sign(B_left) * np.sqrt(D_left)) / A_left
                    t2 = C_left / A_left / t1

                valid_t = [t for t in (t1, t2) if t > 0]
                if valid_t:
                    left_t = max(valid_t)
                    
                    return point + left_t * velocity

def get_normal_vector(intersection ,W_r ,W_l ,H):
    # 【規約】ここが返す n は「領域の内側を向く」法線（正規化はしていない）。
    #   境界 F(x,y) = (x/a)^2 + (y/b)^2 - 1 の勾配 ((H/2)^2 x, (W/2)^2 y) は
    #   外向きなので、符号を反転して内向きに揃える。
    W = W_r if intersection[0] > 0 else W_l

    n = np.array([ ((H /2) ** 2 * intersection[0]) ,(W /2) ** 2 * intersection[1]])

    return -n


def find_reflect_direction(intersection,velocity,W_r,W_l,H) :
    speed = norm2(velocity)

    if intersection[0] == 0 :
        return np.array([velocity[0] ,-velocity[1]])

    n = get_normal_vector(intersection ,W_r ,W_l ,H)
    n_norm = norm2(n)

    n_hat = n / n_norm

    reflected = velocity - 2 * np.dot(velocity,n_hat) * n_hat

    # 反射で |v| は理論上変わらないが、丸め誤差の蓄積を防ぐため毎回正規化し直す。
    return reflected / norm2(reflected) * speed


# ---------------------------------------------------------------- 弧長 s
#
# ポアンカレ断面の横軸。原点は右頂点 (W_r/2, 0)、反時計回りが正で、
# s ∈ (-L/2, L/2]（L は全周長）。定義は docs/contracts.md §2-5。
#
# 楕円弧の長さは不完全楕円積分 E(φ|m) になる。scipy は使わず、
# Carlson の対称形 R_F / R_D（Numerical Recipes 2nd ed. §6.11 の rf / rd）で出す。
# 三角関数を一切使わず、衝突点の座標から cos t = x/a, sin t = y/b を直接取るので、
# 四則演算と sqrt だけで閉じる（simulation.html の JS とビット単位で揃う）。

def carlson_rf(x ,y ,z):
    # R_F(x, y, z)。x, y, z >= 0 で、0 になってよいのは高々1つ。
    # ERRTOL = 0.0025 で相対誤差は約 6e-17（倍精度の丸めと同程度）。
    ERRTOL = 0.0025
    while True:
        sx = math.sqrt(x)
        sy = math.sqrt(y)
        sz = math.sqrt(z)
        lam = sx * (sy + sz) + sy * sz
        x = 0.25 * (x + lam)
        y = 0.25 * (y + lam)
        z = 0.25 * (z + lam)
        ave = (x + y + z) / 3.0
        dx = (ave - x) / ave
        dy = (ave - y) / ave
        dz = (ave - z) / ave
        if max(abs(dx) ,abs(dy) ,abs(dz)) <= ERRTOL:
            break
    e2 = dx * dy - dz * dz
    e3 = dx * dy * dz
    return (1.0 + (e2 / 24.0 - 0.1 - 3.0 / 44.0 * e3) * e2 + e3 / 14.0) / math.sqrt(ave)


def carlson_rd(x ,y ,z):
    # R_D(x, y, z)。x, y >= 0（0 は高々1つ）、z > 0。
    ERRTOL = 0.0015
    C1 = 3.0 / 14.0
    C2 = 1.0 / 6.0
    C3 = 9.0 / 22.0
    C4 = 3.0 / 26.0
    C5 = 0.25 * C3
    C6 = 1.5 * C4
    total = 0.0
    fac = 1.0
    while True:
        sx = math.sqrt(x)
        sy = math.sqrt(y)
        sz = math.sqrt(z)
        lam = sx * (sy + sz) + sy * sz
        total += fac / (sz * (z + lam))
        fac = 0.25 * fac
        x = 0.25 * (x + lam)
        y = 0.25 * (y + lam)
        z = 0.25 * (z + lam)
        ave = 0.2 * (x + y + 3.0 * z)
        dx = (ave - x) / ave
        dy = (ave - y) / ave
        dz = (ave - z) / ave
        if max(abs(dx) ,abs(dy) ,abs(dz)) <= ERRTOL:
            break
    ea = dx * dy
    eb = dz * dz
    ec = ea - eb
    ed = ea - 6.0 * eb
    ee = ed + ec + ec
    return 3.0 * total + fac * (1.0 + ed * (-C1 + C5 * ed - C6 * dz * ee)
                                + dz * (C2 * ee + dz * (-C3 * ec + dz * C4 * ea))) / (ave * math.sqrt(ave))


def ellipe_inc(sin_p ,cos_p ,m):
    # 不完全楕円積分 E(φ|m) = ∫_0^φ sqrt(1 - m sin^2 θ) dθ（0 <= φ <= π/2）。
    # φ そのものではなく sin φ, cos φ を受け取る。
    q = 1.0 - m * sin_p * sin_p
    c2 = cos_p * cos_p
    return sin_p * carlson_rf(c2 ,q ,1.0) - m / 3.0 * (sin_p * sin_p * sin_p) * carlson_rd(c2 ,q ,1.0)


def ellipe(m):
    # 完全楕円積分 E(m) = E(π/2|m)。
    q = 1.0 - m
    return carlson_rf(0.0 ,q ,1.0) - m / 3.0 * carlson_rd(0.0 ,q ,1.0)


def quarter_arc(a ,b):
    # 半軸 a（x 方向）, b（y 方向）の楕円の 1/4 周長。
    if a <= b:
        r = a / b
        return b * ellipe(1.0 - r * r)
    r = b / a
    return a * ellipe(1.0 - r * r)


def half_ellipse_arc(c ,s ,a ,b):
    # x = a cos t, y = b sin t（-π/2 <= t <= π/2）の弧長を t = 0 から符号付きで測る。
    # c = cos t (>= 0), s = sin t を受け取る。
    #   ds/dt = sqrt(a^2 sin^2 t + b^2 cos^2 t)
    #   a <= b : = b sqrt(1 - m sin^2 t),  m = 1 - (a/b)^2  →  b E(t|m)
    #   a >  b : = a sqrt(1 - m cos^2 t),  m = 1 - (b/a)^2  →  a (E(m) - E(π/2 - t|m))
    # どちらも m ∈ [0, 1) に収まるように分けている。
    # ** を使わず掛け算で書く（JS の Math.pow とビット単位で揃える保証がないため）。
    r = math.sqrt(c * c + s * s)
    c = c / r
    s_abs = abs(s) / r
    if a <= b:
        k = a / b
        arc = b * ellipe_inc(s_abs ,c ,1.0 - k * k)
    else:
        k = b / a
        m = 1.0 - k * k
        arc = a * (ellipe(m) - ellipe_inc(c ,s_abs ,m))
    return -arc if s < 0 else arc


def egg_arc_range(W_r ,W_l ,H):
    # (L/2, L_r/2) を返す。s ∈ (-L/2, L/2]、左右の継ぎ目（x = 0）は s = ±L_r/2。
    b = H / 2
    q_r = quarter_arc(W_r / 2 ,b)
    q_l = quarter_arc(W_l / 2 ,b)
    return q_r + q_l ,q_r


def get_arc_length(intersection ,W_r ,W_l ,H):
    # 境界上の点の弧長 s。原点は右頂点 (W_r/2, 0)、反時計回りが正、s ∈ (-L/2, L/2]。
    #   右半分 (x >= 0): 右頂点から測った符号付き弧長そのもの
    #   左半分 (x <  0): 左頂点を s = ±L/2 とし、そこから左の楕円弧を差し引く
    # 左頂点（y == 0 かつ x < 0）はちょうど L/2 に置く（atan2 が π を返すのに合わせる）。
    x = intersection[0]
    y = intersection[1]
    b = H / 2
    if x >= 0:
        a = W_r / 2
        return half_ellipse_arc(x / a ,y / b ,a ,b)
    a = W_l / 2
    half ,_ = egg_arc_range(W_r ,W_l ,H)
    arc_l = half_ellipse_arc(-x / a ,y / b ,a ,b)
    return half - arc_l if y >= 0 else -half - arc_l
