# 古典ビリヤード問題シミュレーション

ビリヤードの形状による粒子の振る舞いをシミュレーションし、ポアンカレ断面や軌道を可視化するプロジェクトです。

## 概要

**動力学的ビリヤード**とは、粒子が境界で鏡面反射しながら運動する力学系です。境界の形状によってカオス性の有無が決まり、積分可能系からエルゴード系まで様々な振る舞いを示します。

このプロジェクトでは以下の5種類のビリヤードを実装しています。

| 形状 | カオス性 | 特徴 |
|------|----------|------|
| 楕円 | なし（積分可能） | 焦点を通る軌道が保存される |
| 矩形（Rectangle） | なし（積分可能） | 速度成分が保存される |
| スタジアム（Bunimovich Stadium） | あり（エルゴード） | 矩形の両端を半円で置き換えた形状 |
| シナイ（Sinai Billiard） | あり（エルゴード） | 矩形の中心に円形障害物 |
| 卵型 | あり | 左右で長半径の違う半楕円を貼り合わせた形状。x = 0 の曲率不連続がカオス性の源 |

`simulation.html` の「エントロピー」タブで測ると、この違いが数値に出ます（分割数 50・衝突 20000）。

| 形状 | シャノンエントロピー S | 使われた格子 |
|---|---|---|
| 円（W = 0） | 5.644 | 50 / 2500 |
| 楕円 | 6.367 | 92 / 2500 |
| 矩形 | 6.690 | 108 / 2500 |
| 卵型 | 11.135 | 2492 / 2500 |
| スタジアム | 11.192 | 2498 / 2500 |
| シナイ | 11.197 | 2496 / 2500 |

上限は `log2(50²) = 11.288`。円がちょうど 50 格子・`S = log2(50)` になるのは、断面が $\sin\phi$ 一定の水平線1本に乗り、格子の1行だけが埋まるためです。

## ポアンカレ断面

境界への衝突点を弧長座標 $s$ と反射角の正弦 $\sin\phi$ の組 $(s, \sin\phi)$ でプロットしたものです。

- **積分可能系**（楕円・矩形）: 軌道は曲線（不変トーラス）上に乗る
- **カオス系**（スタジアム・シナイ）: 軌道が位相空間を一様に埋め尽くす

### 円ビリヤード（W = 0, H = 2）— 積分可能

| ポアンカレ断面 | 軌道 |
|:-:|:-:|
| ![circle_poincare](images/circle_poincare.png) | ![circle_ordit](images/circle_ordit.png) |

$\sin\phi$ が一定の直線上に乗り、軌道が周期的であることがわかります。

### スタジアムビリヤード（W = 2, H = 2）— エルゴード

| ポアンカレ断面 | 軌道 |
|:-:|:-:|
| ![stadium_poincare](images/stadium_poincare.png) | ![stadium_ordit](images/stadium_ordit.png) |

点が位相空間全体に散らばり、カオス的な軌道になっていることがわかります。

## ディレクトリ構成

```
billiard_theory/
├── setting.py              # 描画設定・グラフ初期化
├── ellipse/
│   ├── ellipse_liner_system.py      # 楕円ビリヤードの軌道表示
│   └── ellipse_poincare_map.py      # 楕円ビリヤードのポアンカレ断面
├── squre/
│   ├── squre_liner_system.py        # 矩形ビリヤードの軌道表示
│   ├── squre_poincare_map.py        # 矩形ビリヤードのポアンカレ断面
│   ├── squre_particle_system.py     # 多粒子シミュレーション
│   └── squre_compare_system.py      # 比較シミュレーション
├── stadium/
│   ├── stadium_poincare_map_arc.py  # スタジアムのポアンカレ断面（弧長座標）
│   └── graph_data/                  # 生成した画像の保存先
│       ├── poincare_depend_w_h_arc/
│       └── poincare_depend_w_h_polar/
├── sinai/
│   ├── sinai_liner_system.py        # シナイビリヤードの軌道表示
│   └── sinai_compare_system.py      # 比較シミュレーション
└── func/                            # 各形状の計算モジュール
    ├── stadium/
    │   ├── find_intersection_reversion.py  # 衝突点計算
    │   ├── find_reflect_direction.py       # 反射方向計算
    │   ├── get_normal_vector.py            # 法線ベクトル計算
    │   ├── get_arc_length.py               # 弧長計算
    │   └── get_jacobian.py                 # ヤコビアン計算
    ├── squre/
    ├── sinai/
    ├── ellipse/
    └── calculate/
        ├── newton_method.py         # ニュートン法（交点の数値計算）
        └── vertical_vector.py       # 法線ベクトル計算
```

## 実行方法

### ブラウザで対話的に触る（パラメータ探索用）

リポジトリ直下の **`simulation.html`** をダブルクリックしてブラウザで開くだけです。インストールもビルドもネット接続も要りません。

5形状（矩形・楕円・スタジアム・シナイ・卵型）を切り替えながら、形状パラメータと初期条件をスライダーで動かすと、図が即座に描き直されます。画面は4つのタブに分かれています。

| タブ | 内容 | Python 側の対応 |
|---|---|---|
| 単一軌道 | 軌道図とポアンカレ断面。断面の点にカーソルを合わせると軌道図の対応する衝突が強調される | `main/(形状)/poincare.py` |
| 重ね描き | 境界を等分した位置に初期条件を撒き、色分けして断面に重ねる | `main/(形状)/poincare_mix.py` |
| 占有領域 | 断面を divide × divide の格子に分け、通過回数を濃淡で塗る | `paint_occupany_area` |
| エントロピー | 衝突回数を増やしながらシャノンエントロピーを計算し、log2(N) に対して打つ | `main/(形状)/shannon_entropy_mix.py` |

Python 側と同じ値を出しているかは、ページ上部の「検算」ボタン、またはコマンドで確認できます。

```bash
node tools/check_html.js         # 5形状の数値を Python の参照値と突き合わせる
python tests/test_invariants.py  # 物理不変量（速さ保存・境界上・定義域・法線の向き）
python tools/dump_section.py     # 参照値を作り直して simulation.html へ差し込む
```

計算ロジック（`class/*_func.py` や `func/squre/`）を触ったら、`dump_section.py` → `check_html.js` の順に走らせてください。

詳しい仕様は [`docs/requirements.md`](docs/requirements.md)、座標系の定義は [`docs/contracts.md`](docs/contracts.md) にあります。

### Python で図を生成する（論文用）

```bash
# スタジアムビリヤードのポアンカレ断面と軌道
python stadium/stadium_poincare_map_arc.py

# 矩形ビリヤードのポアンカレ断面と軌道
python squre/squre_poincare_map.py

# 楕円ビリヤードのポアンカレ断面
python ellipse/ellipse_poincare_map.py

# シナイビリヤードの軌道
python sinai/sinai_liner_system.py
```

### パラメータ設定

各スクリプトの冒頭にあるパラメータを変更することで動作を調整できます。

**スタジアムビリヤード** （`stadium/stadium_poincare_map_arc.py`）:
```python
wall_width  = 2.0   # 矩形部分の幅 W（0.0 で円になる）
wall_height = 2.0   # 高さ H（半円の直径 = H）
position_1  = np.array([0.0, 0.5])   # 初期位置
velocity_1  = np.array([-0.05, 0.15])  # 初速度
```

`W = 0` のとき完全な円（積分可能）、`W > 0` で Bunimovich スタジアム（エルゴード）になります。

## 依存ライブラリ

- Python 3.x
- NumPy
- Matplotlib

```bash
pip install numpy matplotlib
```

## 座標系と物理量

- **弧長座標 $s$**: 境界を一周したときの弧長で衝突点を表す
- **反射角の正弦 $\sin\phi$**: 境界法線と入射方向のなす角の正弦（$-1 \leq \sin\phi \leq 1$）
- **境界分離線（赤点線）**: ポアンカレ断面上で矩形部分と半円部分の境界を示す

## 参考

- L. A. Bunimovich, "On the ergodic properties of nowhere dispersing billiards", Commun. Math. Phys. (1979)
- Ya. G. Sinai, "Dynamical systems with elastic reflections", Russian Math. Surveys (1970)
