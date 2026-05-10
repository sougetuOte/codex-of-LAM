# Drift / Generation Timing Harvest Notes

Status: Raw harvest
Date: 2026-05-10

## Purpose

`WORKBOARD.md` から HTML / SVG を生成する場合、生成物が古びて stale truth に
なる危険がある。生成タイミング、drift check、commit 方針、CI 方針の参考材料を
集める。

## Harvest Policy

- 生成物は SSOT ではなく view として扱う。
- quick-load を重くしない。
- Gate / release 前に人間が見るための生成物は、できるだけ deterministic にする。

## Sources

| Source | URL | Notes |
| --- | --- | --- |
| pre-commit | https://pre-commit.com/ | commit 前 hook framework。format / lint / generated file check に使える。 |
| GitHub Actions workflow artifacts | https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts | CI run の生成物を artifact として保存・共有できる。 |
| GitHub Pages custom workflow | https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages | 任意の static site generator を Actions で build/deploy できる。 |
| MkDocs deploying docs | https://www.mkdocs.org/user-guide/deploying-your-docs/ | `site/` generation と deployment の考え方。 |
| Docusaurus deployment | https://docusaurus.io/docs/deployment | build output と GitHub Pages deploy の標準パターン。 |
| mdBook CI example | https://rust-lang.github.io/mdBook/continuous-integration.html | mdBook の CI build / deploy examples。 |
| seite | https://seite.sh/ | AI-native site generator として dry-run / GitHub Actions setup のヒントがある。 |

## Findings

### pre-commit

- commit 前に validator や generator を走らせる用途に向く。
- generated files が変更されたら commit を止める、という drift check に使える。
- ただし template 利用者に pre-commit install を要求すると摩擦が増える。
- Codex App の通常運用では、hook 前提にしない方針と衝突しないよう optional にする。

Classification: `decide_later`

### GitHub Actions workflow artifacts

- HTML / SVG を commit せず、CI artifact として保存する選択肢がある。
- review 用 preview としては良い。
- ただし clone 直後や GitHub repo browsing で見える static dashboard にはならない。

Classification: `decide_later`

### GitHub Pages custom workflow

- source から static site を build して Pages に deploy できる。
- public template として見せるには強い。
- initial pilot では Pages deploy まで含めず、local render / tracked artifact から始めるのが軽い。

Classification: `decide_later`

### MkDocs / Docusaurus deployment

- どちらも source と generated output を分ける前提がある。
- generated output を手で編集しない、build output を deploy target にする、という思想が
  LAM dashboard にも使える。
- ただし docs site generator の build lifecycle をそのまま持ち込むと重い。

Classification: `adopt_candidate` for principle, `decide_later` for tool adoption

### mdBook CI

- build artifact を CI で作る流れは分かりやすい。
- single binary / deterministic build に寄せられるなら template と相性がよい。
- ただし `WORKBOARD.md` dashboard より book publishing 寄り。

Classification: `decide_later`

### seite

- dry-run や CI setup への意識があり、agent-operated static docs の運用例として参考になる。
- 直接採用する前に、license、CLI の安定性、生成物の deterministic 性を確認したい。

Classification: `decide_later`

## Combination Ideas

### C1: Manual Render First

初期 pilot は `python tools/workboard.py render` を手動実行する。

- quick-load は軽い。
- gate 前と release 前だけ render を要求する。
- CI や hook は後回し。

### C2: Deterministic Tracked Artifacts

`docs/project/index.html` と `docs/project/graph.svg` を commit 対象にする。

- clone / GitHub browsing で見える。
- source hash を入れ、drift が分かるようにする。
- CI で `render` 後に diff check できる。

### C3: CI Artifact Preview

HTML / SVG を commit しない代わりに、CI artifact として保存する。

- repo を汚しにくい。
- review 時の取得が一手増える。
- public template の first-view value は弱くなる。

### C4: Optional Pre-commit

後続 wave で optional にする。

- 開発者が望めば local drift check できる。
- Codex LAM の標準は hook 依存にしない。

## Suggested Generation Contract

### quick-load

- render しない。
- `SESSION_STATE.md` と `WORKBOARD.md` 冒頭 dashboard だけ読む。

### quick-save

- `WORKBOARD.md` が変わった場合だけ validate を検討する。
- render は必須にしない。

### gate 前

- validate と render を必須にする。
- generated HTML / SVG を人間が見る。

### release 前

- validate と render を必須にする。
- tracked artifacts を採用する場合は diff clean を確認する。

### on-demand

- ユーザーが「全体見たい」と言ったら render する。
- 認知負荷を下げるための明示コストとして扱う。

## Adoption Candidates

- Baseline now:
  - generated view は SSOT ではなく view。
  - gate 前 / release 前 render を contract にする。
  - quick-load では render しない。

- Next wave:
  - source hash / generated marker を HTML / SVG に入れる。
  - `tools/workboard.py check-generated` を追加する。
  - GitHub Actions で drift check する。

- Reject for initial pilot:
  - pre-commit hook 必須化。
  - GitHub Pages deploy を pilot に含める。
  - docs site generator を build pipeline の前提にする。

## Open Questions

- generated HTML / SVG を commit するか、CI artifact にするか。
- drift check は `git diff --exit-code docs/project` 型で足りるか。
- source hash は `WORKBOARD.md` 単体か、linked files も含めるか。
- render の実行環境は Python 標準ライブラリだけで始めるか。
