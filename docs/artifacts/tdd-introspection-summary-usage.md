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

## コマンド例

```powershell
python -m codex_lam.tdd_introspection_cli summary
```

## 見るポイント

- `FAIL` が多すぎないか
- `UNKNOWN` が残りすぎていないか
- `FAIL->PASS candidates` に、あとで振り返る価値のある対象があるか

## まだやらないこと

- rule candidate の自動生成
- retro への自動転記
- Green State 判定との自動連携

## メモ

- `summary` は read-only として使う
- 候補が 0 件でも異常ではない
- 使いにくさが出たら roadmap の Step 1 に戻って調整する
