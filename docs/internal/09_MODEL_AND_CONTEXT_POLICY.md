# Model And Context Policy

Codex LAM におけるモデル選定とコンテキスト節約の基本方針を定義する。

Status: Draft
Date: 2026-04-30

## 1. 背景

このプロジェクトでは、単純な流れ作業よりも、設計、ADR、仕様整合、legacy migration のような
**文脈依存の強い判断**が多い。

そのため、問題は単なる token 消費ではなく、**context compaction による設計文脈の欠落**である。

特に危険なのは以下の状態である。

- 長いセッションの途中で、前提、非採用案、承認済み制約が暗黙知化する
- 大量ドキュメントを強いモデルへ一気に流し込み、重要な判断根拠が圧縮で脱落する
- quick-load のつもりが、再開前に広範囲の全文読みに戻る
- routine task と architecture decision で同じモデル運用をしてしまう

流れ作業的な session では大きな問題にならなくても、設計や review では致命傷になりうる。

## 2. 基本方針

この repository では、以下を標準運用とする。

1. 通常作業の基本モデルは `5.4` とする。
2. 広い corpus を読む前に、可能な限り `context-harvest` で前処理する。
3. `5.5` は routine に使わず、最終判断または高リスク裁定に限定する。
4. 設計文脈は、長い会話履歴ではなく、`SESSION_STATE.md`、harvest note、spec / ADR / design / tasks に外部化して保持する。
5. quick-load は再開であって再読破ではない。最小確認の後、必要時だけ深掘りする。
6. Codex App on Windows では、日常作業の shell も `pwsh -NoProfile` を標準にし、
   shell 起動の不安定さと PowerShell profile ノイズを避ける。

## 3. 標準モデル運用

### 3.1 `5.4` を基本にする作業

以下は原則として `5.4` で扱う。

- 限定範囲の実装
- docs 更新
- focused review
- 小規模な spec / task 同期
- 既に前提が固まっている判断
- quick-load 後の初動整理

### 3.2 `context-harvest` を先に使う作業

以下は、強いモデルへ bulk input する前に `context-harvest` を優先する。

- `docs/` 配下の広い棚卸し
- legacy project からの知見移設
- 複数 directory にまたがる調査
- 長い会話や日次ログの再整理
- 大規模 review の前処理

`context-harvest` の目的は、全文を賢く読むことではなく、**強いモデルが読む量を減らし、
判断に必要な evidence を薄い中間成果物へ落とすこと**である。

### 3.3 `5.5` へ上げる条件

`5.5` は以下の条件のいずれかを満たす場合だけ検討する。

- 不可逆な設計判断で、誤りコストが高い
- 承認ゲートに影響する
- harvest note 同士が衝突し、裁定が必要
- `5.4` の観点分離では結論が収束しない
- 要件、ADR、設計、tasks の整合が崩れており、論点の再編成が必要
- ユーザーが高コストでも高信頼の最終判断を明示的に求めた

## 4. 設計文脈を守るためのルール

### 4.1 文脈は会話に置かず、artifact に置く

設計文脈は、以下へ意識的に書き出す。

- `SESSION_STATE.md`
- harvest notes / decision notes
- `docs/specs/`
- `docs/adr/`
- `docs/design/`
- `docs/tasks/`

長いやり取りの記憶に依存しない。

### 4.2 「読む量」ではなく「判断単位」で分ける

大きい corpus は、topic / wave /論点単位で分割する。

悪い例:

- `docs/` 全体をまとめて読む
- legacy design を一括で top model に読ませる

良い例:

- model routing
- review policy
- permission / security
- quick-load / session handoff

### 4.3 quick-load では全文読みに戻らない

quick-load の初動では、まず以下だけで再開判断する。

- `.codex/current-phase.md`
- `git status --short --branch`
- `git log --oneline --decorate -3`
- `SESSION_STATE.md` の要約、未 commit 変更、次にやること

追加の文書読みは、次の 1 手を決めるのに不足した時だけ行う。

### 4.4 強いモデルは「読む係」ではなく「決める係」

`5.5` は bulk reader ではない。

先に軽量な harvesting、分類、要約、ノート化を行い、`5.5` はそのノートを読んで
採否、裁定、承認レベル判断を行う。

### 4.5 設計・レビューは危険域に入る前に切る

設計、ADR、仕様衝突整理、広い review では、**圧縮限界まで粘る**より、
**文脈が健全なうちに session を切る**ことを優先する。

基本運用:

- 設計や review は、長時間連続で抱え込む前提にしない
- context compaction の危険域が見えたら、続行より `quick-save` を優先する
- 必要なら次 session で再開する
- 同一 session を続ける場合でも、artifact へ書き出してから実質的に state を切り替える

これは中断コストを増やすためではなく、**判断根拠の変質を防ぐための安全策**である。

### 4.6 危険域の兆候

以下は、設計文脈が変質し始めている兆候として扱う。

- 非採用案や却下理由を即答しにくくなる
- 「なぜその判断だったか」の根拠が薄くなる
- 同じ spec / design / code を何度も読み返し始める
- 直近の要約は合っているが、重要な制約が抜けている感触がある
- 論点が増えたのに、未決事項の一覧が artifact に反映されていない
- review で、重大論点より wording や局所論点へ意識が流れ始める

これらが出たら、会話を延命せず外部化して切る。

### 4.7 危険域での標準対応

危険域に入ったら、次を最小セットとして残す。

- 決定事項
- 未決事項
- 次の 1 手
- 参照元 file
- 非採用案とその理由
- 注意点や罠

保存先の優先順位:

1. `SESSION_STATE.md`
2. 必要なら harvest note / decision note
3. 承認済み内容なら spec / ADR / design / tasks

重要なのは、**あとで思い出すこと**ではなく、**今のうちに変質前の文脈を固定すること**である。

## 5. 運用パターン

### Pattern A: routine implementation

- `5.4` で着手
- shell は `pwsh -NoProfile` を標準にする
- 必要な file だけ読む
- focused test / docs sync
- `SESSION_STATE.md` へ差分記録

### Pattern B: wide document migration

- corpus を topic ごとに分割
- `context-harvest` で raw note を作る
- decision note に集約する
- 必要時だけ `5.5` で採否判断する

### Pattern C: architecture or ADR decision

- 先に関連 spec / ADR / design の該当箇所を絞る
- `5.4` ベースで MAGI / AoT を回す
- 収束しないときだけ `5.5` で裁定する

### Pattern D: Windows-specific work

- Windows ACL、`Start-Process`、Explorer / Electron、PowerShell 固有の管理操作などでは
  `pwsh -NoProfile` を使う
- それ以外の通常作業でも、Codex App on Windows では `pwsh -NoProfile` を使う
- shell の起動ノイズや profile error を、context 汚染源として扱う

## 6. anti-pattern

以下は避ける。

- 何でも最初から `5.5` に投げる
- context limit を、より強いモデル投入だけで解決しようとする
- harvest note を作らず、毎回原文を読み直す
- quick-load で tasks / design / code を最初から全文読む
- 設計根拠を会話中にだけ置き、artifact に残さない
- 日常の read-only 作業まで profile 付き PowerShell で流して、無関係な起動ノイズを拾う

## 7. 現在の推奨

当面の repository 運用では、以下を推奨する。

- 基本モデルは `5.4`
- 広い読書き前は `context-harvest`
- `5.5` は本当に詰まった時の裁定用
- context compaction が疑われたら、会話を延命せず artifact へ書き出して再開する
- 設計や review は、危険域に入る前に `quick-save` して session を切ることを標準選択肢にする
- Codex App on Windows では shell は `pwsh -NoProfile` を標準にする

この文書は、Codex LAM における model cost 最適化だけでなく、
**設計文脈の生存率を上げるための運用基準**として扱う。
