# quick-load harvest notes

## Purpose

- `quick-load` 移行に関して、Claude 由来の command、Codex workflow、internal docs、design/tasks、migration notes の差分を read-only で採掘する。
- 特に、Codex の `quick-load` workflow 本体へ残すべき最小手順と、internal docs 側だけに残すべき運用知識を切り分ける。
- あわせて、見出し名、読取順、責務境界の drift / mismatch を粗く記録する。

## Harvest Policy

- このメモは生の採掘ノートであり、最終判断書ではない。
- 判断ラベルは `adopt_candidate` / `decide_later` / `runtime_specific` / `reject_candidate` を使う。
- 対象は指定 source files を優先し、必要最小限で `AGENTS.md` の現行指示も参照した前提で整理する。
- `quick-load` workflow には「再開に必要な最小実行手順」だけを残し、長い背景説明、同期運用、将来拡張、補助ツール話は internal docs 側へ寄せる前提で読む。
- 既存 dirty changes は他者作業の可能性があるため、このメモでは観測だけ行い、巻き戻しや source 側編集案の断定はしない。

## Findings

### adopt_candidate

- `.codex/workflows/quick-load.md` の中心方針
  - quick-load を「project 再読込」ではなく「resume procedure」と定義している点は採用候補。
  - 出典: `.codex/workflows/quick-load.md`, `.claude/commands/quick-load.md`, `docs/internal/08_QUICK_LOAD_SAVE.md`

- 最小確認の 4 点セット
  - `.codex/current-phase.md` -> `git status --short --branch` -> `git log --oneline --decorate -3` -> `SESSION_STATE.md` の必要項目だけ確認、という流れは Codex quick-load workflow の本体として維持しやすい。
  - 出典: `.codex/workflows/quick-load.md`, `docs/internal/08_QUICK_LOAD_SAVE.md`, `AGENTS.md`

- `SESSION_STATE.md` を部分読みに限定する考え方
  - `保存時刻`、`現在フェーズ`、`復元サマリ`、`現在の未 commit 変更`、`次にやること`、`関連ファイル` のように、必要項目を絞る方針は quick-load 本体に入れる価値がある。
  - Claude 版の「関連ドキュメントを特定するが、まだ読まない」という節約思想とも整合する。
  - 出典: `.claude/commands/quick-load.md`, `.codex/workflows/quick-load.md`, `docs/internal/08_QUICK_LOAD_SAVE.md`

- 深掘り条件を明示して止まりどころを作ること
  - 「summary だけでは次の action に着手できない」「dirty changes の解釈が必要」「phase が食い違う」「ユーザーが deeper work を求めた」時だけ広げる、という条件分岐は Codex 向けに有効。
  - 出典: `.codex/workflows/quick-load.md`, `docs/internal/08_QUICK_LOAD_SAVE.md`

- 深掘り順の段階化
  - `AGENTS.md` -> `SESSION_STATE.md` 必要部 -> tasks 該当箇所 -> requirements/ADR/design 該当箇所 -> code/tests の順で広げる考え方は workflow に残しやすい。
  - これは design/tasks の「明示 workflow で移す」「review 可能にする」という方向にも合う。
  - 出典: `.codex/workflows/quick-load.md`, `docs/design/codex-lam-replacement-design.md`, `docs/tasks/codex-lam-replacement-tasks.md`

- 短い復帰サマリーを返して止まること
  - Claude 版の報告 template を Codex 版でも短い形式で踏襲するのは採用候補。
  - quick-load 完了後に先回りして大量読込しない、という終了条件も含めて workflow 本体向き。
  - 出典: `.claude/commands/quick-load.md`, `.codex/workflows/quick-load.md`

### runtime_specific

- Windows では `pwsh -NoProfile` を first shell checks の標準にすること
  - これは workflow に短く残してよいが、理由説明や shell noise / profile 問題の詳細は internal docs / AGENTS 側の責務。
  - 出典: `.codex/workflows/quick-load.md`, `docs/internal/08_QUICK_LOAD_SAVE.md`, `AGENTS.md`

- 日本語 Markdown 読取時に `Get-Content -Encoding UTF8 -LiteralPath ...` を使うこと
  - 実務上有用だが、repo 共通の Windows local note であり、quick-load 本体の中心ロジックではない。
  - internal docs / AGENTS に残すのが自然。
  - 出典: `docs/internal/08_QUICK_LOAD_SAVE.md`, `AGENTS.md`

- `SESSION_STATE.md` が Git 共有されず、別 PC では手動同期する運用
  - quick-load の前提条件としては重要だが、実行手順そのものではないため internal docs 側中心で保持するのが自然。
  - 出典: `docs/internal/08_QUICK_LOAD_SAVE.md`, `docs/design/codex-lam-replacement-design.md`, `docs/migration/claude-to-codex-migration-notes.md`

### decide_later

- `.codex/workflows/quick-load.md` をこの repo 固有 workflow として維持するか、`session-handoff` 的な共通 skill へさらに寄せるか
  - migration notes と design は repo 内 workflow として成立しているが、Claude 由来 command 群を repo 専用のまま残すか、より共通化するかはこの harvest だけでは未決。
  - 出典: `.codex/workflows/quick-load.md`, `docs/design/codex-lam-replacement-design.md`, `docs/migration/claude-to-codex-migration-notes.md`

- `SESSION_STATE.md` 必須項目の validation を CLI / pytest helper に上げる時期
  - internal docs と design/tasks は「将来候補」として揃っている。quick-load workflow へ今すぐ入れる話ではないが、どこで自動化するかは別判断が必要。
  - 出典: `docs/internal/08_QUICK_LOAD_SAVE.md`, `docs/design/codex-lam-replacement-design.md`, `docs/tasks/codex-lam-replacement-tasks.md`

- `git log -3` までを minimum confirmation に常設するか
  - 現行 workflow と internal docs は含めているが、Claude 版にはない。resume に十分効く一方、最小化をさらに詰めるなら optional 扱いへの見直し余地はある。
  - 出典: `.claude/commands/quick-load.md`, `.codex/workflows/quick-load.md`, `docs/internal/08_QUICK_LOAD_SAVE.md`

### reject_candidate

- quick-load workflow に quick-save の詳細 checklist や更新粒度原則まで持ち込むこと
  - これらは `docs/internal/08_QUICK_LOAD_SAVE.md` に置くべき運用知識であり、quick-load 実行手順へ混ぜると肥大化する。
  - 出典: `docs/internal/08_QUICK_LOAD_SAVE.md`

- quick-load workflow に共有同期ポリシー、`docs/daily/` の位置づけ、将来の自動検証計画を長く書くこと
  - いずれも背景方針としては必要だが、resume 手順の本体からは外したほうが良い。
  - 出典: `docs/internal/08_QUICK_LOAD_SAVE.md`, `docs/design/codex-lam-replacement-design.md`

- Claude の slash command frontmatter や「コンテキスト情報」前提をそのまま canonical contract にすること
  - migration notes でも frontmatter 直移植はしない方針。Claude 版の価値は command metadata ではなく、節約的な再開手順そのものにある。
  - 出典: `.claude/commands/quick-load.md`, `docs/migration/claude-to-codex-migration-notes.md`

### drift / mismatch observations

- `SESSION_STATE.md` の項目名にズレがある
  - `.codex/workflows/quick-load.md` は `現在フェーズ` を読むとしている一方、`docs/internal/08_QUICK_LOAD_SAVE.md` 4.1 では `フェーズ` と書かれている。
  - 同じ internal doc の checklist では `現在フェーズ` 表記なので、文書間で微妙に不整合。

- `.claude/commands/quick-load.md` と Codex 版で開始点が異なる
  - Claude 版は `SESSION_STATE.md` 読取から始まる。
  - Codex 版は phase / git status / git log を先に見てから state の必要項目へ入る。
  - これは drift というより Codex 向け拡張だが、migration note 上で「なぜ増えたか」を短く結び直す余地がある。

- internal docs は「背景方針」と「実行手順」がまだ混在気味
  - 章 4 は workflow の詳細版として読めるが、章 1-3, 5-7 は運用ポリシー色が強い。
  - `.codex/workflows/quick-load.md` が短い SSOT、`docs/internal/08_QUICK_LOAD_SAVE.md` が背景と周辺運用、という境界は概ね見えるが、まだ読み手によって重複感が出る。

- design/tasks は quick-load を「手動 workflow」「将来 validator は defer」として整合している
  - 大きな矛盾は見えない。
  - mismatch は主に workflow と internal docs の粒度差、および `SESSION_STATE.md` 項目名の細部に集中している。
