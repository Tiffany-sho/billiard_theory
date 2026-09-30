/*
 * simulation.html の数値核をブラウザ無しで検算する
 *
 *   実行: node tools/check_html.js
 *   終了コード: 0 = 全形状一致 / 1 = 不一致あり
 *
 * なぜ必要か:
 *   simulation.html には「検算」ボタンがあるが、それを押すには人がブラウザを
 *   開く必要がある。数値が合っているかは機械的に確かめたいので、
 *   同じ script を Node の vm で読み込んで同じ selfTest() を回す。
 *   HTML から抜き出して実行するので、コードを二重管理しない。
 *
 * 出力は ASCII のみ（コンソールが cp932 のため、非ASCII を print しない）。
 */

"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.dirname(__dirname);
const HTML = path.join(ROOT, "simulation.html");

function extractScript(html, id) {
  // <script id="..."> ... </script> の中身を取り出す。
  const re = new RegExp(
    '<script id="' + id + '">([\\s\\S]*?)<\\/script>');
  const m = html.match(re);
  if (!m) throw new Error('script id="' + id + '" not found in simulation.html');
  return m[1];
}

function fmt(x) {
  if (x === 0) return "0";
  return x.toExponential(2);
}

function main() {
  if (!fs.existsSync(HTML)) {
    console.log("simulation.html not found at " + HTML);
    return 1;
  }

  const html = fs.readFileSync(HTML, "utf8");
  const context = {};
  vm.createContext(context);

  // 数値核と参照値を、HTML に書いてあるのと同じ順序で実行する。
  for (const id of ["billiard-core", "billiard-ref"]) {
    const code = extractScript(html, id);
    try {
      vm.runInContext(code, context, { filename: "simulation.html#" + id });
    } catch (e) {
      console.log("FAILED to evaluate " + id + ": " + e.message);
      return 1;
    }
  }

  // 画面まわりは DOM が要るのでここでは実行できないが、構文だけは見ておく。
  // 括弧の閉じ忘れのような事故を、ブラウザを開かずに捕まえられる。
  try {
    new Function(extractScript(html, "billiard-ui"));
    console.log("billiard-ui: syntax ok (not executed -- needs a DOM)");
  } catch (e) {
    console.log("billiard-ui: SYNTAX ERROR -- " + e.message);
    return 1;
  }

  const Billiard = context.Billiard;
  const REFERENCE = context.REFERENCE;

  if (!Billiard) {
    console.log("Billiard is not defined -- check the billiard-core script");
    return 1;
  }
  if (!REFERENCE) {
    console.log("REFERENCE is null -- run: python tools/dump_section.py");
    return 1;
  }

  console.log("=".repeat(72));
  console.log("simulation.html numeric core vs python reference");
  console.log("=".repeat(72));

  const results = Billiard.selfTest(REFERENCE);
  let failures = 0;

  console.log("         " + "shape".padEnd(9) + "    n  " +
    "d_pos".padEnd(9) + " " + "d_vel".padEnd(9) + " " +
    "d_coord".padEnd(9) + " " + "d_sin");

  for (const r of results) {
    if (r.note) {
      console.log("  [FAIL] " + r.id.padEnd(9) + " " + r.note);
      failures++;
      continue;
    }
    const tag = r.ok ? "[PASS]" : "[FAIL]";
    if (!r.ok) failures++;
    console.log("  " + tag + " " + r.id.padEnd(9) +
      String(r.n).padStart(5) + "  " +
      fmt(r.dPos).padEnd(9) + " " +
      fmt(r.dVel).padEnd(9) + " " +
      fmt(r.dCoord).padEnd(9) + " " +
      fmt(r.dSin));
  }

  // --- 幾何の自己検査 -------------------------------------------------
  // pointFromParam(境界パラメータ -> 境界上の点) は JS 側で新規に書いたので
  // Python に照合先が無い。代わりに次を確かめる。
  //   residual   : 生成した点が本当に境界の方程式を満たすか
  //   roundTrip  : 弧長軸の形状なら coord() で元のパラメータに戻るか
  //   outward    : 撒いた初期条件が領域の内側を向いているか（内向き法線の確認）
  if (typeof Billiard.selfTestGeometry === "function") {
    console.log("");
    console.log("=".repeat(72));
    console.log("boundary parametrisation (js only -- no python counterpart)");
    console.log("=".repeat(72));
    console.log("         " + "shape".padEnd(9) +
      "residual  round_trip  outward");

    for (const g of Billiard.selfTestGeometry()) {
      if (!g.ok) failures++;
      console.log("  " + (g.ok ? "[PASS] " : "[FAIL] ") + g.id.padEnd(9) +
        fmt(g.residual).padEnd(10) +
        (g.roundTrip == null ? "-".padEnd(12) : fmt(g.roundTrip).padEnd(12)) +
        String(g.outward));
    }
  }

  console.log("=".repeat(72));
  if (failures) {
    console.log("FAILED for " + failures + " shape(s)  (tolerance " +
      Billiard.TOLERANCE + ")");
    return 1;
  }
  console.log("all checks passed");
  return 0;
}

process.exit(main());
