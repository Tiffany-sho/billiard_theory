"""ポアンカレ断面の参照値を Python 側から書き出す

simulation.html（JavaScript 版）が既存 Python と同じ数値を出しているかを
機械的に確かめるための参照値を作る。HTML 側はこの値を埋め込んで
「検算」ボタンで突き合わせる。

  実行: python tools/dump_section.py
  出力: tools/reference_<shape>.csv   人が見る用
        tools/reference.js            simulation.html に貼る用

なぜ必要か:
  このリポジトリには lint も型チェックも無く、tests/test_invariants.py は
  「物理的に必ず成り立つ不変量」しか見ていない。JS 移植が Python と
  同じ数値を出しているかは、値そのものを突き合わせないと分からない。

このツールが使う規約（docs/contracts.md が正）:
  [D1] 法線 n は全形状で領域の内側を向く。
  [D2] 断面に載せるのは衝突点 1..N のみ。初期位置は載せない。
  [D4] 楕円・卵型の横軸も弧長 s（右頂点が原点、反時計回り）。極角ではない。
  [D5] 角に当たった場合は来た道を戻る。

  sin(phi) は「入射速度」（反射前）と法線の外積で計算している。
  反射後の速度で計算しても数学的には同値だが
  （v_out x n = (v_in - 2(v_in.n)n) x n = v_in x n）、
  丸め誤差で最下位ビットが違うことがある。JS 側と揃えて入射側に固定する。
  したがって CSV の vx_in / vy_in は「その衝突に入ってきたときの速度」であり、
  class/*.py の velocities[i]（反射後）とは別物である。

出力は ASCII のみ（コンソールが cp932 のため、非ASCII を print しない）。
"""

import os
import sys

# setting.py が matplotlib を import するので、画面を開かないバックエンドにしておく。
os.environ.setdefault("MPLBACKEND", "Agg")

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "tools")

sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "class"))
sys.path.insert(0, os.path.join(ROOT, "func", "squre"))

# 重ね描きの色。setting.py が正で、ここは写しではなく import している。
from setting import basic_colors

# class/ 側（現行実装）。matplotlib を引き込まないよう *_func だけを import する。
import stadium_func as SF
import sinai_func as NF
import egg_func as EF

# 矩形はまだクラス化されていないので func/squre/ が唯一の実装。
from find_intersection_reversion import find_intersection_reversion as rect_intersect
from find_reflect_direction import find_reflect_direction as rect_reflect
from get_normal_vector import get_normal_vector as rect_normal
from get_arc_length import get_arc_length as rect_arc

V0 = np.array([0.02, 0.05]) / np.sqrt(29)   # main/stadium/poincare.py と同じ初速度
N_DEFAULT = 35                              # main/stadium/poincare.py と同じ衝突回数


def no_corner(q):
    """角を持たない形状（スタジアム・楕円・卵型）用。"""
    return False


def box_corner(q, W, H, tol=1e-12):
    """矩形・シナイの外壁の4隅に当たったか。

    Python 側の分岐は == の厳密比較だが、ここでは「参照値として脆いか」を
    見たいので、ぎりぎり外した点も角として扱う（tol 付き）。
    """
    return abs(abs(q[0]) - W / 2) < tol and abs(abs(q[1]) - H / 2) < tol


# ---------------------------------------------------------------- 形状の定義
# それぞれ intersect / reflect / normal / coord を同じ形にそろえて渡す。
# normal は矩形だけ速度を使う（角の場合分けがあるため）ので、
# 全形状 normal(q, v) のシグネチャで受ける。

def stadium_case():
    W, H = 5.0, 5.0
    return dict(
        name="stadium", params=dict(W=W, H=H),
        p0=np.array([0.5, 0.0]), v0=V0.copy(), n=N_DEFAULT,
        intersect=lambda p, v: SF.find_intersection_reversion(p, v, W, H),
        reflect=lambda q, v: SF.find_reflect_direction(q, v, W),
        normal=lambda q, v: SF.get_normal_vector(q, W, H),
        coord=lambda q: SF.get_arc_length(q, W, H),
        corner=no_corner,
        coord_range=(-(W + H * np.pi / 2), W + H * np.pi / 2))


def sinai_case():
    W, H, D = 5.0, 5.0, 2.0
    # 初期位置は「外壁の内側 かつ 障害物の外側」でなければならない。
    # |(1.3, 0.7)| = 1.477 > D/2 = 1.0 なので障害物の外にある。
    return dict(
        name="sinai", params=dict(W=W, H=H, D=D),
        p0=np.array([1.3, 0.7]), v0=V0.copy(), n=N_DEFAULT,
        intersect=lambda p, v: NF.find_intersection_reversion(p, v, W, H, D),
        reflect=lambda q, v: NF.find_reflect_direction(q, v, W, H, D),
        normal=lambda q, v: NF.get_n_vector_arc_length(q, W, H, D)[1],
        coord=lambda q: NF.get_n_vector_arc_length(q, W, H, D)[0],
        corner=lambda q: box_corner(q, W, H),
        coord_range=(0.0, 2 * (W + H + np.pi * D / 2)))


def rect_case():
    W, H = 5.0, 5.0
    # 矩形だけ v0 を変えている。共通の V0 は傾きが 0.05/0.02 = 5/2 という有理数で、
    # 5x5 の正方形では周期軌道になり 6 衝突ごとにきっちり角を突いてしまう
    # （角は参照値として脆い。run_case の corner 判定のコメントを参照）。
    # 無理数の傾きにすれば角には乗らない。
    return dict(
        name="rect", params=dict(W=W, H=H),
        p0=np.array([0.5, 0.0]),
        v0=np.array([1.0, np.sqrt(2)]) / np.sqrt(3.0), n=N_DEFAULT,
        intersect=lambda p, v: rect_intersect(p, v, W, H),
        reflect=lambda q, v: rect_reflect(q, v, W, H),
        normal=lambda q, v: rect_normal(q, v, W, H),
        coord=lambda q: rect_arc(q, W, H),
        corner=lambda q: box_corner(q, W, H),
        coord_range=(-(W + H), W + H))


def egg_case():
    W_r, W_l, H = 6.0, 3.0, 4.0
    return dict(
        name="egg", params=dict(W_r=W_r, W_l=W_l, H=H),
        p0=np.array([0.3, 0.1]), v0=V0.copy(), n=N_DEFAULT,
        intersect=lambda p, v: EF.find_intersection_func(p, v, W_r, W_l, H),
        reflect=lambda q, v: EF.find_reflect_direction(q, v, W_r, W_l, H),
        normal=lambda q, v: EF.get_normal_vector(q, W_r, W_l, H),
        coord=lambda q: EF.get_arc_length(q, W_r, W_l, H),
        corner=no_corner,
        coord_range=(-EF.egg_arc_range(W_r, W_l, H)[0],
                     EF.egg_arc_range(W_r, W_l, H)[0]))


def ellipse_case():
    # 楕円は卵型カーネルに W_r = W_l = W を渡したものと厳密に同じ。
    # func/ellipse/ の Newton 法版は使わない（simulation.html も卵型カーネルに寄せる）。
    W, H = 6.0, 4.0
    W_r = W_l = W
    return dict(
        name="ellipse", params=dict(W=W, H=H),
        p0=np.array([0.3, 0.1]), v0=V0.copy(), n=N_DEFAULT,
        intersect=lambda p, v: EF.find_intersection_func(p, v, W_r, W_l, H),
        reflect=lambda q, v: EF.find_reflect_direction(q, v, W_r, W_l, H),
        normal=lambda q, v: EF.get_normal_vector(q, W_r, W_l, H),
        coord=lambda q: EF.get_arc_length(q, W_r, W_l, H),
        corner=no_corner,
        coord_range=(-EF.egg_arc_range(W_r, W_l, H)[0],
                     EF.egg_arc_range(W_r, W_l, H)[0]))


CASES = [stadium_case, sinai_case, rect_case, egg_case, ellipse_case]


# ---------------------------------------------------------------- 計算
def run_case(case):
    """衝突 1..N を回して (rows, corners) を返す。

    rows    : [i, x, y, vx_in, vy_in, coord, sin]
    corners : 角に当たった衝突番号のリスト（D5 の逆行が起きた回）
    """
    p = case["p0"].astype(float).copy()
    v = case["v0"].astype(float).copy()
    rows = []
    corners = []

    for i in range(1, case["n"] + 1):
        q = case["intersect"](p, v)
        if q is None or not np.all(np.isfinite(q)):
            # Python 側は None や inf をそのまま返す経路がある。
            # 黙って進めると以降が NaN で埋まるので、ここで止めて報告する。
            raise RuntimeError(
                "%s: no intersection at collision %d (p=%r v=%r)"
                % (case["name"], i, p.tolist(), v.tolist()))

        n = np.asarray(case["normal"](q, v), dtype=float)
        n_hat = n / np.linalg.norm(n)
        v_hat = v / np.linalg.norm(v)
        sin_phi = float(v_hat[0] * n_hat[1] - v_hat[1] * n_hat[0])
        coord = float(case["coord"](q))

        rows.append([i, float(q[0]), float(q[1]),
                     float(v[0]), float(v[1]), coord, sin_phi])

        # 角に当たっていないかを幾何で見る。角は「2辺の法線が同時に効く」
        # measure-zero の場合で、1 ULP のずれで角判定から壁判定へ転ぶ。
        # 参照値に混ざると、JS 側の丸めがわずかに違うだけで以降の軌道が丸ごと変わる。
        #
        # 注意: 「反射後の速度が -v になったか」で判定してはいけない。
        #   それは垂直入射（滑らかな壁に真っ直ぐ当たる）でも起きるが、
        #   垂直入射は一意に定まるので参照値として何の問題もない。
        #   実際その判定にしたところ、角を持たないスタジアムが引っかかった。
        if case["corner"](q):
            corners.append(i)

        v = np.asarray(case["reflect"](q, v), dtype=float)
        p = np.asarray(q, dtype=float).copy()

    return rows, corners


def sanity(case, rows):
    """書き出す前の最低限の確認。ASCII で1行返す。"""
    lo, hi = case["coord_range"]
    max_sin = max(abs(r[6]) for r in rows)
    min_c = min(r[5] for r in rows)
    max_c = max(r[5] for r in rows)
    ok = (max_sin <= 1.0 + 1e-12) and (lo - 1e-9 <= min_c) and (max_c <= hi + 1e-9)
    return ok, ("|sin| max=%.6f  coord in [%.6f, %.6f] (allowed [%.6f, %.6f])"
                % (max_sin, min_c, max_c, lo, hi))


# ---------------------------------------------------------------- 出力
def write_csv(case, rows):
    path = os.path.join(OUT_DIR, "reference_%s.csv" % case["name"])
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("# generated by tools/dump_section.py -- do not edit by hand\n")
        f.write("# shape=%s params=%s\n" % (case["name"], case["params"]))
        f.write("# p0=%r v0=%r N=%d\n"
                % (case["p0"].tolist(), case["v0"].tolist(), case["n"]))
        f.write("# vx_in/vy_in = velocity ENTERING the collision (before reflection)\n")
        f.write("i,x,y,vx_in,vy_in,coord,sin\n")
        for r in rows:
            f.write("%d,%s\n" % (r[0], ",".join(repr(c) for c in r[1:])))
    return path


def build_js(all_rows):
    """simulation.html に埋め込む JS リテラルを組み立てて返す。

    repr() は float の最短往復表現を返すので、貼り付けても値は劣化しない
    （%.17g のような固定桁と違い、余計な桁も付かない）。
    """
    out = []
    out.append("// generated by tools/dump_section.py -- do not edit by hand")
    out.append("// rows: [i, x, y, vx_in, vy_in, coord, sin]")
    out.append("// vx_in/vy_in = velocity ENTERING the collision (before reflection)")
    out.append("var REFERENCE = {")
    for case, rows in all_rows:
        out.append('  "%s": {' % case["name"])
        out.append('    params: {%s},' % ", ".join(
            "%s: %s" % (k, repr(float(v))) for k, v in case["params"].items()))
        out.append('    p0: [%s], v0: [%s], N: %d,' % (
            ", ".join(repr(float(x)) for x in case["p0"]),
            ", ".join(repr(float(x)) for x in case["v0"]),
            case["n"]))
        out.append('    rows: [')
        for r in rows:
            out.append("      [%d, %s],"
                       % (r[0], ", ".join(repr(c) for c in r[1:])))
        out.append('    ],')
        out.append('  },')
    out.append("};")
    out.append("")
    out.append("// 重ね描きの色。setting.py: basic_colors がここの正。")
    out.append("var BASIC_COLORS = [")
    for k in range(0, len(basic_colors), 10):
        row = basic_colors[k:k + 10]
        out.append("  " + ", ".join('"%s"' % c for c in row) + ",")
    out.append("];")
    return "\n".join(out) + "\n"


def write_js(js_body):
    path = os.path.join(OUT_DIR, "reference.js")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(js_body)
    return path


def splice_into_html(js_body):
    """simulation.html のマーカーの間を、いま作った参照値で置き換える。

    手で貼り付ける運用にすると、参照値を作り直したのに貼り忘れる／
    貼り間違えるという事故が必ず起きる。1コマンドで完結させる。
    simulation.html がまだ無い場合は何もしない（Step 2 より前でも動くように）。
    """
    path = os.path.join(ROOT, "simulation.html")
    if not os.path.exists(path):
        return None

    begin = "// === REFERENCE BEGIN ==="
    end = "// === REFERENCE END ==="

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    i = text.find(begin)
    j = text.find(end)
    if i < 0 or j < 0 or j < i:
        raise RuntimeError("simulation.html: REFERENCE markers not found")

    head = text[:i]
    tail = text[j:]
    marker_line = begin + " tools/dump_section.py が自動生成する。手で編集しない。\n"

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(head + marker_line + js_body + tail)

    return path


def main():
    print("=" * 72)
    print("dump poincare section reference values")
    print("=" * 72)

    all_rows = []
    failures = 0

    for make in CASES:
        case = make()
        try:
            rows, corners = run_case(case)
        except RuntimeError as exc:
            print("  [FAIL] %-9s %s" % (case["name"], exc))
            failures += 1
            continue

        if corners:
            # 角に当たる初期条件は参照値として使えない（上の run_case のコメント参照）。
            print("  [FAIL] %-9s hits a corner at collision %s -- pick another p0/v0"
                  % (case["name"], corners))
            failures += 1
            continue

        ok, detail = sanity(case, rows)
        print("  [%s] %-9s %d rows  %s"
              % ("PASS" if ok else "FAIL", case["name"], len(rows), detail))
        if not ok:
            failures += 1
            continue

        write_csv(case, rows)
        all_rows.append((case, rows))

    if all_rows:
        js_body = build_js(all_rows)
        js = write_js(js_body)
        html = splice_into_html(js_body)
        print("")
        print("wrote %d csv file(s) and %s"
              % (len(all_rows), os.path.relpath(js, ROOT).replace("\\", "/")))
        if html:
            print("spliced reference into %s"
                  % os.path.relpath(html, ROOT).replace("\\", "/"))
        else:
            print("simulation.html not found -- skipped splicing")

    print("=" * 72)
    if failures:
        print("FAILED for %d shape(s)" % failures)
        return 1
    print("all shapes dumped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
