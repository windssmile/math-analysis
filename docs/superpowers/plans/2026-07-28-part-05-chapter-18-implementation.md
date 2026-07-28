# Part V Chapter 18 and Derivative Training Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Chapter 14 derivative-practice bridge and publish all five self-study units of Chapter 18 without using Riemann integration or the fundamental theorem prematurely.

**Architecture:** Preserve the existing Zensical Markdown architecture and stable unit IDs. First close the Chapter 14 training prerequisite and reconcile Part IV/book hours, then establish failing Chapter 18 contracts, write the five units in proof-dependency order, register the pages, and finish with a combined mathematical and publication review. Stop after Chapter 18 passes the full quality gate.

**Tech Stack:** Markdown with YAML front matter, Zensical 0.0.51, MkDocs-compatible navigation, Python 3.12 `unittest`, PyYAML, project content/site checkers, Git.

---

## 1. File map and responsibility boundaries

### Files to create

- `content/chapters/chapter-14/u-04-14-05-derivative-fluency-for-antiderivatives.md`  
  The standalone derivative-fluency bridge. It trains existing rules and introduces no new calculus theorem.
- `content/chapters/chapter-18/index.md`  
  Chapter 18 guide, proof ladder, five-unit reading order, and Chapter 17/19 boundary.
- `content/chapters/chapter-18/u-05-18-01-antiderivatives.md`  
  Antiderivatives, constant ambiguity, interval scope, and the Darboux obstruction.
- `content/chapters/chapter-18/u-05-18-02-substitution.md`  
  Substitution derived from the chain rule, with domain and branch checks.
- `content/chapters/chapter-18/u-05-18-03-integration-by-parts.md`  
  Integration by parts derived from the product rule, including route selection.
- `content/chapters/chapter-18/u-05-18-04-rational-functions.md`  
  Polynomial division, partial fractions, repeated linear factors, and irreducible quadratic factors.
- `content/chapters/chapter-18/u-05-18-05-method-selection.md`  
  Mixed integration practice, error diagnosis, and derivative verification.
- `docs/curriculum/part-05-dependencies.md`  
  The 22-unit Part V dependency and unique-responsibility map; only Chapter 18 is marked published.
- `tests/test_chapter_18.py`  
  Chapter 18 metadata, anchor, content-boundary, training-density, navigation, and release contracts.
- `docs/reviews/2026-07-28-chapter-14-05-and-chapter-18-review.md`  
  Final combined content/mathematics/publication review for this implementation boundary.

### Files to modify

- `tests/test_chapter_14.py`  
  Add the fifth unit, its anchors, training-density checks, and new `5+2=7` hour closure.
- `tests/test_part_04_consistency.py`  
  Change Part IV to 21 units and `26+12.5=38.5`; require the Chapter 14.5 dependency entry.
- `tests/test_chapter_15.py`, `tests/test_chapter_16.py`, `tests/test_chapter_17.py`  
  Replace stale book and Part IV totals with the approved `292+100=392` and `26+12.5=38.5` totals.
- `tests/test_zensical_structure.py`, `tests/test_mkdocs_site.py`  
  Require the final release count and representative Chapter 14.5/18 rendered anchors.
- `content/chapters/chapter-14/index.md`  
  Add the training unit and explain its Chapter 18 bridge role.
- `mkdocs.yml`  
  Add Chapter 14.5, Part V, the Chapter 18 guide, and five Chapter 18 units in reading order.
- `content/course-map.md`  
  Add Chapter 14.5, Chapter 18, exact hours, links, and final published count.
- `README.md`  
  Advance the release surface to Part V Chapter 18 and 78 published units.
- `scripts/check_site.py`  
  Require representative stable anchors and navigation markers for Chapter 14.5 and Chapter 18.
- `docs/curriculum/part-04-dependencies.md`  
  Add Chapter 14.5 as the forward derivative-training bridge.
- `docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md`  
  Reconcile Chapter 14, Part IV, unit-count, and hour totals.
- `docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md`  
  Reconcile Part IV, Part V, and whole-book totals to `292+100=392`.
- `docs/reviews/2026-07-27-part-04-consistency-review.md`  
  Record the approved post-release Chapter 14.5 extension without rewriting the historical review.

### Files intentionally not created

- No symbolic-integration Python module: Chapter 18 is about mathematical method selection and derivative verification, not a computer algebra system.
- No Riemann-integration page or API: those belong to Chapter 19.
- No empty Chapter 19 pages: the implementation stops at the Chapter 18 acceptance point.

## 2. Required unit metadata

Use these exact records.

| Unit | Slug | Theory | Applied |
|---|---|---:|---:|
| `u-04-14-05` | `derivative-fluency-for-antiderivatives` | 0.50 | 1.50 |
| `u-05-18-01` | `antiderivatives` | 1.25 | 0.25 |
| `u-05-18-02` | `substitution` | 1.00 | 0.50 |
| `u-05-18-03` | `integration-by-parts` | 1.00 | 0.50 |
| `u-05-18-04` | `rational-functions` | 1.00 | 0.50 |
| `u-05-18-05` | `method-selection` | 0.25 | 1.75 |

Every page uses `content_standard: 2`, all four prerequisite categories, a stable H1 anchor equal to
`unit_id`, all nine required v2 headings, at least two anchored examples, at least five anchored
exercises, and at least seven page-local collapsed answers. Units 14.5 and 18.5 each contain at least
12 exercises with full answers.

### Task 1: Verify the clean approved baseline

**Files:**
- Inspect: `docs/superpowers/specs/2026-07-28-part-05-integration-design.md`
- Inspect: `content/chapters/chapter-14/`
- Inspect: `tests/test_chapter_14.py`

- [ ] **Step 1: Confirm the branch and worktree state**

Run:

```bash
git status --short --branch
git log -2 --oneline
```

Expected: the branch contains commit `2fc55fd`, and no uncommitted files are present.

- [ ] **Step 2: Run the current full quality gate**

Run:

```bash
make verify
```

Expected: 143 tests pass, `scripts/check_content.py` exits 0, Zensical prints `No issues found`, and
`scripts/check_site.py` exits 0.

### Task 2: Lock the Chapter 14.5 contract with failing tests

**Files:**
- Modify: `tests/test_chapter_14.py`
- Modify: `tests/test_part_04_consistency.py`
- Modify: `tests/test_chapter_15.py`
- Modify: `tests/test_chapter_16.py`
- Modify: `tests/test_chapter_17.py`

- [ ] **Step 1: Add the exact fifth unit record**

Append this tuple to `EXPECTED_UNITS` in `tests/test_chapter_14.py`:

```python
(
    "u-04-14-05",
    "怎样为原函数计算准备可靠的求导能力？",
    0.50,
    1.50,
    "derivative-fluency-for-antiderivatives",
),
```

Add:

```python
"u-04-14-05": (
    "tbl-u-04-14-05-structure-signals",
    "ex-u-04-14-05-nested-chain",
    "ex-u-04-14-05-error-diagnosis",
),
```

Change Chapter 14 totals to:

```python
self.assertEqual(5.0, theory)
self.assertEqual(3.0, applied)
```

Change the guide assertion to:

```python
self.assertIn("本章共5个核心单元，8学时（理论5，应用3）。", guide)
self.assertIn("第 18 章", guide)
```

- [ ] **Step 2: Add the training-density and boundary test**

Add to `ChapterFourteenTests`:

```python
def test_derivative_fluency_unit_prepares_integration_without_teaching_it(self) -> None:
    path = unit_path(EXPECTED_UNITS[4])
    text = path.read_text(encoding="utf-8")
    self.assertGreaterEqual(text.count("{#pr-u-04-14-05-"), 12)
    self.assertGreaterEqual(text.count('??? note "答案"'), 14)
    for marker in (
        "结构识别",
        "错误诊断",
        "定义域",
        "第 18 章",
        "求导回验",
    ):
        self.assertIn(marker, text)
    core = text.split("## 常见误区与后续", 1)[0]
    for forbidden in ("换元积分公式", "分部积分公式", "Riemann 积分", "微积分基本定理"):
        self.assertNotIn(forbidden, core)
```

- [ ] **Step 3: Reconcile Part IV contract expectations**

In `tests/test_part_04_consistency.py`, rename the first test and require:

```python
self.assertEqual(21, len(units))
self.assertEqual(21, len(set(unit_ids)))
self.assertEqual(26.0, sum(float(record["hours"]["theory"]) for record in records))
self.assertEqual(12.5, sum(float(record["hours"]["applied"]) for record in records))
```

Require these design strings:

```python
self.assertIn("| **第四部** | **26** | **12.5** | **38.5** |", part)
self.assertIn("| IV | 微分与局部线性化 | 26 | 12.5 | 38.5 |", master)
self.assertIn("| V | 积分、累积与数值求积 | 26 | 13.5 | 39.5 |", master)
self.assertIn("| **当前总计** |  | **292** | **100** | **392** |", master)
```

Update identical stale-total assertions in `tests/test_chapter_15.py` and
`tests/test_chapter_17.py`. Add `tests/test_chapter_16.py` to the release-count update set so the
full suite can close when Chapter 14.5 is published.

- [ ] **Step 4: Run the tests and verify the intended failures**

Run:

```bash
python3.12 -m unittest tests.test_chapter_14 tests.test_part_04_consistency tests.test_chapter_15 tests.test_chapter_16 tests.test_chapter_17 -v
```

Expected: failures report the missing `u-04-14-05` page and stale hour/design totals; existing
mathematics tests continue to pass.

- [ ] **Step 5: Commit the red contract**

```bash
git add tests/test_chapter_14.py tests/test_part_04_consistency.py tests/test_chapter_15.py tests/test_chapter_16.py tests/test_chapter_17.py
git commit -m "test: lock derivative training bridge contract"
```

### Task 3: Write the Chapter 14.5 derivative-fluency unit

**Files:**
- Create: `content/chapters/chapter-14/u-04-14-05-derivative-fluency-for-antiderivatives.md`
- Modify: `content/chapters/chapter-14/index.md`

- [ ] **Step 1: Create the exact front matter and section skeleton**

Start the page with:

```markdown
---
title: 怎样为原函数计算准备可靠的求导能力？
unit_id: u-04-14-05
hours: {theory: 0.50, applied: 1.50}
difficulty: 3
prerequisites:
  book: [u-04-14-01, u-04-14-02, u-04-14-03, u-04-14-04]
  higher_algebra: [因式分解与通分, 指数和对数运算, 三角恒等变形]
  analytic_geometry: [函数图像, 定义域与分支]
  python: [函数求值, 数值点检]
capabilities: [derivative_computation, structure_recognition, error_diagnosis, verification]
learning_goals: [熟练组合求导法则, 识别复合与乘积结构, 检查定义域和分支, 用替代路线回验结果]
content_standard: 2
---

# 怎样为原函数计算准备可靠的求导能力？ {#u-04-14-05}
```

Use the exact v2 section order:

```markdown
## 先备知识
## 学习目标
## 牵引问题
## 探索与猜想
## 概念与理论
## 例题与迁移
## 即时检验与回望
## 习题与答案
## 常见误区与后续
```

- [ ] **Step 2: Write the structure-recognition table and examples**

Create anchor `{#tbl-u-04-14-05-structure-signals}` and include these rows:

| Visible structure | Differentiate as | Required check |
|---|---|---|
| \(F(g(x))\) | \(F'(g(x))g'(x)\) | inner derivative and domain |
| \(u(x)v(x)\) | \(u'v+uv'\) | both factors differentiable |
| \(u(x)/v(x)\) | \((u'v-uv')/v^2\) | \(v\ne0\) |
| \(u(x)^{v(x)}\) | logarithmic differentiation | \(u>0\) on the working interval |
| inverse branch | reciprocal derivative | branch continuity and nonzero original derivative |

Use anchored examples:

- `{#ex-u-04-14-05-nested-chain}`: completely differentiate
  \(e^{\sin(x^2)}\), naming both inner layers and checking the all-real domain.
- `{#ex-u-04-14-05-error-diagnosis}`: diagnose the first illegal step in
  \(\frac{d}{dx}\log(x^2-1)=2x/(x^2-1)\) when the solver claims the formula on
  all real numbers; correct the domain to \((-\infty,-1)\cup(1,\infty)\).

Add two immediate checks with collapsed answers:

1. Differentiate \(x e^{x^2}\) and identify the product and chain contributions.
2. Explain why differentiating \(\sqrt{x^2}\) as if it were \(x\) loses the branch at \(x<0\).

- [ ] **Step 3: Add 12 graded exercises and complete answers**

Use anchors `pr-u-04-14-05-01` through `pr-u-04-14-05-12`. Cover exactly:

1. polynomial/rational simplification;
2. \(e^{3x-x^2}\);
3. \(\log(1+x^2)\);
4. \(\sin(\sqrt{1+x})\);
5. \(x^2e^{-x}\);
6. \(x\log x\);
7. \((1+x^2)^{-1}\);
8. \(\arctan(2x)\);
9. \(x^x\) on \(x>0\);
10. implicit differentiation of \(x^2+y^2=1\) on an already-given differentiable branch;
11. diagnose a missing chain factor;
12. compare two independently simplified derivatives of
    \((x^2+1)e^{-x}\).

Every exercise receives an adjacent `??? note "答案"` block. Include the two examples and two
immediate checks with answers, so the page has at least 16 collapsed answers.

- [ ] **Step 4: Update the Chapter 14 guide**

Change the guide to:

```markdown
本章共5个核心单元，8学时（理论5，应用3）。
```

Add item 5:

```markdown
5. [怎样为原函数计算准备可靠的求导能力？](u-04-14-05-derivative-fluency-for-antiderivatives.md)
   （理论 0.50，应用 1.50）
```

Explain that 14.5 trains already-proved rules, exports forward structure recognition to Chapter 18,
and does not state substitution or integration-by-parts formulas.

- [ ] **Step 5: Run the focused content and chapter checks**

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_14 -v
```

Expected: content check passes; Chapter 14 tests still fail only because navigation/course-map
registration has not yet been updated.

### Task 4: Publish Chapter 14.5 and reconcile Part IV/book totals

**Files:**
- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `README.md`
- Modify: `scripts/check_site.py`
- Modify: `docs/curriculum/part-04-dependencies.md`
- Modify: `docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md`
- Modify: `docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md`
- Modify: `docs/reviews/2026-07-27-part-04-consistency-review.md`
- Modify: `tests/test_zensical_structure.py`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Register Chapter 14.5**

Add to `mkdocs.yml` immediately after 14.4:

```yaml
- 14.5 怎样为原函数计算准备可靠的求导能力？: chapters/chapter-14/u-04-14-05-derivative-fluency-for-antiderivatives.md
```

Change the Chapter 14 course-map hours to `8 小时（理论 5，应用 3）` and add the same linked title.
Advance the live course-map and README count from 72 to 73 units while keeping Chapter 17 as the
furthest published chapter.

- [ ] **Step 2: Reconcile Part IV and whole-book totals**

Apply these exact final values in both design documents:

```markdown
| 第 14 章 | 5.0 | 3.0 | 8 |
| **第四部** | **26** | **12.5** | **38.5** |
```

In the master table use:

```markdown
| IV | 微分与局部线性化 | 26 | 12.5 | 38.5 |
| V | 积分、累积与数值求积 | 26 | 13.5 | 39.5 |
| **当前总计** |  | **292** | **100** | **392** |
```

Rewrite the adjacent prose to say the approved derivative bridge adds `0.5+1.5=2` hours and the
Part V training expansion adds `0+3.5=3.5` hours, taking the baseline from 386.5 to 392.

- [ ] **Step 3: Update dependency and historical-review records**

Add this row to `docs/curriculum/part-04-dependencies.md`:

```markdown
| `u-04-14-05` | `u-04-14-01`–`04` | 已证求导法则的综合训练、结构识别、定义域检查与第 18 章计算桥梁 |
```

Append a dated addendum to the historical Part IV review. State that the 2026-07-27 review remains
valid for its original 20-unit release snapshot, while the approved 2026-07-28 extension changes the
live Part IV contract to 21 units and 38.5 hours.

- [ ] **Step 4: Add the rendered anchor and update the intermediate 73-unit contracts**

In `scripts/check_site.py`, add:

```python
"chapters/chapter-14/u-04-14-05-derivative-fluency-for-antiderivatives/index.html": [
    "tbl-u-04-14-05-structure-signals",
    "ex-u-04-14-05-nested-chain",
    "ex-u-04-14-05-error-diagnosis",
],
```

Add the same page and anchor expectation to `tests/test_mkdocs_site.py`, with navigation markers:

```python
[
    "md-sidebar",
    "第四部：微分与局部线性化",
    "第 14 章：求导法则、反函数与高阶导数",
]
```

In `tests/test_zensical_structure.py`, require:

```python
self.assertIn("第四部第 17 章，共 73 个学习单元", readme)
```

Use the same count in stale assertions in Chapter 15/17 and Part IV consistency tests until
Chapter 18 is published. Update the Chapter 16 assertion as well. The later publication task will
advance this count to 78.

- [ ] **Step 5: Run and commit the closed Chapter 14.5 increment**

Run:

```bash
python3.12 -m unittest tests.test_chapter_14 tests.test_part_04_consistency tests.test_chapter_15 tests.test_chapter_16 tests.test_chapter_17 tests.test_mkdocs_site tests.test_zensical_structure -v
python3.12 scripts/check_content.py
make verify
```

Expected: all listed tests and the full quality gate pass; strict Zensical build prints
`No issues found`.

Commit:

```bash
git add content/chapters/chapter-14 mkdocs.yml content/course-map.md README.md scripts/check_site.py docs/curriculum/part-04-dependencies.md docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md docs/reviews/2026-07-27-part-04-consistency-review.md tests
git commit -m "docs: add derivative fluency bridge"
```

### Task 5: Lock Chapter 18 with failing contracts

**Files:**
- Create: `tests/test_chapter_18.py`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Define exact units and anchors**

Create `EXPECTED_UNITS`:

```python
EXPECTED_UNITS = [
    ("u-05-18-01", "导数能否反向恢复原函数？", 1.25, 0.25, "antiderivatives"),
    ("u-05-18-02", "复合函数的导数怎样反向产生换元法？", 1.00, 0.50, "substitution"),
    ("u-05-18-03", "乘积法则怎样反向产生分部积分法？", 1.00, 0.50, "integration-by-parts"),
    ("u-05-18-04", "有理函数怎样通过代数分解获得原函数？", 1.00, 0.50, "rational-functions"),
    ("u-05-18-05", "怎样选择积分方法并用求导可靠回验？", 0.25, 1.75, "method-selection"),
]
```

Use:

```python
REQUIRED_ANCHORS = {
    "u-05-18-01": (
        "def-u-05-18-01-antiderivative",
        "thm-u-05-18-01-constant-difference",
        "ex-u-05-18-01-darboux-obstruction",
    ),
    "u-05-18-02": (
        "thm-u-05-18-02-substitution",
        "tbl-u-05-18-02-domain-checks",
    ),
    "u-05-18-03": (
        "thm-u-05-18-03-integration-by-parts",
        "tbl-u-05-18-03-route-selection",
    ),
    "u-05-18-04": (
        "thm-u-05-18-04-partial-fractions",
        "tbl-u-05-18-04-factor-forms",
    ),
    "u-05-18-05": (
        "alg-u-05-18-05-method-selection",
        "tbl-u-05-18-05-verification",
    ),
}
```

- [ ] **Step 2: Add contract tests**

Require:

```python
self.assertEqual(4.5, theory)
self.assertEqual(3.5, applied)
self.assertIn("本章共5个核心单元，8学时（理论4.5，应用3.5）。", guide)
self.assertIn("第 17 章", guide)
self.assertIn("第 19 章", guide)
```

Add boundary checks:

```python
FORBIDDEN_CORE_TERMS = (
    "Riemann 和",
    "Darboux 和",
    "微积分基本定理",
    "Newton–Leibniz",
    "积分上限函数",
    "Lebesgue",
)
```

For 18.5 require at least 12 exercise anchors, at least 14 collapsed answers, and all markers:

```python
(
    "识别结构",
    "选择方法",
    "求导回验",
    "失败路线",
    "没有初等原函数",
)
```

- [ ] **Step 3: Add representative rendered-site expectations**

In `tests/test_mkdocs_site.py`, require Chapter 14.5 and Chapter 18.1/18.5 pages with their exact
anchor lists and navigation markers:

```python
[
    "md-sidebar",
    "第五部：积分、累积与数值求积",
    "第 18 章：原函数与积分方法",
]
```

- [ ] **Step 4: Run the red tests**

Run:

```bash
python3.12 -m unittest tests.test_chapter_18 tests.test_mkdocs_site -v
```

Expected: Chapter 18 failures report missing pages/navigation/anchors; existing site-checker tests
remain green.

- [ ] **Step 5: Commit the red Chapter 18 contract**

```bash
git add tests/test_chapter_18.py tests/test_mkdocs_site.py
git commit -m "test: lock chapter 18 antiderivative contract"
```

### Task 6: Create the Chapter 18 guide and Part V dependency map

**Files:**
- Create: `content/chapters/chapter-18/index.md`
- Create: `docs/curriculum/part-05-dependencies.md`

- [ ] **Step 1: Write the chapter guide**

Use:

```markdown
---
title: 第 18 章：原函数与积分方法
---

# 第 18 章：原函数与积分方法 {#chapter-18}
```

State:

```markdown
本章共5个核心单元，8学时（理论4.5，应用3.5）。
```

List the five exact linked titles from Task 5. Include this proof ladder:

```math
\text{导数规则}
\longrightarrow
\text{原函数族}
\longrightarrow
\text{换元与分部积分}
\longrightarrow
\text{有理函数分解}
\longrightarrow
\text{方法选择与求导回验}.
```

State that Chapter 17 supplies derivative structure, Chapter 14.5 supplies fluency, and Chapter 19
will independently define Riemann integration. Explicitly forbid using the fundamental theorem,
Riemann sums, or definite-integral properties in Chapter 18 proofs.

- [ ] **Step 2: Write all 22 Part V dependency rows**

Use the exact unit IDs from the approved design:

```text
u-05-18-01 ... u-05-18-05
u-05-19-01 ... u-05-19-04
u-05-20-01 ... u-05-20-04
u-05-21-01 ... u-05-21-04
u-05-22-01 ... u-05-22-05
```

For every row name direct dependencies and one unique output. Mark Chapter 18 as the current
publication boundary and Chapters 19–22 as locked future contracts. The first five dependencies are:

| Unit | Direct dependency | Unique output |
|---|---|---|
| `u-05-18-01` | `u-04-15-02`, `u-04-14-05` | antiderivative definition, constant difference, Darboux obstruction |
| `u-05-18-02` | `u-04-14-02`, `u-05-18-01` | substitution derived from chain rule |
| `u-05-18-03` | `u-04-14-01`, `u-05-18-01` | integration by parts derived from product rule |
| `u-05-18-04` | `u-05-18-01`–`03`, higher algebra | rational-function reduction and partial fractions |
| `u-05-18-05` | `u-05-18-01`–`04` | mixed method selection and derivative verification |

- [ ] **Step 3: Run structural checks**

Run:

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_18 -v
```

Expected: content check passes; Chapter 18 tests fail only for the five missing units and
publication registration.

- [ ] **Step 4: Commit the guide and dependency map**

```bash
git add content/chapters/chapter-18/index.md docs/curriculum/part-05-dependencies.md
git commit -m "docs: establish chapter 18 learning arc"
```

### Task 7: Write Unit 18.1 — antiderivatives and existence boundaries

**Files:**
- Create: `content/chapters/chapter-18/u-05-18-01-antiderivatives.md`

- [ ] **Step 1: Create metadata**

Use:

```yaml
title: 导数能否反向恢复原函数？
unit_id: u-05-18-01
hours: {theory: 1.25, applied: 0.25}
difficulty: 3
prerequisites:
  book: [u-04-14-05, u-04-15-02]
  higher_algebra: [恒等变形, 参数与常数]
  analytic_geometry: [函数图像, 区间与连通分支]
  python: [函数求值, 数值点检]
capabilities: [definition, proof, counterexample, verification]
learning_goals: [定义原函数, 证明原函数族相差常数, 判断区间作用域, 识别存在与表示的边界]
content_standard: 2
```

- [ ] **Step 2: Write the complete theory**

Include:

- `{#def-u-05-18-01-antiderivative}`: \(F'=f\) on an interval \(I\);
- notation \(\int f(x)\,dx=F(x)+C\) as an antiderivative-family notation, not a limit;
- `{#thm-u-05-18-01-constant-difference}`: prove by the zero-derivative constant theorem;
- disconnected-domain warning using \(1/x\) on \(\mathbb R\setminus\{0\}\);
- a basic table whose entries are verified by differentiation;
- `{#ex-u-05-18-01-darboux-obstruction}`: the sign-step function has no antiderivative because
  derivatives have the Darboux property;
- explicit statement that Darboux is necessary, not sufficient in this course.

Use complete examples for recovering antiderivatives of \(3x^2-2x+1\) and for the Darboux
obstruction.

- [ ] **Step 3: Add checks and exercises**

Use five exercises covering a polynomial, \(1/x\) on separate intervals, \(e^x\), \(\cos x\), and a
false claim that equal derivatives imply one global constant on a disconnected domain. Give seven
collapsed answers total.

- [ ] **Step 4: Run and commit**

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_18 -v
git add content/chapters/chapter-18/u-05-18-01-antiderivatives.md
git commit -m "docs: establish antiderivatives and boundaries"
```

Expected: content passes; Chapter 18 failures no longer mention Unit 18.1 content or anchors.

### Task 8: Write Unit 18.2 — substitution

**Files:**
- Create: `content/chapters/chapter-18/u-05-18-02-substitution.md`

- [ ] **Step 1: Create metadata and theorem contract**

Use prerequisites `[u-04-14-02, u-04-14-05, u-05-18-01]`, hours `1.00+0.50`, and capabilities
`[proof, substitution, domain_analysis, verification]`.

At `{#thm-u-05-18-02-substitution}`, state:

```math
F'=f \text{ on } J,\quad g:I\to J \text{ differentiable}
\quad\Longrightarrow\quad
\int f(g(x))g'(x)\,dx=F(g(x))+C
```

Prove it directly by the chain rule.

- [ ] **Step 2: Write domain checks and examples**

At `{#tbl-u-05-18-02-domain-checks}`, cover range inclusion \(g(I)\subseteq J\), logarithm absolute
values, square-root branches, and interval-by-interval constants.

Use examples:

- \(\int 2x\cos(x^2)\,dx\);
- \(\int x/(1+x^2)\,dx\), with \(\frac12\log(1+x^2)+C\);
- an error diagnosis where the inner derivative is missing.

- [ ] **Step 3: Add exercises and answers**

Five exercises must include linear substitution, \(x e^{x^2}\), trigonometric composition,
\(1/(ax+b)\), and a domain-sensitive square-root example. Include seven collapsed answers.

- [ ] **Step 4: Run and commit**

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_18 -v
git add content/chapters/chapter-18/u-05-18-02-substitution.md
git commit -m "docs: derive substitution from the chain rule"
```

### Task 9: Write Unit 18.3 — integration by parts

**Files:**
- Create: `content/chapters/chapter-18/u-05-18-03-integration-by-parts.md`

- [ ] **Step 1: Create metadata and derive the formula**

Use prerequisites `[u-04-14-01, u-04-14-05, u-05-18-01]`, hours `1.00+0.50`, and at
`{#thm-u-05-18-03-integration-by-parts}` derive:

```math
\int u(x)v'(x)\,dx=u(x)v(x)-\int u'(x)v(x)\,dx.
```

State that the formula is an identity, not a guarantee of simplification.

- [ ] **Step 2: Write the route-selection table and examples**

At `{#tbl-u-05-18-03-route-selection}`, compare algebraic × exponential, algebraic × trigonometric,
logarithmic, inverse-trigonometric, and cyclic cases.

Use complete examples:

- \(\int xe^x\,dx\);
- \(\int \log x\,dx\) on \(x>0\);
- \(\int e^x\cos x\,dx\), solving the cyclic identity without illegal cancellation.

- [ ] **Step 3: Add exercises and answers**

Five exercises cover \(x\sin x\), \(x^2e^x\), \(\arctan x\), repeated parts, and a poor split that
increases complexity. Include seven collapsed answers.

- [ ] **Step 4: Run and commit**

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_18 -v
git add content/chapters/chapter-18/u-05-18-03-integration-by-parts.md
git commit -m "docs: derive integration by parts"
```

### Task 10: Write Unit 18.4 — rational functions

**Files:**
- Create: `content/chapters/chapter-18/u-05-18-04-rational-functions.md`

- [ ] **Step 1: Create metadata and algebraic reduction**

Use prerequisites `[u-05-18-01, u-05-18-02, u-05-18-03]`, higher-algebra prerequisites
`[多项式除法, 因式分解, 待定系数法, 配方]`, and hours `1.00+0.50`.

At `{#thm-u-05-18-04-partial-fractions}`, state the course-scope real partial-fraction form after
proper-fraction reduction. Do not claim or prove the full abstract algebra theorem.

- [ ] **Step 2: Write factor forms and examples**

At `{#tbl-u-05-18-04-factor-forms}`, include:

- distinct linear factors \(A/(x-a)\);
- repeated linear factors \(A_k/(x-a)^k\);
- irreducible quadratic factors \((Ax+B)/(x^2+px+q)^k\);
- polynomial part after long division.

Use complete examples:

- \(\int (3x+5)/(x^2+x-2)\,dx\);
- \(\int dx/(x^2+1)\);
- a repeated-factor example containing \(1/(x-1)^2\).

- [ ] **Step 3: Add exercises and answers**

Five exercises cover improper-to-proper reduction, two distinct linear factors, a repeated factor,
an irreducible quadratic, and derivative verification of a decomposed result. Include at least seven
collapsed answers.

- [ ] **Step 4: Run and commit**

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_18 -v
git add content/chapters/chapter-18/u-05-18-04-rational-functions.md
git commit -m "docs: add rational antiderivative methods"
```

### Task 11: Write Unit 18.5 — mixed method selection and verification

**Files:**
- Create: `content/chapters/chapter-18/u-05-18-05-method-selection.md`

- [ ] **Step 1: Create metadata and the decision process**

Use hours `0.25+1.75`, prerequisites `[u-04-14-05, u-05-18-01, u-05-18-02, u-05-18-03,
u-05-18-04]`, and capabilities `[method_selection, mixed_computation, error_diagnosis,
derivative_verification]`.

At `{#alg-u-05-18-05-method-selection}`, write:

```text
1. Simplify algebraically and determine the working interval.
2. Look for a direct derivative-table match.
3. Look for an inner function together with its derivative.
4. Look for a product whose derivative complexity decreases under parts.
5. For rational functions, divide and decompose.
6. If no elementary route is justified, say so without claiming nonexistence.
7. Differentiate the proposed result on the stated interval.
```

- [ ] **Step 2: Write the verification table and mixed examples**

At `{#tbl-u-05-18-05-verification}`, distinguish algebraic equality, domain equality, derivative
equality, arbitrary constants, and numerical spot checks.

Use two complete examples:

- \(\int x^3 e^{x^2}\,dx\), requiring algebra plus substitution and then derivative verification;
- \(\int x\log(1+x^2)\,dx\), requiring substitution plus parts.

Discuss \(e^{-x^2}\) only as an example where no elementary antiderivative is supplied; do not
attempt to prove non-elementarity.

- [ ] **Step 3: Add 12 ungrouped exercises and full answers**

Use anchors `pr-u-05-18-05-01` through `pr-u-05-18-05-12`, in a mixed order:

1. direct table;
2. algebraic simplification;
3. substitution;
4. parts;
5. rational partial fractions;
6. substitution followed by parts;
7. repeated parts;
8. domain-sensitive logarithm;
9. diagnose a missing chain factor;
10. diagnose a lost arbitrary constant;
11. compare two equivalent antiderivatives on one interval;
12. explain why “software returned no elementary form” is not “no antiderivative exists”.

Each exercise gets a complete adjacent answer. Combined with two example and two immediate-check
answers, the page must have at least 16 collapsed answers.

- [ ] **Step 4: Run the full Chapter 18 content contract and commit**

```bash
python3.12 scripts/check_content.py
python3.12 -m unittest tests.test_chapter_18 -v
git add content/chapters/chapter-18/u-05-18-05-method-selection.md
git commit -m "docs: add mixed antiderivative practice"
```

Expected: all content and mathematics assertions pass; only publication-surface assertions may still
fail.

### Task 12: Publish Chapter 18 and advance the release surface

**Files:**
- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `README.md`
- Modify: `scripts/check_site.py`
- Modify: `tests/test_zensical_structure.py`
- Modify: `tests/test_chapter_15.py`
- Modify: `tests/test_chapter_16.py`
- Modify: `tests/test_chapter_17.py`
- Modify: `tests/test_part_04_consistency.py`

- [ ] **Step 1: Add Part V navigation**

Add:

```yaml
- 第五部：积分、累积与数值求积:
    - 第 18 章：原函数与积分方法:
        - 本章导学: chapters/chapter-18/index.md
        - 18.1 导数能否反向恢复原函数？: chapters/chapter-18/u-05-18-01-antiderivatives.md
        - 18.2 复合函数的导数怎样反向产生换元法？: chapters/chapter-18/u-05-18-02-substitution.md
        - 18.3 乘积法则怎样反向产生分部积分法？: chapters/chapter-18/u-05-18-03-integration-by-parts.md
        - 18.4 有理函数怎样通过代数分解获得原函数？: chapters/chapter-18/u-05-18-04-rational-functions.md
        - 18.5 怎样选择积分方法并用求导可靠回验？: chapters/chapter-18/u-05-18-05-method-selection.md
```

- [ ] **Step 2: Update course map and README**

Use:

```markdown
当前已发布第一至第四部及第五部第 18 章，共 78 个学习单元。
```

Add the Part V heading, guiding question, Chapter 18 guide link, `8 小时（理论 4.5，应用 3.5）`,
and all five unit links. Change the future route to say Chapter 19 and later are not yet published.

- [ ] **Step 3: Add rendered anchors and navigation markers**

In `scripts/check_site.py`, require:

```python
"chapters/chapter-14/u-04-14-05-derivative-fluency-for-antiderivatives/index.html": [
    "tbl-u-04-14-05-structure-signals",
    "ex-u-04-14-05-nested-chain",
    "ex-u-04-14-05-error-diagnosis",
],
"chapters/chapter-18/u-05-18-01-antiderivatives/index.html": [
    "def-u-05-18-01-antiderivative",
    "thm-u-05-18-01-constant-difference",
    "ex-u-05-18-01-darboux-obstruction",
],
"chapters/chapter-18/u-05-18-05-method-selection/index.html": [
    "alg-u-05-18-05-method-selection",
    "tbl-u-05-18-05-verification",
],
```

Give Chapter 18 pages the exact Part V and Chapter 18 navigation markers from Task 5.

- [ ] **Step 4: Advance every release-count assertion to 78**

Search:

```bash
rg -n "72 个|73 个|第 18 章及以后|17 章，共" README.md content tests
```

Replace only assertions describing the live publication surface. Do not rewrite historical review
snapshots that explicitly say they describe the earlier release.

- [ ] **Step 5: Run publication checks and commit**

```bash
python3.12 -m unittest tests.test_chapter_14 tests.test_chapter_18 tests.test_mkdocs_site tests.test_zensical_structure tests.test_part_04_consistency -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: all commands pass; Zensical prints `No issues found`.

Commit:

```bash
git add mkdocs.yml content/course-map.md README.md scripts/check_site.py tests
git commit -m "docs: publish chapter 18 antiderivative units"
```

### Task 13: Perform the combined mathematical review and final verification

**Files:**
- Create: `docs/reviews/2026-07-28-chapter-14-05-and-chapter-18-review.md`
- Modify only if review finds a defect: files in Tasks 2–12

- [ ] **Step 1: Review Chapter 14.5 against its boundary**

Record pass/fail evidence for:

- every derivative computation has its working domain;
- nested chain factors are complete;
- inverse-function branches and logarithm conditions are explicit;
- the page trains but does not state substitution or integration-by-parts formulas;
- all 12 exercises and answers are mathematically correct.

- [ ] **Step 2: Review Chapter 18 unit by unit**

Record a six-row matrix for Chapter 14.5 and Units 18.1–18.5. Columns:

```markdown
| 单元 | 先备 | 定义/定理 | 证明假设 | 例题/练习 | 边界 | 结果 |
```

Explicitly verify:

- “two antiderivatives differ by a constant” is interval-scoped;
- disconnected domains allow different constants;
- Darboux is used only as a necessary obstruction;
- substitution includes the inner derivative and range/domain checks;
- integration by parts is not promised to simplify every integral;
- partial fractions first reduces improper rational functions;
- \(e^{-x^2}\) is not used to assert an unproved non-elementarity theorem;
- no core proof uses Riemann integration, the fundamental theorem, or Newton–Leibniz.

- [ ] **Step 3: Reconcile counts and hours**

Record:

```text
Part IV: 21 units, theory 26, applied 12.5, total 38.5.
Chapter 18: 5 units, theory 4.5, applied 3.5, total 8.
Published: 78 units through Chapter 18.
Whole-book baseline: theory 292, applied 100, total 392.
```

- [ ] **Step 4: Run the full quality gate**

Run:

```bash
make verify
```

Expected: the enlarged test suite passes with 0 failures, content check exits 0, strict Zensical
build prints `No issues found`, and site check exits 0.

- [ ] **Step 5: Inspect generated representative pages**

Confirm these files exist:

```text
site/chapters/chapter-14/u-04-14-05-derivative-fluency-for-antiderivatives/index.html
site/chapters/chapter-18/index.html
site/chapters/chapter-18/u-05-18-01-antiderivatives/index.html
site/chapters/chapter-18/u-05-18-05-method-selection/index.html
```

Confirm the stable anchors from Task 12 and Chinese navigation titles appear in the generated HTML.

- [ ] **Step 6: Commit the review and any verified corrections**

```bash
git add docs/reviews/2026-07-28-chapter-14-05-and-chapter-18-review.md
git commit -m "docs: verify derivative bridge and chapter 18"
```

- [ ] **Step 7: Stop at the approved boundary**

Run:

```bash
git status --short --branch
git log -12 --oneline
```

Expected: clean worktree, the implementation commits are visible, and no Chapter 19 content page
exists. Report Chapter 18 as the stopping point; do not push or begin Chapter 19 without a new user
instruction.
