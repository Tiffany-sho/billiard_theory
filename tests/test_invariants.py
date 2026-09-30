"""ビリヤードの物理不変量テスト

このプロジェクトには lint / 型チェック / テストが無く、
「図を描いて目で見る」以外に done を証明する手段が無かった。
分岐を網羅するユニットテストではなく、形状に依らず必ず成り立つ
物理の不変量だけを4本チェックする。

  [1] 速さ保存        : 鏡面反射は |v| を変えない
  [2] 境界上にいる    : 全衝突点が境界の方程式を満たす（かつ領域内）
  [3] 断面座標の定義域: |sinφ| <= 1、弧長 s が宣言した範囲に入る
  [4] 法線の向き      : 出射速度と法線の内積の符号が境界全体で一貫している
                        （スタジアム/シナイは内向き法線なので dot > 0）

[4] は「スタジアムの円弧部だけ法線が外向きで、
断面の sinφ が接続点 s = ±W/2 で符号反転していた」バグを機械的に検出する。

  実行: python tests/test_invariants.py
  終了コード: 0 = 全通過 / 1 = 失敗あり

出力は ASCII のみ（コンソールが cp932 のため、非ASCII を print しない）。
"""

import os
import sys

os.environ.setdefault("MPLBACKEND", "Agg")  # plt.show() を持つモジュールを import するため

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "class"))
sys.path.insert(0, os.path.join(ROOT, "main"))

from stadium import Stadium
from sinai import Sinai
from egg import Egg
import stadium_func as SF
import sinai_func as NF
import egg_func as EF
from create_setting import stadium_create_setting, sinai_create_setting

TOL = 1e-9

_failures = []


def check(name, ok, detail=""):
    """1件の検査結果を記録して1行出力する。detail は ASCII のみ。"""
    status = "PASS" if ok else "FAIL"
    line = "  [%s] %-46s %s" % (status, name, detail)
    print(line)
    if not ok:
        _failures.append(name)
    return ok


# ---------------------------------------------------------------- 幾何ヘルパ
def stadium_residual(p, W, H):
    """スタジアム境界からの距離。0 なら境界上。"""
    if abs(p[0]) <= W / 2:
        return abs(abs(p[1]) - H / 2)
    center = np.array([np.sign(p[0]) * W / 2, 0.0])
    return abs(np.linalg.norm(p - center) - H / 2)


def sinai_residual(p, W, H, D):
    """シナイ境界（矩形の4辺 or 中央の円）からの距離。"""
    return min(abs(np.linalg.norm(p) - D / 2),
               abs(abs(p[0]) - W / 2),
               abs(abs(p[1]) - H / 2))


def egg_residual(p, W_r, W_l, H):
    """卵型（左右で半径の違う半楕円）の境界方程式の残差。"""
    a = W_r / 2 if p[0] > 0 else W_l / 2
    return abs((p[0] / a) ** 2 + (p[1] / (H / 2)) ** 2 - 1.0)


# ---------------------------------------------------------------- 共通の4検査
def run_invariants(label, positions, velocities, residual, normal_of,
                   arc_of, arc_range, expect_inward):
    """1本の軌道に対して不変量4本を回す。

    positions[0] は初期位置（衝突点ではない）なので、衝突点は 1..N。
    これは class/*.py の poincare() が使うインデックス範囲と一致させてある。
    """
    n_coll = len(positions) - 1
    idx = range(1, n_coll + 1)

    # [1] 速さ保存
    speeds = [float(np.linalg.norm(v)) for v in velocities]
    drift = max(speeds) - min(speeds)
    check("%s / [1] speed conserved" % label, drift < 1e-12,
          "drift=%.2e" % drift)

    # [2] 全衝突点が境界上
    res = [residual(positions[i]) for i in idx]
    check("%s / [2] all collisions on boundary" % label, max(res) < TOL,
          "max residual=%.2e over %d collisions" % (max(res), n_coll))

    # [3] 断面座標が定義域に入っている
    sins, arcs = [], []
    for i in idx:
        n = normal_of(positions[i])
        n_hat = n / np.linalg.norm(n)
        v_hat = velocities[i] / np.linalg.norm(velocities[i])
        sins.append(float(v_hat[0] * n_hat[1] - v_hat[1] * n_hat[0]))
        arcs.append(float(arc_of(positions[i])))
    lo, hi = arc_range
    check("%s / [3] |sin(phi)| <= 1 and s in range" % label,
          max(abs(s) for s in sins) <= 1.0 + 1e-12
          and lo - TOL <= min(arcs) and max(arcs) <= hi + TOL,
          "|sin| max=%.6f  s in [%.4f, %.4f] (allowed [%.4f, %.4f])"
          % (max(abs(s) for s in sins), min(arcs), max(arcs), lo, hi))

    # [4] 法線の向きが境界全体で一貫している
    #     内向き法線なら、反射「後」の速度は必ず領域内を向く => dot > 0。
    #     スタジアムの円弧部だけ法線が外向きになるバグは、直線部 dot>0 / 円弧部 dot<0 という
    #     ここが割れる形で現れていた。
    dots = []
    for i in idx:
        n = normal_of(positions[i])
        n_hat = n / np.linalg.norm(n)
        v_hat = velocities[i] / np.linalg.norm(velocities[i])
        dots.append(float(np.dot(v_hat, n_hat)))
    if expect_inward:
        ok = min(dots) > -TOL
        want = "inward (dot > 0)"
    else:
        ok = max(dots) < TOL
        want = "outward (dot < 0)"
    check("%s / [4] normal orientation consistent" % label, ok,
          "expect %s, got dot in [%+.4f, %+.4f]" % (want, min(dots), max(dots)))


# ---------------------------------------------------------------- 各形状
def test_stadium():
    W, H, N = 5.0, 5.0, 500
    print("STADIUM  W=%.1f H=%.1f  N=%d" % (W, H, N))
    half = W + H / 2 * np.pi          # class/stadium.py の range_arc / 2

    rng = np.random.RandomState(0)
    np.random.seed(0)
    cases = [(np.array([0.5, 0.0]), np.array([0.02, 0.05]) / np.sqrt(29)),
             (np.array([0.0, 0.0]), np.array([1.0, np.sqrt(2)]))]
    for k in (7, 23, 61, 88):         # 境界上の初期条件も混ぜる
        cases.append(stadium_create_setting(k, W, H, 2 * half / 100))

    for c, (p0, v0) in enumerate(cases):
        s = Stadium(p0.copy(), v0.copy(), W, H, N)
        run_invariants(
            "stadium#%d" % c, s.positions, s.velocities,
            residual=lambda p: stadium_residual(p, W, H),
            normal_of=lambda p: SF.get_normal_vector(p, W, H),
            arc_of=lambda p: SF.get_arc_length(p, W, H),
            arc_range=(-half, half),
            expect_inward=True)
    del rng


def test_sinai():
    W, H, D, N = 5.0, 5.0, 2.0, 500
    print("SINAI    W=%.1f H=%.1f D=%.1f  N=%d" % (W, H, D, N))
    perim = 2 * (W + H + np.pi * D / 2)   # class/sinai.py の range_arc

    np.random.seed(1)
    cases = [(np.array([0.5, 0.0]), np.array([0.02, 0.05]) / np.sqrt(29)),
             (np.array([1.5, 1.5]), np.array([-1.0, -0.3]))]
    for k in (5, 40, 77):
        cases.append(sinai_create_setting(k, W, H, D, perim / 100))

    for c, (p0, v0) in enumerate(cases):
        s = Sinai(p0.copy(), v0.copy(), W, H, D, N)
        run_invariants(
            "sinai#%d" % c, s.positions, s.velocities,
            residual=lambda p: sinai_residual(p, W, H, D),
            normal_of=lambda p: NF.get_n_vector_arc_length(p, W, H, D)[1],
            arc_of=lambda p: NF.get_n_vector_arc_length(p, W, H, D)[0],
            arc_range=(0.0, perim),
            expect_inward=True)


def test_egg():
    W_r, W_l, H, N = 6.0, 3.0, 4.0, 500
    print("EGG      W_r=%.1f W_l=%.1f H=%.1f  N=%d" % (W_r, W_l, H, N))
    # 卵型は弧長ではなく極角 arctan2(y, x) を断面の横軸に使っている
    # （弧長には楕円積分が要る）。定義域は [-pi, pi]。
    cases = [(np.array([0.3, 0.1]), np.array([0.02, 0.05]) / np.sqrt(29)),
             (np.array([-0.5, 0.4]), np.array([1.0, 0.37]))]

    for c, (p0, v0) in enumerate(cases):
        e = Egg(p0.copy(), v0.copy(), W_r, W_l, H, N)
        run_invariants(
            "egg#%d" % c, e.positions, e.velocities,
            residual=lambda p: egg_residual(p, W_r, W_l, H),
            normal_of=lambda p: EF.get_normal_vector(p, W_r, W_l, H),
            arc_of=lambda p: np.arctan2(p[1], p[0]),
            arc_range=(-np.pi, np.pi),
            expect_inward=True)


def test_index_range_is_collisions_only():
    """[B] のリグレッションテスト。

    positions[0] は初期位置であって衝突点ではない。
    内点から始めた場合、positions[0] は境界上に無いので断面に載せてはいけない。
    poincare() が range(1, bound_num + 1) を使っていることをここで固定する。
    """
    W, H, N = 5.0, 5.0, 50
    print("INDEX RANGE  (regression guard for the off-by-one fix)")
    s = Stadium(np.array([0.5, 0.0]), np.array([0.02, 0.05]) / np.sqrt(29),
                W, H, N)

    r0 = stadium_residual(s.positions[0], W, H)
    check("index / positions[0] is NOT on the boundary", r0 > 1e-3,
          "residual=%.4f (interior start point, must be excluded)" % r0)

    check("index / positions[1..N] are all collisions",
          max(stadium_residual(s.positions[i], W, H)
              for i in range(1, N + 1)) < TOL,
          "N=%d collisions available" % N)

    import inspect
    src = inspect.getsource(Stadium.poincare)
    check("index / poincare() iterates range(1, bound_num + 1)",
          "range(1, self.bound_num + 1)" in src,
          "guards against reverting to range(self.bound_num)")


def main():
    print("=" * 72)
    print("billiard invariant tests")
    print("=" * 72)
    for t in (test_stadium, test_sinai, test_egg,
              test_index_range_is_collisions_only):
        t()
        print("")
    print("=" * 72)
    if _failures:
        print("FAILED %d check(s):" % len(_failures))
        for f in _failures:
            print("  - %s" % f)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
