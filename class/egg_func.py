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
            # 修正(2026-08-25): 以前はここが B_right * B_right、
            #   下の np.sqrt の中が B_right ** 2 と書き分けられていた。
            #   numpy の float64 では x*x と x**2 が 1 ULP ずれることがあるため、
            #   「D_right >= 0 を通ったのに sqrt には負の値が渡る」ことが起こりうる。
            #   sqrt 側の式に合わせて ** 2 に統一する。
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
    #
    # 修正(2026-08-25): 以前は class/egg.py の poincare() に外向きのまま
    #   インラインで書かれていた。スタジアム/シナイが内向きに統一されたため、
    #   卵型の断面だけ sinφ が上下反転していた。内向きへ揃える。
    #   反射計算 v - 2(v·n̂)n̂ は n の符号に不変で、しかも IEEE754 の符号反転は
    #   厳密なので、軌道はビット単位でも変わらない。変わるのは断面の sinφ の符号だけ。
    #
    #   x == 0（上下の頂点）の特別扱いは不要。x 成分が 0 になるため
    #   W_r / W_l のどちらを使っても向きは (0, -sign(y)) になる。
    #   以前あった (0, sign(vy)) は速度依存で、他の点と意味が揃っていなかった。
    W = W_r if intersection[0] > 0 else W_l

    n = np.array([ ((H /2) ** 2 * intersection[0]) ,(W /2) ** 2 * intersection[1]])

    return -n


def find_reflect_direction(intersection,velocity,W_r,W_l,H) :
    # 高速化(2026-08-25): np.linalg.norm -> norm2（ビット単位で等価。vector_func.py 参照）。
    speed = norm2(velocity)

    if intersection[0] == 0 :
        return np.array([velocity[0] ,-velocity[1]])

    # 整理(2026-08-25): 右半分と左半分で W_r / W_l が違うだけの同じブロックが
    #   丸ごと2回書かれていたので、幅の選択だけを分岐にまとめた。計算内容は変えていない。
    # 整理(2026-08-25): 法線の式は get_normal_vector に一元化した。
    #   向きが内向きに変わったが、上記のとおり反射結果はビット単位で不変。
    n = get_normal_vector(intersection ,W_r ,W_l ,H)
    n_norm = norm2(n)

    n_hat = n / n_norm

    reflected = velocity - 2 * np.dot(velocity,n_hat) * n_hat

    # 反射で |v| は理論上変わらないが、丸め誤差の蓄積を防ぐため毎回正規化し直す。
    return reflected / norm2(reflected) * speed

