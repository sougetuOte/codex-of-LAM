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

## Roadmap

### Step 1: CLI pilot を安定化する

- `record` と `summary` の使い方を短い例で固定する
- 出力形式の微調整が必要なら、この段階で吸収する
- 日常 BUILDING で無理なく使えるかを確認する

### Step 2: retro での利用手順を決める

- `summary` をいつ見るかを決める
- FAIL -> PASS 候補を retro メモへどう転記するかを決める
- rule candidate 自動生成はまだ入れない

### Step 3: 保存ルールを固める

- log の保持期間を決める
- 1 session / 1 file にするか、追記運用を続けるかを決める
- `SESSION_STATE.md` とどう結びつけるかを決める

### Step 4: pytest helper の要否を再判断する

- CLI 運用だけで十分かを確認する
- 入力漏れや記録漏れが多いなら pytest helper を検討する
- helper を足しても Codex-native の明示性を壊さない形に限定する

## 非スコープ

- Claude hook の直移植
- Green State の自動判定連携
- rule candidate の自動生成
- 常駐プロセス化

## 次の一手

1. 実行例を 1 つ決める
2. `summary` を retro 前チェックとして 1 回試す
3. その結果を見て Step 2 の運用文書を作る
