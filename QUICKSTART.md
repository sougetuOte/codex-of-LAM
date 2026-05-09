# LAM クイックスタートガイド

> LAM の概念をまだ知らない方は、先に [概念説明スライド](docs/slides/index.html) をご覧ください。

## 前提条件

- Codex App
- Git
- GitHub アカウント
- Python 3.8+（補助 CLI や検証を使う場合）

## Step 1: テンプレートからリポジトリを作成

GitHub で「Use this template」ボタンをクリックし、新しいリポジトリを作成。

[Create from template](https://github.com/sougetuOte/codex-of-LAM/generate)

または手動でクローン:

```bash
git clone https://github.com/sougetuOte/codex-of-LAM.git my-project
cd my-project
rm -rf .git && git init
```

## Step 2: Codex App で開く

Codex App でリポジトリを開く。最初のセッションでは、AI にこう伝える:

```text
AGENTS.md と SESSION_STATE.md を読んで quick-load してください。
SESSION_STATE.md がなければ新規プロジェクトとして始めてください。
```

template 直後の fresh repo では、`SESSION_STATE.md` がまだ存在しないのが通常です。
その場合は `AGENTS.md`、`.codex/current-phase.md`、`.codex/workflows/` を入口にして PLANNING から始めます。

Codex LAM の入口は `AGENTS.md`、`.codex/current-phase.md`、`.codex/workflows/`、必要な `.agents/skills/` です。
旧 Claude Code 資料は Codex App の主制御面ではありません。archive / delete 判断が必要な場合は `docs/migration/` を参照します。

## Step 3: PLANNING から始める

新規プロジェクトなら、まず PLANNING フェーズでアイデアを伝える:

```text
PLANNING フェーズで始めます。
「〇〇を管理する Web アプリを作りたい」
```

AI が壁打ち相手になりながら、承認ゲートを一つずつ通過していく:

```text
1. アイデアを自然言語で伝える
2. AI と壁打ちしながら要件を具体化
3. 要求仕様書（docs/specs/）が出力される → 承認
4. ADR と設計書が出力される → 承認
5. タスク分解（docs/tasks/）が出力される → 承認
```

全ての承認ゲートを通過して初めて BUILDING に進める。

## Step 4: プロジェクトに合わせて LAM を適応

要件が固まったら、AI に一言伝える:

```text
要件定義が完了したので、LAM の全ファイルを確認して必要な部分をこのプロジェクトに適応させてください。
```

### 適応すべきファイル

| ファイル | 適応内容 |
|---------|---------|
| `AGENTS.md` | Identity セクションをプロジェクト名・説明に変更 |
| `README.md` / `README_en.md` | プロジェクトの説明に書き換え |
| `CHANGELOG.md` | 白紙から開始 |
| `docs/specs/` | LAM 自体の仕様書を削除 |
| `docs/adr/` | LAM 固有の ADR を削除 |
| `QUICKSTART.md` 等 | LAM 導入ガイドなので削除可 |

### そのままでよいファイル

| ディレクトリ | 理由 |
|-------------|------|
| `.codex/workflows/` | Codex-native のフェーズ、レビュー、quick-load/save 手順 |
| `.agents/skills/` | Codex App で使う project skill 候補 |
| `docs/internal/` | 開発プロセスの SSOT |
| `docs/artifacts/knowledge/` | プロジェクト知見の蓄積 |
| `CHEATSHEET.md` | 運用リファレンス |

## Step 5: 最初の BUILDING セッション

承認済み tasks ができたら、BUILDING フェーズに切り替えて TDD 実装を始める。

```text
BUILDING フェーズに進みます。
承認済み task の最小単位から Red-Green-Refactor で進めてください。
```

完了後は AUDITING フェーズでレビューし、Green State、検証結果、残リスクを明示する。

## よくある質問

### Q: セッションが切れたら？

A: `quick-load` で復帰します。`SESSION_STATE.md` が短い復元メモとして機能します。

### Q: セーブはどうする？

A: `quick-save` で `SESSION_STATE.md` を更新します。長いログは `docs/daily/` へ逃がし、git commit は別操作にします。


## 次のステップ

1. [新規プロジェクトスライド](docs/slides/story-newproject.html) で流れを確認
2. Codex App で最初の PLANNING セッションを始める
3. [CHEATSHEET.md](CHEATSHEET.md) を手元に置いて日常運用
4. 慣れてきたら [docs/internal/](docs/internal/) でプロセス SSOT を深掘り
