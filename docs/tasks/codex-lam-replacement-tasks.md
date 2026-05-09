# Codex LAM 置き換えタスク

Status: Accepted
Date: 2026-04-30

## Wave 1: Codex contract scaffold

- [x] Codex 置き換え contract のための最初の manifest test を追加する。
- [x] manifest validation 用の `codex_lam/manifest.py` を追加する。
- [x] Codex 入口として `AGENTS.md` を追加する。
- [x] `.codex/manifest.json` を追加する。
- [x] `.codex/workflows/planning.md` を追加する。
- [x] `.codex/workflows/building.md` を追加する。
- [x] `.codex/workflows/auditing.md` を追加する。
- [x] requirements、ADR、design、tasks を review 可能な形で追加する。
- [x] focused test を実行し、結果を記録する。

## Wave 1 Review Sync: 承認前の文書同期

- [x] requirements review の指摘を反映する。
- [x] requirements を日本語化し、承認ゲート、quick-load、legacy behavior 最大移設を明記する。
- [x] ADR を requirements の FR-6/FR-7 に同期する。
- [x] design を requirements の FR-6/FR-7 と FR-5 test matrix に同期する。
- [x] tasks を requirements、ADR、design に同期する。
- [x] requirements の最終軽量レビューを行う。
- [x] requirements の承認を得る。
- [x] 旧 `docs/specs/`、`docs/adr/`、`docs/design/` の軽量採掘メモを作成する。
- [x] ADR のレビューと承認を得る。
- [x] design のレビューと承認を得る。
- [x] tasks のレビューと承認を得る。

## Wave 2A: Manifest validation hardening

requirements FR-5 と design の TDD Strategy に合わせて、manifest validation を強化する。

- [x] `source_harness` が `.codex` ではない場合に失敗する test を追加する。
- [x] phase list の不足で失敗する test を追加する。
- [x] phase list の重複で失敗する test を追加する。
- [x] phase list の順序違いで失敗する test を追加する。
- [x] phase list の大文字小文字違いで失敗する test を追加する。
- [x] approval gate list の不足で失敗する test を追加する。
- [x] approval gate list の重複で失敗する test を追加する。
- [x] approval gate list の順序違いで失敗する test を追加する。
- [x] approval gate list の大文字小文字違いで失敗する test を追加する。
- [x] manifest が列挙する required document が存在しない場合に失敗する test を追加する。
- [x] required workflow が存在しない場合に失敗する test を追加する。
- [x] 上記の Red test を通すために `codex_lam/manifest.py` を更新する。
- [x] focused test を実行し、Windows ACL 問題が出た場合は権限外実行または手動 cleanup を記録する。

## Wave 2B: quick-load/save workflow

requirements FR-6 と design の `SESSION_STATE.md` 方針に合わせて、手動 quick-load/save を運用できる形にする。

- [x] `SESSION_STATE.md` の必須項目を checklist として明文化する。
- [x] quick-save 時に記録する項目を定義する。
- [x] quick-load 時に最初に読むファイルと確認コマンドを定義する。
- [x] `SESSION_STATE.md` は `.gitignore` 対象のまま、共有フォルダで手動同期する運用を明記する。
- [x] `docs/daily/` は長めの日次ログであり、quick-load の必須入力ではないことを明記する。
- [x] 必要になった時点で、`SESSION_STATE.md` の必須項目を検証する CLI または pytest helper を検討する。

## Wave 2C: Legacy behavior inventory and migration

requirements FR-7 と ADR/design の方針に合わせて、`.claude/` 配下の資産と旧 `docs/` 資産を棚卸しし、Codex で扱える形へ移す。

- [x] `.claude/commands/` の slash command を棚卸しする。
- [x] `.claude/hooks/` の hook script を棚卸しする。
- [x] `.claude/agents/` または subagent 定義を棚卸しする。
- [x] `.claude/settings.json` などの設定を棚卸しする。
- [x] `.claude/` 配下の rules、guides、checklists、運用メモを棚卸しする。
- [x] 旧 `docs/specs/`、`docs/adr/`、`docs/design/`、`docs/internal/` の Codex へ再利用できる資産を棚卸しする。
- [x] `docs/migration/codex-reusable-legacy-docs.md`、`docs/migration/legacy-harvest-notes.md`、`docs/migration/legacy-harvest-decision.md` を入口として、model routing、Green State、scalable review、TDD introspection、security/permission、upstream-first、development flow、multi-perspective decision、cross-module blame を分類する。
- [x] baseline 候補として分類済みの Green State、read/write 権限、upstream-first、spec/design/tasks/tests 同期を、Codex LAM のどの artifact へ反映するか決める。
- [x] 棚卸し結果を `docs/migration/claude-legacy-inventory.md` などの review 可能な文書へまとめる。
- [x] 各 legacy item を、Codex ハーネスへ移設、Codex-native workflow/CLI/pytest/review procedure として再実装、legacy 参考資料として維持、Claude-only runtime glue として非推奨化、のいずれかに分類する。
- [x] 旧 docs 由来の reusable idea を、Codex LAM design、workflow、CLI、pytest helper、review checklist、migration notes のどれへ反映するか判断する。
- [x] 移設しない legacy item について、理由を design、tasks、または migration notes に記録する。
- [x] `.claude/agents/` や subagent 定義は、原則として役割別レビュー観点、作業手順、workflow、task generation guidance として文書化する。
- [x] ただし agent/subagent は一律変換せず、design または tasks を作る時点で各項目ごとに Codex での扱いを個別確認する。
- [x] permission-level classification は Wave 2C では standalone validator へ移さず、migration notes と workflow guidance に留める。
- [x] scalable review を Codex-native audit procedure candidate として整理し、即時反映する review 原理と後続実装へ送る要素を分離する。
- [x] TDD introspection を Codex BUILDING の必須 gate にはせず、Claude `PostToolUse` 非依存の optional CLI / pytest helper candidate として位置づける。
- [x] cross-module blame を自動修正機構ではなく AUDITING の帰責判断支援として整理する。
- [x] MAGI を trigger-based decision protocol、`lam-orchestrate` を多ファイル作業の decomposition guidance として再表現する。
- [x] TDD introspection の後続入口として、retro 用入力の収集を優先した Codex-native CLI または pytest helper の spec を `docs/specs/feat-tdd-introspection-helper.md` に追加する。
- [x] `.claude/` をコピー済みの既存プロジェクト向け migration notes を追加する。

## Wave 2D: TDD introspection CLI pilot

`docs/specs/feat-tdd-introspection-helper.md` に基づき、optional helper の初手として
Codex-native CLI を最小スコープで導入する。

- [x] CLI の配置先と entrypoint を決める。
- [x] `record` サブコマンドの最小 I/O を定義する。
- [x] `timestamp`, `status`, `target`, `command` を 1 record として保存できるようにする。
- [x] 保存先を review 可能な workspace 内 path に限定する。
- [x] `PASS` / `FAIL` / `UNKNOWN` を区別して記録する。
- [x] 記録不能時に silent failure せず、理由を人間が確認できるようにする。
- [x] helper 未使用でも BUILDING が成立することを README ではなく workflow / spec / task 側で明確にする。
- [x] focused な実行例と最小 verification を追加する。
- [x] この wave では read-only な `summary` 表示までを対象にし、retro 集計の自動連携や pytest helper 連携は非スコープとする。
- [x] `docs/artifacts/tdd-introspection/sessions/*.log` は生成物として Git 管理外にする。
- [x] retro へ転記する最小フォーマットを usage artifact に定義する。
- [x] 保存単位を 1 session / 1 file にし、`SESSION_STATE.md` には最新 summary 要点だけ残す方針を決める。
- [x] pytest helper の要否を再判断し、現時点では採用せず CLI 継続とする。

## Wave 2E: Codex App Refresh Wave

Codex App の新機能を前提に、template / bootstrap / skill-plugin の配布モデルを再評価する。

- [x] R0: 公式情報と外部評価を調査し、`docs/artifacts/codex-app-refresh-wave-research.md` に snapshot として保存する。
- [x] R1: `docs/internal/10_DISTRIBUTION_MODEL.md` に `.agents/skills`、user-level skills、plugin の責務境界を反映する。
- [x] R2: project `.codex/config.toml` を template に含めるか、docs-only sample に留めるか判断する。
- [x] R3: `quick-load` を最初の project skill 候補として設計する。
- [x] R4: worktree mode、review pane、in-app browser、automations を既存 workflow docs の optional path として整理する。
- [x] R5: fresh repo / existing repo bootstrap の最小検証観点を定義する。
- [x] R6: distribution collateral refresh として README / QUICKSTART / CHEATSHEET / slides の文面と導線を Codex App 前提へ更新する。
  - 日本語を canonical、英語を追従版として整備する。
  - `README.md`, `README_en.md`, `QUICKSTART.md`, `CHEATSHEET.md`, `CHEATSHEET_en.md`, `CHANGELOG.md` の役割とリンクを確認する。
  - 既存リンクを維持するため `QUICKSTART_en.md` は必須追加候補として扱う。
  - `CONTRIBUTING.md`, `SECURITY.md` は R6 の最小ゴール外として defer。必要なら配布仕上げ gate で薄い版を別タスク化する。
## Wave 2F: Distribution finishing

R6 で文面と導線は Codex App 前提へ更新済み。ここでは画像・visual onboarding と
配布用の薄い補助文書を、Wave 3 legacy cleanup とは分けて仕上げる。

- [x] F0: README / HTML slides / 配布補助文書の仕上げ範囲を確認する。
  - `CONTRIBUTING.md` と `SECURITY.md` は現状存在しないため、薄い版を新規作成するか判断する。
  - README / HTML slides に入れる画像は、装飾ではなく onboarding の理解補助に限定する。
- [x] F1: README / HTML slides 用 visual asset plan を作る。
  - quick-load、worktree、review / ship、fresh repo bootstrap のうち、README に必要な画像と slides に必要な画像を分ける。
  - 画像を作らない項目は、理由を task または artifact に残す。
- [x] F2: `CONTRIBUTING.md` の薄い版を作成する。
  - LAM の truth hierarchy、phase / gate、small reviewable changes、quick-load / quick-save の扱いを短く案内する。
  - 詳細は `AGENTS.md` と `docs/internal/` へリンクし、重複した運用マニュアルにしない。
  - README / README_en から配布補助文書として参照できるようにする。
- [x] F3: `SECURITY.md` の薄い版を作成する。
  - security issue の扱い、sandbox / approval / secret handling、外部 API や tool contract drift の確認方針を短く案内する。
  - 詳細は `AGENTS.md` と `docs/internal/07_SECURITY_AND_AUTOMATION.md` へリンクする。
  - README / README_en から配布補助文書として参照できるようにする。
- [ ] F4: README / HTML slides に必要な画像または代替 visual を実装する。
  - 画像は template / starter kit の価値が直感的に伝わることを優先する。
  - `docs/slides/*.html` は「読ませる文書」ではなく「見て把握できる visual onboarding」として確認する。
- [ ] F5: 配布仕上げの確認を行う。
  - README / QUICKSTART / CHEATSHEET / slides / CONTRIBUTING / SECURITY のリンクを確認する。
  - `git diff --check` を実行する。
  - ドキュメントのみなら pytest は省略可。挙動に関わる変更があれば focused test を選ぶ。

## Wave 3: Legacy cleanup

Codex parity がレビューされ、移設対象と非推奨対象が明確になったあとで実施する。

- [ ] Wave 2F の配布仕上げ gate が完了しているか確認する。
- [ ] reviewer approval 後、top-level docs で `.claude/` を legacy として明記する。
- [ ] 日本語 mojibake の既存 docs を修復するか、英語のみを維持するか、bilingual docs として再生成するかを決める。
- [ ] Codex parity が受け入れられたあと、Claude-only docs を archive または削除する。
- [ ] R6 後の quickstart / cheatsheet に Claude 前提の表現が残っていないか確認し、残存分だけ修正する。

## Review Gates

- requirements review: behavior migration を拡張する前に実施する。
- ADR review: Claude assets の削除または archive 前に実施する。
- design review: portable validator や migration helper を実装する前に実施する。
- tasks review: 各 build wave の前に実施する。
- building review: implementation と tests が tasks と同期しているか確認する。
- auditing review: findings、残リスク、検証結果を確認する。
