# Security & Automation Protocols (Command Safety)

本ドキュメントは、"Living Architect" がターミナルコマンドを実行する際の安全基準（Allow List / Deny List）と、自動化のルールを定義する。

## 1. Core Principle (基本原則)

- **Safety First**: システムの破壊、データの消失、意図しない外部通信を防ぐことを最優先とする。
- **Automation with Consent**: 安全が確認された操作は自動化し（Allow List）、リスクのある操作は必ずユーザーの承認を得る（Deny List）。

## 2. Command Lists (コマンドリスト)

### A. Allow List (Auto-Run Safe)

以下のコマンドは、**副作用がなく（Read-Only）、かつローカル環境で完結するもの**であるため、ユーザー承認なしで実行してよい。

| Category               | Commands                                                      | Notes                              |
| :--------------------- | :------------------------------------------------------------ | :--------------------------------- |
| **File System (Read)** | `ls`, `cat`, `grep`, `pwd`, `du`, `file`                      | ファイル内容の読み取り、検索。`find` は v4.3.1 で ask に移動。 |
| **Git (Read)**         | `git status`, `git log`, `git diff`, `git show`, `git branch` | リポジトリ状態の確認。             |
| **Testing (Local)**    | `pytest`, `npm test`, `go test`                               | **ローカルでの**テスト実行。       |
| **Package Info**       | `npm list`, `pip list`                                        | インストール済みパッケージの確認。 |
| **Process Info**       | `ps`                                                          | プロセス状態の確認。               |

### B-1. Deny List (実行禁止)

以下のコマンドは、**不可逆または致命的な影響を持つ**ため、AI による実行を禁止する（`settings.json` の `deny` に対応）。削除が必要な場合はユーザーに削除候補リストを提示し、手動実行を依頼すること。

| Category                | Commands                                                       | Risks                                                        |
| :---------------------- | :------------------------------------------------------------- | :----------------------------------------------------------- |
| **File Deletion**       | `rm`, `rm -rf`                                                 | 不可逆なデータ消失。`git rm` で代替可能。                    |
| **File Move**           | `mv`                                                           | 意図しないファイル上書き。`git mv` または Read→Write で代替。 |
| **Permission Change**   | `chmod`, `chown`                                               | セキュリティ境界の破壊。                                     |
| **System Mutation**     | `apt`, `yum`, `brew`, `systemctl`, `service`, `reboot`, `shutdown` | システム設定の変更、再起動。                                 |
| **find 破壊パターン**   | `find -delete`, `find -exec rm`, `find -exec chmod/chown`      | 再帰的な破壊操作。                                           |

### B-2. Approval Required (承認必須)

以下のコマンドは、**システムに変更を加える（Write/Mutation）、または外部と通信するもの**であるため、実行前に必ずユーザーの承認を得なければならない（`settings.json` の `ask` に対応）。

| Category                | Commands                                                                    | Risks                                                        |
| :---------------------- | :-------------------------------------------------------------------------- | :----------------------------------------------------------- |
| **File System (Write)** | `cp`, `touch`, `mkdir`                                                      | ファイルのコピー、作成。                                     |
| **File Search**         | `find`                                                                      | 破壊的パターンは B-1 で deny。通常の検索は ask。             |
| **Git (Remote/Write)**  | `git push`, `git pull`, `git fetch`, `git clone`, `git commit`, `git merge` | リモートリポジトリへの影響、コンフリクト発生。               |
| **Network**             | `curl`, `wget`, `ssh`                                                       | 外部へのデータ送信、不正なスクリプトのダウンロード。         |
| **Build/Run**           | `npm start`, `npm run build`, `python main.py`, `make`                      | アプリケーションの実行（無限ループやリソース枯渇のリスク）。 |

> **Note**: Permission Layer 0（本ドキュメント）としては B-1, B-2 ともに「ユーザー承認なしに実行してはならない」。
> `settings.json`（Permission Layer 1）で deny（実行不可）/ ask（確認後実行可）の実際の制御粒度を設定する。

> **Note**: ファイルリネームが必要な場合、`mv` は Deny List に含まれるため以下の代替手段を用いる:
> - `Read` → `Write`（新名称で作成）→ `Write`（旧ファイルを空にするか削除依頼）
> - `git mv`（Git 追跡下のファイルの場合。ユーザー承認は必要）

### C. Gray Area Protocol (判断基準)

上記リストに含まれないコマンド、または引数によって挙動が大きく変わるコマンドについては、**原則として「Deny List」扱い（承認必須）**とする。

- 例: `make` (Makefile の中身によるため危険)
- 例: シェルスクリプト (`./script.sh`)

## 3. Automation Workflow

以下は Codex LAM の運用レベルでの判断指針である。実際の sandbox / approval UI の挙動は
Codex App と実行環境の設定に従う。

1.  **Check**: 実行したいコマンドが Allow List に含まれているか確認する。
2.  **Decide**:
    - **Allow List に含まれる**: そのまま実行する。
    - **含まれない**: ユーザーに承認を求める。
3.  **Log**: 実行結果を確認し、エラーが出た場合はユーザーに報告する。

## 4. Emergency Stop

ユーザーから「止めて」「ストップ」等の指示があった場合、直ちに実行中のコマンドを停止（`Ctrl+C` / `SIGINT`）し、全ての自動化プロセスを中断すること。

## 5. Permission Model And Automation Boundary

Codex LAM では、コマンド安全基準をまず運用ルールとして保持し、
runtime 固有の enforcement は canonical source にしない。

現時点の baseline は以下である:

- read-only inspection は広く許容する
- workspace 外 write、破壊的操作、高リスク mutation は明示確認する
- 権限等級の考え方は review と報告粒度の基準として使う
- validator や helper へ切り出す場合は、別の design review を通してから実装する

legacy runtime では native permission と dynamic hook 判定を組み合わせる多層モデルも使われていた。
その詳細は外部参照スナップショットと migration docs に残し、この公開 template の canonical rule にはしない。

> **用語注意**: 本セクションの「Permission Layer 0/1/2」は権限制御の多層モデルを指す。
> `00_PROJECT_STRUCTURE.md` Section 3 の「情報層 1/2/3」（SSOT の情報階層）とは別の概念である。
>
> **deny と ask の関係**: Section 2 の B-1 (Deny List) は「AI は自発的に実行してはならない」を意味する。
> 実際の allow / ask / deny は Codex App、sandbox、project trust、ユーザー承認設定に従う。

この legacy runtime は外部参照スナップショットに残すが、Codex でそのまま直移植する前提ではない。

### 権限等級 (PG/SE/PM)

PG/SE/PM は、Codex でも有用な判断原理として扱う。
現時点では hook による自動 enforcement ではなく、作業運用と review の基準として使う。

- **PG級**: 自動許可（読取専用ツール、lint 修正等）
- **SE級**: 許可 + 修正後にユーザーへ報告（src/ 配下の変更、ドキュメント更新等）
- **PM級**: ask 応答で承認ダイアログを表示（仕様書、ADR、ルールファイル、設定ファイルの変更）

詳細な分類原理は外部 legacy snapshot を参照できるが、Codex の canonical rule は
`AGENTS.md` と本ドキュメントで管理する。
standalone validator 化は将来候補だが、現 wave の baseline ではない。

### Automation Boundary

Codex では、以下を標準運用とする:

- テスト結果、変更意図、既知リスクは commentary と artifact で明示する
- doc sync や quick-save は手動 workflow として review 可能に保つ
- TDD introspection や session validation の自動化が必要になった場合だけ、
  CLI / pytest helper 候補として個別に設計する

legacy hook による常時自動記録や自律ループ制御は、
原理の参考にはしてよいが、Codex の標準前提にはしない。

Green State の判定基準自体は引き続き重要だが、
収束判定は hook 任せではなく、明示的な verification と報告で扱う。

## 6. Recommended Security Tools (推奨セキュリティツール)

### セキュリティレビュー補助

| ツール | 用途 | 導入方法 |
|:---|:---|:---|
| gitleaks | secret scan | local CLI または CI |
| CodeQL | GitHub 上の静的解析 | GitHub Actions |
| Dependabot | 依存関係更新と脆弱性通知 | GitHub repository settings |

### 依存脆弱性スキャン（プロジェクトに応じて選択）

| 言語 | ツール | コマンド |
|:---|:---|:---|
| JavaScript/Node.js | npm audit | `npm audit --audit-level=critical` |
| Python | pip-audit | `pip-audit --desc` |
| Python | safety | `safety check` |
| Go | govulncheck | `govulncheck ./...` |

### CI/CD 統合

CI へ入れる場合は、プロジェクトの言語・配布形態・secret 管理方式に合わせて、
gitleaks、CodeQL、依存脆弱性 scan のうち必要なものだけを採用する。
