# quick-save Harvest Notes

Status: Raw harvest
Date: 2026-05-09

## Purpose

- `C:\work6\codex-of-LAM` における Claude 由来の `quick-save` 運用を read-only で採掘し、Codex 用 quick-save workflow に残す要素、落とす要素、保留する要素を粗く分類する。
- 特に、Codex の quick-save が何を含むべきか、Claude-only な clutter をどこまで落とすべきか、`SESSION_STATE.md` を短く保つ既存方針と衝突していないかを確認する。
- この文書は決定記録ではなく、生の harvest note として扱う。

## Harvest Policy

- 対象は `.claude/commands/quick-save.md`、`docs/internal/08_QUICK_LOAD_SAVE.md`、`docs/design/codex-lam-replacement-design.md`、`docs/tasks/codex-lam-replacement-tasks.md`、`docs/migration/claude-to-codex-migration-notes.md`、補助として `AGENTS.md`。
- 読み取り専用で観察し、実装・文書の確定判断は行わない。
- 分類は `adopt_candidate` / `decide_later` / `runtime_specific` / `reject_candidate` を用いる。
- quick-save の主眼は「次の 5 分で迷わず再開できるか」とし、履歴保全や自動化の魅力よりも `SESSION_STATE.md` の薄さと review 可能性を優先して観察する。

## Findings

### adopt_candidate

- `.claude/commands/quick-save.md`
  - 既存 `SESSION_STATE.md` を土台にした差分更新を標準にする、という考え方は Codex 側でもそのまま有効。
  - 更新対象を `保存時刻`、`今回の重要な更新`、`現在の未 commit 変更`、`次にやること` に寄せる方針は、軽量 handoff に合う。

- `docs/internal/08_QUICK_LOAD_SAVE.md`
  - quick-save は `SESSION_STATE.md` ベースの手動 workflow とし、CLI 自動化を前提にしない方針は Codex LAM と整合している。
  - `git status --short --branch` と `git log --oneline --decorate -5` だけを quick-save 前の基本確認にするのは、context 節約と review 性の両立に向く。
  - `docs/daily/`、loop log、KPI を optional layer として外出しし、毎回の quick-save 必須作業にしない方針は採用候補。
  - quick-save の記録目標を「次回セッションが迷わず最初の 5 分を過ごせること」と定義している点は、Codex の resume workflow の中心原理として強い。
  - context compaction や state drift の兆候が出たら、長い継続より先に quick-save するという運用原理は採用候補。

- `docs/design/codex-lam-replacement-design.md`
  - `SESSION_STATE.md` を「手動 quick-load/save のための最短復元メモ」として扱う位置づけは、quick-save workflow の SSOT 側要件として採用候補。
  - 保存内容を phase、branch/remote、進行中作業、次手順、主要ファイル、環境注意点、直近検証結果に絞る設計意図は、quick-save の最小構成の基礎になる。

- `docs/tasks/codex-lam-replacement-tasks.md`
  - Wave 2B が `SESSION_STATE.md` の必須項目、quick-save 記録項目、手動同期運用、`docs/daily/` の非必須性を明示対象としているため、quick-save workflow は文書運用中心で十分という裏付けになる。

- `docs/migration/claude-to-codex-migration-notes.md`
  - `.claude/commands/quick-save.md` は slash command としてではなく、`SESSION_STATE.md` 中心の手動運用へ読み替える、という移行原則はそのまま採用候補。
  - `.claude/` が残っていても canonical source は `.codex/` と `docs/` と tracked files に置くべき、という整理は quick-save の責務境界を明確にする。

- `AGENTS.md`
  - `SESSION_STATE.md` は `.gitignore` の薄い local handoff であり、別 PC 継続時は手動同期、`docs/daily/` は quick-load 必須入力にしない、というローカル運用メモは quick-save の制約として採用候補。

### decide_later

- `docs/internal/08_QUICK_LOAD_SAVE.md`
  - 必須項目 checklist に `プロジェクト名`、`Remote`、`現在の作業パス`、`完了済み`、`重要な環境メモ`、`関連ファイル` まで含める現行定義はやや厚い。`SESSION_STATE.md` を「前回何をやったか / 次に何をするか」へ寄せる方針と比べ、どこまで本当に必須とするかは再判定が必要。
  - `直近の検証結果`、`実行した主要コマンド`、`sandbox / 権限 / OS 由来の既知問題`、`wave / task 名` を strong recommendation にしているが、毎回残すと handoff が肥大化しやすい。短い要約で十分か、別 artifact 参照へ逃がすかは保留。
  - quick-save に「どのファイルを先に読むべきか」「続行時に踏みやすい罠」まで毎回書くべきかは、価値は高いが定常運用では冗長化しうるため保留。

- `docs/design/codex-lam-replacement-design.md`
  - `branch/remote` や `主要ファイル` を常設フィールドにするか、必要時のみ残すかは設計上まだ絞れる余地がある。

- `.claude/commands/quick-save.md`
  - 「必要なら `直近の BUILDING 更新` または同等の直近作業欄」を残す考え方は有用だが、Codex では phase 共通の汎用欄にするか、BUILDING 専用欄を維持するかは要判断。

### runtime_specific

- `.claude/commands/quick-save.md`
  - loop log 保存手順そのものは Claude 由来の運用色が強く、Codex quick-save の中核ではない。
  - KPI 集計を quick-save 文脈に同居させる構成は、evaluation 用の legacy 文脈が強く、常用 quick-save からは切り離す前提で扱うのが自然。

- `docs/migration/claude-to-codex-migration-notes.md`
  - `.claude/commands/quick-save.md` を「運用メモとして残してよい」としている点は、あくまで legacy reference の扱いであり、Codex 側 workflow の canonical source にはしない前提が必要。

### reject_candidate

- `.claude/commands/quick-save.md`
  - 完了報告ブロック内の `claude -c`、`claude`、`/quick-load`、`/ship` 前提の再開案内は Codex では不要。
  - `.claude/logs/loop-*.txt` や `.claude/logs/permission.log` を quick-save の標準材料にする発想は落とすべき。

- `docs/migration/claude-to-codex-migration-notes.md`
  - slash command frontmatter、hook registration、subagent frontmatter、Stop / PostToolUse / PreCompact 前提の自動 loop は quick-save workflow に持ち込まない。

### SESSION_STATE.md policy mismatch

- `docs/internal/08_QUICK_LOAD_SAVE.md` の必須項目定義は、現行の「短いセッション復元メモ」「逃がせるものは逃がす」という repo 方針より厚めに見える。
- 特に `完了済み`、`重要な環境メモ`、`関連ファイル`、`実行した主要コマンド`、`wave / task 名` を常設・必須寄りで積むと、`SESSION_STATE.md` が履歴ログへ戻るリスクがある。
- 一方で、`今回の重要な更新`、`現在の未 commit 変更`、`次にやること`、必要最小限の検証結果だけを残す軽量原則は、`AGENTS.md` と Claude 由来 quick-save の軽量化ルールと整合している。
- したがって、Codex quick-save workflow の主線は「差分更新」「次の再開に必要な最小情報」「長い履歴は `docs/daily/` や他 artifact へ逃がす」で問題ないが、`08_QUICK_LOAD_SAVE.md` の checklist の厚さは後続判断ポイントとして残る。
