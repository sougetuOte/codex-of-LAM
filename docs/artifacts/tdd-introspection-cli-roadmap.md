# TDD Introspection CLI Roadmap

Status: Draft  
Date: 2026-04-30

## 目的

Codex-native な `TDD introspection` を、hook 依存なしで小さく導入し、
retro 前に FAIL -> PASS の流れを見返せる状態にする。

## 現在地

- `record` サブコマンドを実装済み
- `summary` サブコマンドを実装済み
- 保存先は `docs/artifacts/tdd-introspection-records.log` に確定済み
- focused test は green
- `summary` の retro 前チェック手順を `docs/artifacts/tdd-introspection-summary-usage.md` に固定済み
- Windows ACL による focused pytest 判定不能例を `UNKNOWN` として記録し、転記方針を example に反映済み

## Roadmap

### Step 1: CLI pilot を安定化する

- `record` と `summary` の使い方を短い例で固定する
- 出力形式の微調整が必要なら、この段階で吸収する
- 日常 BUILDING で無理なく使えるかを確認する

### Step 2: retro での利用手順を決める

- [x] `summary` をいつ見るかを決める
- [x] FAIL -> PASS 候補を retro メモへどう転記するかを決める
- [x] `UNKNOWN` を環境要因と実装不明点に分けて扱う方針を決める
- [x] rule candidate 自動生成はまだ入れない

### Step 3: 保存ルールを固める

- log の保持期間を決める
- 1 session / 1 file にするか、追記運用を続けるかを決める
- `SESSION_STATE.md` とどう結びつけるかを決める

### Step 4: pytest helper の要否を再判断する

- CLI 運用だけで十分かを確認する
- 入力漏れや記録漏れが多いなら pytest helper を検討する
- helper を足しても Codex-native の明示性を壊さない形に限定する

再判断の目安:

- `record` の呼び忘れが頻発する
- Python/pytest の focused test が主経路になっている
- `summary` で欲しい情報の大半が pytest 実行時点で自動取得できる
- CLI の明示実行だけでは運用コストが高い

## 非スコープ

- Claude hook の直移植
- Green State の自動判定連携
- rule candidate の自動生成
- 常駐プロセス化

## 次の一手

1. Step 3 として log の保持期間を決める
2. 1 session / 1 file にするか、追記運用を続けるかを決める
3. `SESSION_STATE.md` とどう結びつけるかを決める
