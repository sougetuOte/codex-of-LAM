# TDD Introspection CLI Roadmap

Status: Draft  
Date: 2026-04-30

## 目的

Codex-native な `TDD introspection` を、hook 依存なしで小さく導入し、
retro 前に FAIL -> PASS の流れを見返せる状態にする。

## 現在地

- `record` サブコマンドを実装済み
- `summary` サブコマンドを実装済み
- 保存先は `docs/artifacts/tdd-introspection/sessions/<session-id>.log` の
  1 session / 1 file に確定済み
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

- [x] log の保持期間を決める
- [x] 1 session / 1 file にするか、追記運用を続けるかを決める
- [x] `SESSION_STATE.md` とどう結びつけるかを決める

決定:

- log は開発用の local record として無制限に保持してよい
- 保存単位は 1 session / 1 file とする
- 既定保存先は `docs/artifacts/tdd-introspection/sessions/<session-id>.log`
- Codex App の session / thread id が取れる場合はそれを file name に使う
- session id が取れない場合は UTC timestamp file へ fallback する
- `SESSION_STATE.md` には raw log を写さず、最新 summary の要点だけ残す
- 詳細が必要なときは、harvest / log 参照で session file を見に行く

### Step 4: pytest helper の要否を再判断する

- [x] CLI 運用だけで十分かを確認する
- [x] 入力漏れや記録漏れが多いなら pytest helper を検討する
- [x] helper を足しても Codex-native の明示性を壊さない形に限定する

決定:

- 現時点では pytest helper は採用しない
- TDD introspection は CLI の `record` / `summary` を継続する
- 理由は、Codex App on Windows で pytest temp directory の ACL failure が既知であり、
  記録支援を pytest runtime に寄せると、補助機構が検証環境の不安定さを抱えるため
- pytest helper は破棄ではなく deferred とし、再判断条件を満たした時点で再検討する

再判断の目安:

- `record` の呼び忘れが頻発する
- Python/pytest の focused test が主経路になっている
- `summary` で欲しい情報の大半が pytest 実行時点で自動取得できる
- CLI の明示実行だけでは運用コストが高い

### Step 5: Codex App Refresh Wave を準備する

- Codex App の新機能を棚卸しする
- template / bootstrap / skill-plugin distribution に取り込むものを分類する
- `.codex/` workflow、`docs/internal/`、user-level skill / plugin のどこへ反映するか決める
- 変更が大きい場合は、別 wave として requirements / design / tasks を作る

## 非スコープ

- Claude hook の直移植
- Green State の自動判定連携
- rule candidate の自動生成
- 常駐プロセス化

## 次の一手

1. Codex App Refresh Wave の対象範囲を決める
2. Codex App の新機能を、template / bootstrap / skill-plugin のどこへ反映するか棚卸しする
3. 必要なら `docs/internal/10_DISTRIBUTION_MODEL.md` を入口に planning artifact を作る
