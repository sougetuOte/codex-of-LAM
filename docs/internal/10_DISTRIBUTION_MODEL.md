# Codex LAM Distribution Model

このドキュメントは、`codex-of-LAM` を他プロジェクトへ展開するための配布モデルを定義する。

## 1. 目的

`codex-of-LAM` は、単体で動かす作業リポジトリであると同時に、
新しい開発プロジェクトへ Codex LAM の運用体系を持ち込むための
template / starter kit として扱う。

ここでいう template は、GitHub の "Use this template" に近い比喩である。
つまり、他プロジェクトがこのリポジトリを参照し続けるのではなく、
新規プロジェクト作成時または既存プロジェクト導入時に、
必要な初期構造、運用ルール、workflow、文書雛形を複製して使う。

## 2. 基本方針

- `codex-of-LAM` は Codex LAM の配布元として扱う。
- 新規プロジェクトには、まず template / starter kit として一式を持ち込む。
- 既存プロジェクトには、bootstrap / sync 手順で必要ファイルだけ導入できるようにする。
- quick-load / quick-save のような呼び出し操作は、template 本体とは別に
  skill / plugin 化を検討する。
- `.codex/workflows/*.md` は workflow guidance であり、それだけでは
  Codex App の slash command として自動登録されるとは限らない。

## 3. 配布レイヤー

### Layer 1: Template repository

新規プロジェクト向けの基本配布形。

含めるもの:

- `AGENTS.md`
- `.codex/constitution.md`
- `.codex/current-phase.md`
- `.codex/workflows/`
- `docs/internal/`
- `docs/specs/`, `docs/design/`, `docs/tasks/` の雛形
- 必要に応じた `docs/artifacts/` の例

含めないもの:

- active file としての `.codex/config.toml`
  - ただし、docs-only sample は `docs/internal/` 側に置く。

狙い:

- 新規 repo の初期状態から LAM の truth hierarchy と phase control を使えるようにする。
- project-facing documentation と workflow を、最初から review 可能な形にする。

### Layer 2: Bootstrap / sync script

既存プロジェクト向けの導入形。

想定する機能:

- 既存 repo に `AGENTS.md` と `.codex/` を追加する。
- `docs/internal/` の不足ファイルを追加する。
- 既存ファイルと衝突する場合は上書きせず、diff / report を出す。
- 導入後に、対象プロジェクト固有の requirements / design / tasks へ適応する。

狙い:

- template から始めなかったプロジェクトにも、後から Codex LAM を導入できるようにする。
- 既存プロジェクトの履歴や構成を壊さず、レビュー可能な migration として扱う。

### Layer 3: Project skills / user skills / plugin distribution

Codex App から呼び出したい操作向けの配布形。

候補:

- `quick-load`
- `quick-save`
- planning / building / auditing の開始補助
- session handoff
- LAM project status

配布単位:

- project skills: repo 内 `.agents/skills/` に置く。template と一緒に配布でき、
  その project 固有の workflow や文書構造を前提にできる。
- user skills: user-level `~/.codex/skills` または同等の user skill path に置く。
  複数 repo で使うが、project truth source ではない個人運用に向く。
- plugin: skill が安定し、複数環境へ広く配布したい段階で検討する。
  初期導入では skill より重い配布形として扱う。

狙い:

- 自然文で「quick-load しましょう」と依頼しなくても、Codex が対象 workflow を発見しやすくする。
- 複数プロジェクトで同じ運用手順を再利用しやすくする。

注意:

- skill / plugin は、template repository とは別レイヤーとして扱う。
  ただし `.agents/skills/` に置く project skill は template candidate として扱える。
- project skill は repo の `AGENTS.md`、`.codex/`、`docs/` を参照してよいが、
  truth hierarchy を置き換えない。
- user skill は個人の横断運用に便利だが、GitHub template の再現性には含めない。
- repository 内の `.codex/workflows/quick-load.md` は workflow の SSOT であり、
  slash command 登録そのものではない。
- Codex App の UI や plugin / command 仕様は変わり得るため、
  実装前に現在のローカル仕様または公式資料で確認する。

### Project config policy

`.codex/config.toml` は、現時点では active template file として配布しない。
まず docs-only sample として扱い、fresh repo / existing repo bootstrap で安全に使えることを
確認してから実ファイル化を検討する。

理由:

- approval policy、sandbox、web search、memories、multi-agent は、ユーザー環境、
  plan、project trust、作業対象によって適切な値が変わる。
- template に active config を含めると、新規 project の初回起動時から
  権限や search scope を変えてしまう可能性がある。
- Codex App / CLI / IDE extension の config contract は drift し得るため、
  実ファイル配布より先に review 可能な sample として運用した方が安全である。

docs-only sample に載せる候補:

| 項目 | 目的 | 初期判断 |
| --- | --- | --- |
| `approval_policy` | sandbox / shell / skill / MCP の承認境界を明示する | 候補に入れるが、値は project ごとに決める |
| `approvals_reviewer` | 自動承認レビューを使うかどうかを決める | 候補に入れるが、強制しない |
| `web_search` | cached / live / disabled の使い分けを明示する | docs-only。template default にはしない |
| `skills.config` | project skills の探索 path を明示する | `.agents/skills` pilot 後に再判断 |
| `features.memories` | memories を使うかどうかを明示する | advisory layer のため、template default にはしない |
| `features.multi_agent` | multi-agent を使うかどうかを明示する | gate 判断と worker 分離が安定してから検討 |
| Windows sandbox 周辺 | Windows project の shell / temp / ACL 問題を扱う | 現時点では `AGENTS.md` と quality standards に留める |

## 4. 採用順序

当面の推奨順序は以下とする。

1. Template repository として必要な配布内容を整理する。
2. 既存プロジェクト向け bootstrap / sync 手順を設計する。
3. quick-load / quick-save など、使用頻度が高いものから skill / plugin 化する。

理由:

- template 化は最も単純で、GitHub を中心に共有しやすい。
- bootstrap / sync は既存 repo への導入で必要になる。
- project skill 化は、Codex App 側の現在の機能と相性がよく、template と一緒に
  配布しやすい。
- user skill / plugin 化は便利だが、Codex App 側の発見・登録仕様に依存するため、
  project skill が安定してから進めた方が drift に強い。

## 5. 非目標

- `.codex/workflows/` をそのまま slash command とみなすこと。
- Claude Code の `.claude/commands/` を Codex App へ一律変換すること。
- 既存プロジェクトへの導入時に、ユーザーの既存 docs / tasks / rules を無確認で上書きすること。
- template repository と user-level skill / plugin の責務を混ぜること。
- project skill を `AGENTS.md` や requirements / design / tasks の代替 truth source にすること。

## 6. 次に決めること

- Codex App Refresh Wave の判断材料は
  `docs/artifacts/codex-app-refresh-wave-research.md` を参照する。
- Template repository として GitHub に載せる最小ファイル集合。
- 既存プロジェクト導入用の bootstrap / sync script を作るかどうか。
- `quick-load` を最初の project skill として切り出す具体設計。
- `quick-save` を project skill 化するか、session handoff / automation と分けるか。
- project-local `.agents/skills/` と user-level `~/.codex/skills` の同期方針。
- plugin 化に進むための安定条件。
- `.codex/config.toml` を active template file へ昇格する条件。
- README / QUICKSTART / CHEATSHEET / HTML slides を Codex App 前提の配布物として
  どう整えるか。

## 7. 初期 project skill

最初の project skill として `.agents/skills/quick-load/SKILL.md` を追加する。

この skill は `.codex/workflows/quick-load.md` を置き換えない。
役割は、Codex App / CLI / IDE extension が quick-load 操作を発見しやすくする
薄い入口である。

境界:

- skill body には最小実行手順だけを書く。
- 詳細な運用方針は `docs/internal/08_QUICK_LOAD_SAVE.md` に残す。
- workflow の SSOT は `.codex/workflows/quick-load.md` とする。
- `quick-save` は session writeback、Git、daily log、automation の責務境界が絡むため、
  `quick-load` skill の運用が安定するまで後回しにする。

## 8. Distribution collateral

template / starter kit として配布する場合、README や slides は単なる補助文書ではなく、
初回利用者の onboarding surface として扱う。

対象:

- `README.md`
- `README_en.md`
- `QUICKSTART.md`
- `QUICKSTART_en.md`
- `CHEATSHEET.md`
- `CHEATSHEET_en.md`
- `CHANGELOG.md`
- `docs/slides/*.html`

方針:

- 日本語を canonical、英語を追従版として整備する。
- Codex App 前提の使い方を明示し、Claude Code 前提の古い表現は残す場合も legacy として分離する。
- README と HTML slides では、画像付きの説明を積極的に使う。ただし R6 では文面と導線の更新を完了範囲とし、画像投入は配布仕上げ gate の未完了タスクとして扱う。
- 画像は装飾ではなく、template / starter kit の価値、quick-load、worktree、review / ship、
  fresh repo bootstrap の流れを短時間で理解させるために使う。
- slides は「読ませる文書」ではなく「見て把握できる visual onboarding」として再設計する。

## 9. Codex App workflow options

Codex App の機能は、LAM の必須 gate ではなく optional path として扱う。

反映先:

- `.codex/workflows/planning.md`
- `.codex/workflows/building.md`
- `.codex/workflows/auditing.md`
- `.codex/workflows/quick-save.md`

方針:

- Worktree mode は広い変更、並列実験、高リスク refresh wave に使う。
- review pane は diff inspection、inline comment、stage、commit、push、PR 準備に使う。
- in-app browser は HTML slides、README 画像、frontend、file-backed artifact の目視確認に使う。
- automations は template に同梱せず、手動 workflow が安定した後の任意 operation として扱う。

## 10. Fresh repo / bootstrap validation

template / starter kit として配布する前に、fresh repo と existing repo の両方で
最小検証を行う。

### Fresh repo validation

GitHub template 相当の新規 repo では、以下を確認する。

- `AGENTS.md` が Codex の project contract として読める。
- `.codex/current-phase.md` が存在し、初期 phase を示す。
- `.codex/workflows/` の planning / building / auditing / quick-load / quick-save が存在する。
- `.agents/skills/quick-load/SKILL.md` が存在し、skill validation に通る。
- `docs/internal/10_DISTRIBUTION_MODEL.md` が template / bootstrap / skill-plugin の境界を説明している。
- `docs/specs/`, `docs/design/`, `docs/tasks/` の初期雛形または作成先がある。
- active file としての `.codex/config.toml` が含まれていない。
- `SESSION_STATE.md` と `docs/daily/` が local state として Git 管理外にできる。
- quick-load の最小確認だけで、次に読むべきファイルと次の作業が判断できる。

### Existing repo bootstrap validation

既存 repo へ導入する場合は、以下を確認する。

- 既存の `README.md`, docs, tasks, rules を無確認で上書きしない。
- 追加対象、衝突対象、手動確認対象を diff / report として分ける。
- `AGENTS.md` が既にある場合は、追記候補を出し、即時上書きしない。
- `.codex/` が既にある場合は、workflow ごとに不足分だけ提案する。
- `.agents/skills/` が既にある場合は、採用済み project skill だけを追加候補にする。
- `.codex/config.toml` は active file として導入せず、docs-only sample を案内する。
- 導入後に対象 repo 固有の requirements / design / tasks へ適応する。

### Validation output

検証結果は、最低限以下を残す。

- 対象 repo 種別: fresh repo / existing repo
- 確認したファイル集合
- 追加予定ファイル
- 衝突または保留したファイル
- quick-load が成立したか
- 未解決リスク
