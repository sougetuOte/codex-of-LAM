# Distribution visual asset plan

作成日: 2026-05-09

## 目的

Wave 2F では、R6 で更新済みの README / QUICKSTART / CHEATSHEET / HTML slides を、
template / starter kit として初見でも把握しやすい配布物へ仕上げる。

画像は装飾ではなく、Codex App での導入、再開、レビュー、配布判断を短時間で理解するための
visual onboarding として扱う。

## 採用方針

- README には、最初の理解に効く画像だけを入れる。
- HTML slides には、README より少し多めに、手順の流れが見える visual を入れる。
- quick-load / worktree / review / ship / fresh repo bootstrap は、文章だけで十分な箇所と、
  visual が必要な箇所を分ける。
- 画像を作らない項目は、理由をこの plan に残す。

## 対象別判断

| 対象 | README | HTML slides | 判断 |
| --- | --- | --- | --- |
| template / starter kit overview | 追加候補 | 追加候補 | README の first viewport 直後か「使い方」前に、全体像を 1 枚で示す価値がある。 |
| quick-load | 追加候補 | 追加候補 | SESSION_STATE.md と最小確認 bundle の関係を図示すると復帰手順が伝わりやすい。 |
| worktree mode | なし | 追加候補 | README では optional path として重すぎる。slides では Codex App option として示す価値がある。 |
| review / ship | なし | 追加候補 | README では gate の説明で足りる。slides では review pane / push 前確認の流れを見せる価値がある。 |
| fresh repo bootstrap | 追加候補 | 追加候補 | template / starter kit の価値そのものなので README と slides の両方で有効。 |
| CONTRIBUTING / SECURITY | なし | なし | 補助文書は text-first で十分。画像化すると保守対象が増える。 |

## 初期スコープ

最初の実装では、生成画像よりも保守しやすい local asset を優先する。

1. `docs/slides/assets/` または同等の配布用 asset directory を作る。
2. まずは SVG / HTML diagram / screenshot placeholder のどれが最小か判断する。
3. README には最大 2 枚までに制限する。
4. slides には各 deck の理解を助ける範囲で追加する。

## 未決定

- 実画像を AI 生成するか、repo-native な SVG / HTML diagram にするか。
- README に入れる最終枚数。
- `docs/slides/assets/` を新設するか、既存構造に合わせて別名にするか。
