# TDD Introspection Summary Usage

Status: Draft  
Date: 2026-04-30

## 目的

`summary` を retro 前の軽い確認手順として使い、
FAIL -> PASS 候補を見落としにくくする。

## 使うタイミング

- focused test をいくつか回したあと
- ひと区切りの BUILDING を終える前
- retro メモを書く直前

## 最小手順

1. `record` で focused test の結果を残す
2. 区切りで `summary` を実行する
3. FAIL -> PASS 候補があれば retro メモへ転記する

## retro 前チェック手順

BUILDING の区切り、または retro メモを書く直前に以下を行う。

1. `summary` を実行する
2. `PASS` / `FAIL` / `UNKNOWN` の件数を見る
3. `FAIL->PASS candidates` を retro に転記するか判断する
4. `UNKNOWN` が残っている場合は、失敗の性質を 1 行で残す
5. この時点では rule candidate を自動生成しない

`UNKNOWN` は異常扱いではない。
Windows ACL、外部依存、環境差分などで focused test の結果が判定不能だった場合は、
retro では「実装の失敗」ではなく「検証環境の注意点」として扱う。

## コマンド例

```powershell
python -m codex_lam.tdd_introspection_cli summary
```

## 見るポイント

- `FAIL` が多すぎないか
- `UNKNOWN` が残りすぎていないか
- `FAIL->PASS candidates` に、あとで振り返る価値のある対象があるか

## retro への最小転記フォーマット

retro メモには、必要なら次の最小形で転記する。

```markdown
### TDD Introspection

- Summary:
  - PASS: <count>
  - FAIL: <count>
  - UNKNOWN: <count>
- FAIL->PASS candidates:
  - <target 1>
  - <target 2>
- Notes:
  - <short observation>
```

候補が 0 件なら `FAIL->PASS candidates: none` とだけ残せばよい。
`UNKNOWN` が 1 件以上ある場合は、`Notes` に原因を短く残す。

## 転記判断

- FAIL -> PASS 候補がある場合は、retro へ転記する。
- `UNKNOWN` が環境要因なら、retro へ転記するか `SESSION_STATE.md` の環境メモへ残す。
- `UNKNOWN` が実装不明点なら、次の focused check として扱う。
- 候補が 0 件で、`UNKNOWN` も既知環境要因だけなら、retro には `none` だけでよい。

## まだやらないこと

- rule candidate の自動生成
- retro への自動転記
- Green State 判定との自動連携

## メモ

- `summary` は read-only として使う
- 候補が 0 件でも異常ではない
- `docs/artifacts/tdd-introspection-records.log` はローカル生成物として扱い、Git へは載せない
- 使いにくさが出たら roadmap の Step 1 に戻って調整する
