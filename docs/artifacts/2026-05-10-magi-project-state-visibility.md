# MAGI: Project State Visibility

作成日: 2026-05-10

## 議題

Codex App でプロジェクトを進める際に、目標、進行ライン、依存、現在地が見えず、提案判断とレビュー判断の認知負荷が上がっている。これを解消するための状態可視化方式を検討する。

## AoT Decomposition

| Atom | 判断内容 | 依存 |
| --- | --- | --- |
| A1 | 何を可視化するべきか | なし |
| A2 | どの表示形式を中核にするか | A1 |
| A3 | Codex / Claude Code 系の運用とどう接続するか | A1, A2 |
| A4 | codex-of-LAM に入れる場合の最小導入単位 | A1, A2, A3 |

## Atom A1: 可視化対象

**MELCHIOR**: 目標、ライン、依存、承認 gate、検証結果を一枚で見られると、ユーザーと Codex の判断精度が上がる。とくに「次に何をやるか」だけではなく「なぜ今それか」が見える。

**BALTHASAR**: 全情報を一枚に集めると、すぐ肥大化して quick-load の軽さを壊す。更新されない可視化は、ないより危険な stale truth になる。

**CASPAR**: 可視化対象は「意思決定に必要な薄い状態」に限定する。詳細ログや議論本文は別ファイルへ逃がし、board は index として扱う。

## Atom A2: 表示形式

**MELCHIOR**: カンバン、依存 graph、状態遷移表、Mermaid でかなりの認知負荷を下げられる。とくに Agentic coding では、タスクが非同期化するため board 表現が相性よい。

**BALTHASAR**: ガントチャートは日付見積もりの精度がないと虚構になりやすい。状態遷移表だけだと「どの成果物がどこまで進んだか」が薄くなる。

**CASPAR**: 中核は `WORKBOARD.md` 型のカンバン + 依存表にする。ガントは採用せず、必要時だけ milestones / target dates の補助欄に留める。

## Atom A3: Agentic workflow との接続

**MELCHIOR**: Codex worktrees、subagents、skills、Claude Code の plan/review/context 管理と相性がよい。作業単位が board card になれば、Codex への依頼も精密になる。

**BALTHASAR**: 外部ツール依存を強めると、個人運用や複数 PC 同期の摩擦が増える。Codex App on Windows では Chronicle など一部機能が使えない、または安全上の注意が強い。

**CASPAR**: まず repo-native Markdown を SSOT にする。外部 UI は「ビュー」として後付けできる位置に置く。

## Atom A4: 最小導入単位

**MELCHIOR**: `PROJECT_DASHBOARD.md` を作り、quick-load 時に `SESSION_STATE.md` と一緒に読めば、すぐ効果が出る。

**BALTHASAR**: `SESSION_STATE.md` を太らせると過去の失敗を繰り返す。Git 管理外か管理対象かも分ける必要がある。

**CASPAR**: Git 管理対象の `WORKBOARD.md` または `docs/project/PROJECT_MAP.md` を作り、`SESSION_STATE.md` には現在カード ID と次アクションだけを置く。

## Reflection

致命的な見落とし: なし。懸念は stale 化なので、更新契約と quick-load 契約を同時に定義する必要がある。

## 統合結論

最適解は「ガントチャート単体」ではなく、薄い repo-native project board を中心にした三層構造。

1. `SESSION_STATE.md`: 次セッション復帰用の極小状態。
2. `WORKBOARD.md`: 目標、ライン、依存、gate、状態、検証の可視化 SSOT。
3. `docs/tasks/`, `docs/specs/`, `docs/artifacts/`: 詳細根拠と実行ログ。

次の導入候補は、`WORKBOARD.md` の仕様を PLANNING gate で定義し、pilot として codex-of-LAM 自身に適用すること。
