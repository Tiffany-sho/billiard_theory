# CLAUDE.md — billiard_theory

## プロジェクト概要
- 名前: billiard_theory（古典ビリヤード問題シミュレーション）
- 目的 / 誰のためのアプリか: 上田将生の研究用。矩形・楕円・スタジアム・シナイ・卵型の5種類のビリヤードについて、粒子の軌道とポアンカレ断面を可視化し、形状パラメータとカオス性の関係を調べる
- スタック:
  - **既存（論文用の図の生成）**: Python 3.14 / NumPy / Matplotlib。`python <スクリプト>` で直接実行する。パッケージマネージャなし、`pyproject.toml` なし
  - **新規（パラメータ探索用）**: 素の HTML + JavaScript + Canvas 2D。**ビルドツールも外部ライブラリも使わない**単一ファイル `simulation.html`
- リポジトリ構成の要点:
  - `class/` — **現行のコード**。`Stadium` / `Sinai` / `Egg` クラスと、それぞれの `*_func.py`。ここが実質の本体
  - `main/<形状>/` — 実行用スクリプト。パラメータを冒頭に直書きして `python main/stadium/poincare.py` のように叩く
  - `main/create_setting.py` — 多初期値の重ね描き用に、境界上の初期条件を生成する
  - `setting.py` — 全形状の matplotlib 描画設定（`*_set` が軌道図、`*_poincare_map*` が断面）と `basic_colors`（100色）
  - `func/<形状>/` — **クラス化前の旧実装**。`squre`（矩形）と `ellipse` はまだクラス化されておらず、ここにしか無い。`stadium` / `sinai` / `egg` は `class/*_func.py` と重複しているので、**編集するなら `class/` 側**
  - `simulation.html` — パラメータ探索用の HTML。`billiard-core`（数値核・DOM 非依存）/ `billiard-ref`（自動生成される参照値と色）/ `billiard-ui`（画面）の3つの script に分かれている。画面は4タブ（単一軌道 / 重ね描き / 占有領域 / エントロピー）
  - `tools/` — `dump_section.py`（参照値を作って HTML へ差し込む）と `check_html.js`（Node で数値照合）
  - `tests/test_invariants.py` — 物理不変量テスト
  - `stadium/graph_data/` — 生成済みの PNG。コードではない

## 検証コマンド（このプロジェクトで「done」を証明する手段）
> 完了報告の前に必ずこれらを実行する。実行できないものは「⚠️ 未検証」として明示する。

- Lint: **無し**（導入していない）
- 型チェック: **無し**
- ビルド: **無し**（Python は直接実行、HTML はビルド不要）
- **物理不変量テスト**: `python tests/test_invariants.py`
  速さ保存 / 全衝突点が境界上 / 断面座標が定義域内 / 法線の向きが境界全体で一貫、の4本を5形状で回す。終了コード 0 が通過。分岐網羅ではなく「形状に依らず必ず成り立つこと」だけを見る
- **JS と Python の数値照合**: `node tools/check_html.js`
  `simulation.html` から数値核を抜き出して Node で実行し、Python が書き出した参照値と突き合わせる。UI スクリプトの構文チェックも兼ねる。ブラウザは要らない。終了コード 0 が通過
- **参照値の再生成**: `python tools/dump_section.py`
  5形状ぶんの CSV と `tools/reference.js` を作り、`simulation.html` のマーカー間へ自動で差し込む。計算ロジックを触ったら必ず走らせる
- 起動 / 目視確認（Python）: `python main/stadium/poincare.py` — matplotlib のウィンドウが開く。`plt.show()` で止まるので**ヘッドレスでは完走しない**
- 起動 / 目視確認（HTML）: `simulation.html` をブラウザで開き、**開発者コンソールにエラーが1件も出ていないこと**と `docs/requirements.md` §6 の目視手順を確認する

⚠️ **上の3コマンドが通っても「見た目が正しい」ことは証明できない。** 数値と不変量しか見ていない。レイアウト・アニメーションの滑らかさ・文字の重なりは必ずブラウザで目視する。「コードを読んで正しそう」を done と呼ばない。

## Single Source of Truth（一元管理する場所）
> 同じ定数・テーブルを複数ファイルに複製しない。編集前にここを確認・grep する。

- **座標系の定義（弧長 s の原点と向き・法線 n の向き・sinφ の符号・パラメータ名の綴り）**: `./docs/contracts.md`。**ここが正**。実装と食い違ったら先にこの文書を直す
- **既定値（W, H, 初期位置, 初速度, 衝突回数）**: `./docs/contracts.md` §4。`main/` の各スクリプトに直書きされている値をコピーしないこと
- **描画の配色・線種**: `setting.py`（Python 側）。断面の破線は赤、点は `s=0.05`、重ね描きは `basic_colors`
- **HTML 側のデザイントークン（色）**: `simulation.html` の `:root`（`--boundary` / `--orbit` / `--dash` / `--dot` ほか）。描画コードは `getComputedStyle` で読む。**canvas の描画コードに生の色コードを直接書かない**。見た目は Python 側（黒い境界線・赤い破線）を踏襲
- **衝突判定・反射・弧長の計算ロジック**: Python は `class/*_func.py`（`stadium` / `sinai` / `egg`）と `func/squre/`（矩形はクラス化されていない）。JS は `simulation.html` の `billiard-core`。**両方を直さないとずれる。ずれたら `node tools/check_html.js` が落ちる**
- **2次元ベクトルの小道具**: `class/vector_func.py: norm2`（`np.linalg.norm` と 2 成分ではビット単位で等価）
- ⚠️ `func/stadium/`・`func/sinai/`・`func/egg/` は `class/` と**重複した旧実装**。`func/ellipse/`（Newton 法）も使っていない。編集するなら `class/` 側

## ドメイン用語集（曖昧な用語の定義と出典）
> 多義的な語は勝手に解釈せず、ここで定義を固定する。未定義の語が出たら AskUserQuestion。

- **弧長座標 s**: 境界を一周したときの弧長で衝突点を表す。⚠️ **原点と向きが形状ごとに違う**（スタジアム・矩形は上辺中央が原点で負値を含む／シナイは右上角が原点で 0 始まり・時計回り／楕円・卵型は右頂点が原点で反時計回り。楕円積分で出す）。定義は `docs/contracts.md` §2
- **sinφ**: 反射角の正弦。実装は `v̂ × n̂`（速度と法線の2次元外積）。**n は全5形状で領域の内側を向く**ので符号の意味は揃っている（決定 D1）。`docs/contracts.md` §1・§2
- **W / H / D / W_r / W_l**: すべて**直径・全幅**であって半径・半幅ではない。式ではつねに `W/2` として現れる
- **スタジアムの `H`**: 高さであると同時に**両端の半円の直径**。`W = 0` で半径 `H/2` の真円になる
- **bound_num（衝突回数）**: `positions` の長さは `bound_num + 1`（先頭が初期位置）。**断面に載せるのは衝突点 1..N だけ**で、初期位置は載せない（決定 D2）。`docs/contracts.md` §1
- **積分可能 / エルゴード**: 矩形・楕円は積分可能（断面上で軌道が曲線に乗る）、スタジアム・シナイはエルゴード（位相空間を一様に埋める）。卵型は左右の曲率不連続がカオス性の源

## 実装前に必ず読む参照資料
- `./docs/requirements.md` — **何を作るか（WHAT / WHY）**。Must / 非スコープ / 受け入れ基準 / 未決事項
- `./docs/contracts.md` — **データ契約**。弧長・法線・sinφ・パラメータ名・既定値はここが正
- `./README.md` — 4形状の物理的な意味と参考文献（Bunimovich 1979 / Sinai 1970）
- `class/stadium_func.py` / `class/sinai_func.py` / `class/egg_func.py` — 衝突判定・反射・弧長の実装。移植元
- `setting.py` — 図の見た目（軸範囲・破線の位置・配色）。JS 側の軸範囲と破線位置はここから写している
- `tests/test_invariants.py` / `tools/dump_section.py` — 規約が破れたときに落ちる仕掛け。規約を変えるならここも直す
- UIワイヤーフレーム: https://claude.ai/code/artifact/0eeb4444-13e4-4718-a41f-2ea8b46f8a42 （2026-08-25 時点。**実装の正ではない**）

## このプロジェクト特有の注意

- **`simulation.html` は自己完結の1ファイル**。CDN・外部フォント・fetch を使わない。ネットを切っても動くことが受け入れ基準20
- **`class/` と `func/` に同じ関数が重複している**。`stadium` / `sinai` / `egg` を直すときは `class/*_func.py` 側。`func/` 側は旧実装
- **浮動小数の比較は Python の書き方をそのまま写す。独自に境界へ丸めない。** 丸めると座標が 1e-16 ずれ、カオス系では 35 衝突で増幅されて数値照合が落ちる。実際そのまま写した結果、矩形・スタジアム・シナイは位置・速度がビット単位で一致している（`docs/contracts.md` §1）
- **交点が求まらない経路がある。** Python は `None` や `inf` をそのまま返す。JS は `null` を返して計算を止め、何回目で止まったかを画面に出す。**黙って NaN を先へ流さない**
- **法線は全5形状で内向き。片方だけ直さない。** Python と JS の両方に同じ規約がある。`tests/test_invariants.py` の検査 [4] が規約の破れを検出する
- **角（頂点にちょうど当たる）は逆行させる**（`v → −v`）。矩形・シナイとも同じ。`v0` の傾きが有理数だと周期軌道になって規則的に角を突くので、参照値や検証には無理数傾きを使う
- **`create_occupany_area()` には off-by-one が残っている**（初期位置を1個数えて N 回目を捨てる）。`poincare()` 側だけ直してあり、意図的に手を付けていない。S2・S3（占有領域・エントロピー）に着手するときにまとめて直す
- **canvas の寸法は `clientWidth` / `clientHeight` を使う。** `getBoundingClientRect()` は `box-sizing:border-box` の 1px ボーダーを含むので、それを `canvas.width` にすると描画面が縮小表示され、マウス座標と数 px ずれる（断面のホバーが隣の点を拾う形で出た）
- **`billiard-ui` は1つの IIFE で、後半のブロックほど後に初期化される。** `var` は巻き上げられるので、前半の関数から後半で定義した定数を参照すると `undefined` になる（`new Array(NaN)` で `RangeError` を出して UI 全体が起動しなくなった）。索引などは遅延生成にする
- **長い軌道で JS と Python の数値一致を期待しない。** カオス系なので数百衝突で 1 ULP から指数的に開く（スタジアムで実測 420 衝突目）。移植の正しさは 35 衝突の参照照合が担保する。エントロピーのような統計量は 1% 程度の差が出て当たり前
- **`billiard-ui` から核の内部関数は見えない。** `norm2` などは `billiard-core` の IIFE に閉じているので、UI 側では `Billiard.norm2` と書く。裸で呼ぶと `ReferenceError` で UI 全体が起動しなくなる
- **ブロックコメントの中にパスを書くときは `*` と `/` を並べない。** `main/*/foo.py` と書くとそこでコメントが閉じ、以降がコードとして解釈されて UI 全体が落ちる
- **`plt.show()` を含むスクリプトはヘッドレスで完走しない**。バックグラウンド実行して「終わった」と判断しないこと
- **コンソールは cp932**。Python から非ASCII文字（上付き文字・φ・✓・絵文字）を print しない。既存コードは `print(f"...sinφ:...")` を含んでおり、環境によっては落ちる。新しく print を足すときは ASCII に留めるか、ファイルへ書き出す
- **新規ファイルは UTF-8（BOMなし）**。ソースファイルに PowerShell の一括正規表現置換をかけない（UTF-8 が壊れる）

## 絶対に守ること
- 進捗の一覧表を CLAUDE.md に書かない（実装が進むほど古くなり、事実と逆のことを書く表になる）
- 決定を変えたら、変えた事実と理由を残す（古い記述を消すだけにしない）
- エラーを握り潰さない。「交点が見つからなかった」と「衝突が0回だった」を必ず区別する
- 「コードを読んだ」を「確認した」と書かない。図を描いて見るまでは未確認
