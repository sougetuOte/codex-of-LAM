# WORKBOARD / Visualization Seed

作成日: 2026-05-10

## 目的

Codex App でプロジェクトを進める際に、現在の目標、作業ライン、依存関係、
gate 状態、検証状態が見えにくくなり、ユーザーと Codex の両方で判断負荷が
上がっている。

このファイルは、`WORKBOARD.md` とそこから生成する静的 HTML / SVG ビューの
起点案をまとめるための seed である。ここでは実装を確定せず、次の検討、
外部事例調査、仕様化の土台を作る。

## 現時点の仮説

`SESSION_STATE.md` だけでは、次回復帰には十分でも、プロジェクト全体の盤面を
見るには薄すぎる。一方で、`docs/specs/`, `docs/tasks/`, `docs/adr/`,
`docs/artifacts/` を横断で読むだけでは、情報量が多く、認知負荷がまだ高い。

そのため、次の三層構造がよさそうである。

| 層 | 役割 | 想定ファイル |
| --- | --- | --- |
| 復帰メモ | 次セッションで迷わない最小状態 | `SESSION_STATE.md` |
| 盤面 SSOT | 目標、ライン、gate、依存、active card | `WORKBOARD.md` |
| 詳細根拠 | 仕様、ADR、タスク、検証、判断ログ | `docs/specs/`, `docs/tasks/`, `docs/adr/`, `docs/artifacts/` |

加えて、`WORKBOARD.md` と関連 Markdown を解析して、静的な HTML / SVG ビューを
生成する。

## 目指す体験

- ユーザーが `WORKBOARD.md` を直接読める。
- Codex が quick-load 時に全文再読せず、冒頭 dashboard だけで現在地を把握できる。
- gate 前には HTML / SVG の全体ビューを見て、判断対象を視覚的に確認できる。
- 仕様、ADR、タスク、検証ログがリンクされ、動的な仕様書に近い体験になる。
- 生成物が壊れても、Markdown SSOT は残る。

## 中核ファイル案

```text
WORKBOARD.md                  # 人間と Codex が読む状態 SSOT
docs/tasks/*.md               # 詳細タスク
docs/specs/*.md               # 要求・仕様
docs/adr/*.md                 # 判断理由
docs/artifacts/*.md           # 判断ログ、レビュー、検証記録

tools/workboard.py            # validate / export / render
docs/project/index.html       # 生成された全体ダッシュボード
docs/project/workstreams.html # 生成されたライン別ビュー
docs/project/graph.svg        # 生成された依存グラフ
docs/project/cards/*.html     # 必要ならカード別詳細
```

## `WORKBOARD.md` の候補構造

### 1. Dashboard

- North Star
- 現在の phase
- active card
- blocked card
- 次の gate
- 直近の検証状態

### 2. Workstreams

例:

- Public template / release
- Workflow docs
- Project skills
- Review / audit
- Tooling / visualization

各 workstream には、目的、現在 gate、代表 card、参照ファイルを置く。

### 3. Gate Matrix

`requirements`, `design`, `tasks`, `building`, `auditing`, `released` のどこに
いるかを表で見る。

### 4. Kanban

`Backlog`, `Ready`, `Doing`, `Review`, `Done`, `Blocked` の簡単な card 一覧。

各 card は最低限以下を持つ。

- ID
- title
- status
- workstream
- next action
- evidence files
- verification
- blocker

### 5. Dependency Map

Mermaid または生成 SVG の source になる依存リストを置く。

## 静的ビュー案

### HTML

生成先候補: `docs/project/index.html`

役割:

- 全体 dashboard
- workstream 別の状態
- card へのリンク
- specs / tasks / ADR / artifacts へのリンク
- gate 前レビューの入口

### SVG

生成先候補: `docs/project/graph.svg`

役割:

- workstream 間の依存
- card 間の依存
- gate 状態
- blocked 箇所の視覚表示

### Mermaid

Markdown に直接埋め込む lightweight view として使う。

ただし、Mermaid から SVG への変換を必須にすると Node 系依存が増える可能性がある。
最初は Markdown 内 Mermaid と、Python 生成の簡易 SVG を分けて考える。

## 生成タイミング案

| タイミング | 生成 | 理由 |
| --- | --- | --- |
| quick-load | 原則しない | context と時間を節約する。冒頭 dashboard だけ読む。 |
| quick-save | validate 中心 | stale 化を防ぐ。重い render は必須にしない。 |
| gate 前 | 必ず render | 人間が判断する前に盤面を視覚確認する。 |
| release 前 | 必ず render | template / public repo として見える状態を保証する。 |
| ユーザーが全体把握を求めた時 | on-demand render | 認知負荷を下げるための明示コストとして扱う。 |

## 追跡方針案

- `WORKBOARD.md` は Git 管理対象。
- `tools/workboard.py` も Git 管理対象。
- `docs/project/*.html` と `docs/project/*.svg` は、deterministic に生成できるなら
  Git 管理対象にする。
- 生成 HTML には source file と生成日時または source hash を記録する。
- CI では、必要になった段階で「生成物が source とズレていないか」を検査する。

## 反対意見・懸念

### 1. 生成ビューが stale truth になる

生成物が更新されないと、Markdown より危険な誤情報になる。

対策:

- gate 前と release 前は render を必須にする。
- HTML に source hash / generated marker を入れる。
- CI で drift check を後から追加できるようにする。

### 2. quick-load が重くなる

全体可視化を quick-load に含めすぎると、過去に問題になった context 消費を繰り返す。

対策:

- quick-load は `SESSION_STATE.md` と `WORKBOARD.md` 冒頭 dashboard だけ読む。
- 詳細 card / HTML / SVG / docs 横断は必要時だけ読む。

### 3. 外部ツール依存が増える

Mermaid CLI、docs site generator、外部 Kanban などに依存すると、template としての
再利用性が落ちる。

対策:

- 最初は Markdown + 標準ライブラリ寄りの小さな generator にする。
- 外部ツールは SSOT ではなく view / adaptor として扱う。

### 4. 手書き HTML 化が運用負債になる

要望のたびに HTML / SVG を手作業で作ると、すぐ維持できなくなる。

対策:

- HTML / SVG は原則生成物にする。
- 手書きするのは template と generator だけにする。

## 外部調査メモ

次回以降に調べたいもの。

- Claude Code / Claude 側で話題になっている Markdown から HTML への workflow。
- Markdown SSOT から静的 docs / dashboard を生成する事例。
- Codex App / Claude Code / Cursor / agentic coding での Kanban, worktree, project graph 運用。
- Coddo, mymir, Task Master, Vibe Kanban などの思想と取り込み可能な要素。
- Mermaid, Markmap, mdBook, MkDocs, Docusaurus, Quartz などを使う場合の依存コスト。

## 最小 pilot 案

1. `WORKBOARD.md` の初版を作る。
2. `tools/workboard.py validate` で card ID、依存、blocked 理由を検査する。
3. `tools/workboard.py render` で `docs/project/index.html` と `docs/project/graph.svg` を生成する。
4. quick-load / quick-save / gate 前 / release 前のどこで読む・生成するかを
   `docs/internal/08_QUICK_LOAD_SAVE.md` または関連 workflow に反映する。

## 未決定事項

- `WORKBOARD.md` を root に置くか、`docs/project/WORKBOARD.md` に置くか。
- generated HTML / SVG を commit 対象にするか、local generated artifact に留めるか。
- generator を Python 標準ライブラリだけで始めるか、Markdown parser だけ導入するか。
- Mermaid を source として使うか、表示補助としてだけ使うか。
- CI drift check を初期 pilot に含めるか、後続 wave に分けるか。

## 現時点の推奨

最初は root の `WORKBOARD.md` を SSOT とし、`tools/workboard.py` で validate / render する。
外部ツールは fork して取り込まず、思想だけを参考にする。HTML / SVG は generated view として
扱い、Markdown SSOT を壊さない。

この seed をもとに、次は外部事例を調べて、採用する構造と捨てる構造を分ける。
