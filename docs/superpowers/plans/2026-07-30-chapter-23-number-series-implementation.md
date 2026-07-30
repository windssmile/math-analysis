# Chapter 23 Number Series Convergence and Positive-Term Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Chapter 23 as five rigorous self-study units, establish the 24-unit/42-hour Part VI dependency contract, and add tested certificates for geometric and \(p\)-series truncation.

**Architecture:** Introduce Part VI without creating Chapter 24–27 placeholders. Lock metadata, proof, training, algorithm, publication, and rendered-anchor contracts in failing tests; write the chapter in dependency order; publish only after the complete Chapter 23 contract passes. Keep signed-series cancellation, rearrangement, Cauchy products, function series, uniform convergence, and power series outside Chapter 23.

**Tech Stack:** Markdown with YAML front matter and MathJax, Python 3.12 standard library, frozen dataclasses, `unittest`, PyYAML, Zensical/MkDocs, existing content and site validation scripts.

---

## Scope and file map

### Create

- `content/chapters/chapter-23/index.md` — Chapter 23 route, prerequisites, positive-series decision path, outputs, and Chapter 24 boundary.
- `content/chapters/chapter-23/u-06-23-01-partial-sums.md` — partial sums, convergence, remainder, necessary condition, geometric and telescoping baselines.
- `content/chapters/chapter-23/u-06-23-02-cauchy-tail.md` — series Cauchy criterion, finite tails, epsilon budgets, and observed-difference boundary.
- `content/chapters/chapter-23/u-06-23-03-comparison-tests.md` — positive-series monotonicity, direct/limit comparison, and tail bounds.
- `content/chapters/chapter-23/u-06-23-04-ratio-root-tests.md` — ratio/root tests, limsup forms, critical-value failure, and method comparison.
- `content/chapters/chapter-23/u-06-23-05-integral-condensation.md` — integral and condensation tests, \(p\)-series/logarithmic families, and certified truncation.
- `docs/curriculum/part-06-dependencies.md` — all 24 approved Part VI units, interfaces, hours, and current Chapter 23 publication boundary.
- `src/mathbook_examples/series.py` — the only executable geometric and \(p\)-series certificate implementation.
- `tests/test_series.py` — algorithm results, validation, error-bound, and status contracts.
- `tests/test_chapter_23.py` — metadata, mathematics, training, scope, publication, and anchor contracts.
- `docs/reviews/2026-07-30-chapter-23-consistency-review.md` — mathematical, pedagogical, publication, and engineering audit.

### Modify

- `README.md` — release boundary becomes Part VI Chapter 23 and 103 learning units.
- `content/course-map.md` — add Part VI problem arc, Chapter 23 links, 8.5 hours, and the unrendered Chapter 24–27 route in prose only.
- `mkdocs.yml` — add Part VI and the Chapter 23 guide plus five pages after Part V.
- `scripts/check_site.py` — require representative Chapter 23 anchors and Part VI sidebar markers.
- `tests/test_chapter_15.py`
- `tests/test_chapter_16.py`
- `tests/test_chapter_17.py`
- `tests/test_chapter_18.py`
- `tests/test_chapter_19.py`
- `tests/test_chapter_20.py`
- `tests/test_chapter_21.py`
- `tests/test_chapter_22.py`
- `tests/test_part_04_consistency.py`
- `tests/test_zensical_structure.py`
- `tests/test_mkdocs_site.py`

The master 12-part design keeps its approved Part VI 42-hour design in
`docs/superpowers/specs/2026-07-30-part-06-series-approximation-design.md`.
Do not rewrite historical chapter specifications. Do not change the master whole-book total until Part VI closes, as required by the approved Part VI design.

## Locked Chapter 23 registry

```python
EXPECTED_UNITS = [
    (
        "u-06-23-01",
        "无限求和怎样由部分和定义？",
        1.25,
        0.25,
        "partial-sums",
        7,
        9,
    ),
    (
        "u-06-23-02",
        "Cauchy 尾部判据怎样控制无限求和？",
        1.50,
        0.25,
        "cauchy-tail",
        7,
        9,
    ),
    (
        "u-06-23-03",
        "正项级数怎样通过比较判断收敛？",
        1.25,
        0.50,
        "comparison-tests",
        8,
        10,
    ),
    (
        "u-06-23-04",
        "局部增长率怎样产生比值与根值判别？",
        1.25,
        0.50,
        "ratio-root-tests",
        8,
        10,
    ),
    (
        "u-06-23-05",
        "积分与凝聚怎样提供判别和余项证书？",
        1.25,
        0.50,
        "integral-condensation",
        10,
        13,
    ),
]
```

The exact totals are 5 units, 6.5 theory hours, 2 application hours, 8.5 hours, 40 exercises, and 51 folded answers. Each page uses `content_standard: 2`.

### Task 1: Lock Chapter 23, algorithm, and rendered-site contracts in failing tests

**Files:**

- Create: `tests/test_chapter_23.py`
- Create: `tests/test_series.py`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Write the Chapter 23 registry and metadata test**

Create `tests/test_chapter_23.py` with:

```python
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-23"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-06-dependencies.md"

EXPECTED_UNITS = [
    ("u-06-23-01", "无限求和怎样由部分和定义？", 1.25, 0.25, "partial-sums", 7, 9),
    ("u-06-23-02", "Cauchy 尾部判据怎样控制无限求和？", 1.50, 0.25, "cauchy-tail", 7, 9),
    ("u-06-23-03", "正项级数怎样通过比较判断收敛？", 1.25, 0.50, "comparison-tests", 8, 10),
    ("u-06-23-04", "局部增长率怎样产生比值与根值判别？", 1.25, 0.50, "ratio-root-tests", 8, 10),
    ("u-06-23-05", "积分与凝聚怎样提供判别和余项证书？", 1.25, 0.50, "integral-condensation", 10, 13),
]

REQUIRED_ANCHORS = {
    "u-06-23-01": (
        "def-u-06-23-01-series-convergence",
        "def-u-06-23-01-remainder",
        "thm-u-06-23-01-term-necessary",
        "ex-u-06-23-01-geometric",
        "ex-u-06-23-01-telescoping",
    ),
    "u-06-23-02": (
        "thm-u-06-23-02-cauchy-tail",
        "ex-u-06-23-02-harmonic-failure",
        "ex-u-06-23-02-epsilon-budget",
        "tbl-u-06-23-02-evidence-boundary",
    ),
    "u-06-23-03": (
        "thm-u-06-23-03-positive-monotone",
        "thm-u-06-23-03-direct-comparison",
        "thm-u-06-23-03-limit-comparison",
        "cor-u-06-23-03-tail-bound",
    ),
    "u-06-23-04": (
        "thm-u-06-23-04-ratio-test",
        "thm-u-06-23-04-root-test",
        "thm-u-06-23-04-limsup-forms",
        "ex-u-06-23-04-critical-one",
    ),
    "u-06-23-05": (
        "thm-u-06-23-05-integral-test",
        "cor-u-06-23-05-integral-tail-bounds",
        "thm-u-06-23-05-cauchy-condensation",
        "ex-u-06-23-05-p-series",
        "ex-u-06-23-05-logarithmic-family",
        "alg-u-06-23-05-certified-truncation",
    ),
}


def unit_path(unit: tuple[str, str, float, float, str, int, int]) -> Path:
    unit_id, _title, _theory, _applied, suffix, _exercises, _answers = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text
```

Implement `test_units_have_final_metadata_hours_anchors_and_training` following the Chapter 22 parser. Assert:

```python
self.assertEqual(6.5, theory)
self.assertEqual(2.0, applied)
self.assertEqual(40, total_exercises)
self.assertEqual(51, total_answers)
```

Require at least two `### 例 ` headings and two `### 即时检验 ` headings per page, exact exercise/answer counts, every locked anchor, exact metadata, and one H1 anchor matching the unit ID.

- [ ] **Step 2: Add focused mathematical and scope tests**

Add these contracts to `ChapterTwentyThreeTests`:

```python
def test_chapter_guide_lists_units_hours_route_and_boundaries(self) -> None:
    guide = self.required_text(CHAPTER / "index.md")
    self.assertIn("本章共5个核心单元，8.5学时（理论6.5，应用2）。", guide)
    for marker in (
        "部分和",
        "Cauchy 尾部",
        "正项级数",
        "比较判别",
        "比值与根值",
        "积分与凝聚",
        "余项证书",
        "第 22 章",
        "第 24 章",
    ):
        self.assertIn(marker, guide)
    for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
        self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

def test_unit_one_does_not_confuse_terms_and_partial_sums(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[0]))
    for marker in (
        "部分和",
        "通项趋于零只是必要条件",
        "有限项",
        "余项",
        "几何级数",
        "伸缩级数",
    ):
        self.assertIn(marker, text)
    self.assertIn(r"\sum_{n=1}^{\infty}\frac1n", text)

def test_unit_two_uses_arbitrary_finite_tails(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[1]))
    for marker in (
        "任意有限尾段",
        "n>m",
        "实数完备性",
        "相邻部分和差",
        "不能证明收敛",
    ):
        self.assertIn(marker, text)

def test_unit_three_keeps_both_comparison_directions(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[2]))
    for marker in (
        "最终成立",
        "上方级数收敛",
        "下方级数发散",
        "正有限极限",
        "L=0",
        r"L=\infty",
        "余项上界",
    ):
        self.assertIn(marker, text)

def test_unit_four_keeps_critical_value_and_limsup_boundaries(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[3]))
    for marker in (
        "临界值 1",
        "无结论",
        "上极限",
        "最终几何控制",
        "比值极限不存在",
        "根值判别",
    ):
        self.assertIn(marker, text)

def test_unit_five_requires_positive_decreasing_integral_model(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[4]))
    for marker in (
        "最终非负",
        "单调递减",
        "积分判别",
        "Cauchy 凝聚",
        "尾项上下界",
        "截断预算",
        "调用者已经证明",
    ):
        self.assertIn(marker, text)
    self.assertIn(r"\sum_{n=1}^{\infty}\frac1{n^p}", text)
```

Check core text before `## 常见误区与后续` against:

```python
FORBIDDEN_CORE_TERMS = (
    "交错级数判别",
    "Riemann 重排",
    "Cauchy 乘积",
    "Mertens 定理",
    "函数项级数",
    "一致收敛",
    "幂级数",
    "Fourier 级数",
    "Lebesgue 积分",
)
```

Boundary notes may name Chapter 24 and later topics.

- [ ] **Step 3: Write failing series-certificate tests**

Create `tests/test_series.py`:

```python
from dataclasses import FrozenInstanceError
import math
import unittest

from mathbook_examples.series import (
    SeriesCertificate,
    geometric_series_certificate,
    p_series_integral_certificate,
)


class GeometricSeriesCertificateTests(unittest.TestCase):
    def test_returns_smallest_certified_term_count(self) -> None:
        result = geometric_series_certificate(
            first_term=1.0,
            ratio=0.5,
            tolerance=0.01,
            max_terms=100,
        )
        self.assertEqual("certified", result.status)
        self.assertEqual(8, result.terms_used)
        self.assertLessEqual(result.error_bound, 0.01)
        self.assertAlmostEqual(2.0 - 2.0**-7, result.approximation)
        self.assertIn("|r| < 1", result.assumptions)

    def test_reports_budget_unmet_without_false_certificate(self) -> None:
        result = geometric_series_certificate(1.0, 0.9, 1e-12, 4)
        self.assertEqual("budget_unmet", result.status)
        self.assertEqual(4, result.terms_used)
        self.assertGreater(result.error_bound, 1e-12)

    def test_rejects_invalid_geometric_inputs(self) -> None:
        invalid = (
            (math.nan, 0.5, 0.1, 10),
            (1.0, 1.0, 0.1, 10),
            (1.0, -1.0, 0.1, 10),
            (1.0, 0.5, 0.0, 10),
            (1.0, 0.5, 0.1, 0),
        )
        for args in invalid:
            with self.subTest(args=args), self.assertRaises(ValueError):
                geometric_series_certificate(*args)


class PSeriesCertificateTests(unittest.TestCase):
    def test_integral_tail_bound_certifies_requested_tolerance(self) -> None:
        result = p_series_integral_certificate(
            exponent=2.0,
            tolerance=0.01,
            max_terms=1_000,
        )
        self.assertEqual("certified", result.status)
        self.assertEqual(100, result.terms_used)
        self.assertLessEqual(result.error_bound, 0.01)
        self.assertIn("p > 1", result.assumptions)

    def test_budget_unmet_keeps_the_proved_bound(self) -> None:
        result = p_series_integral_certificate(2.0, 1e-6, 100)
        self.assertEqual("budget_unmet", result.status)
        self.assertAlmostEqual(0.01, result.error_bound)

    def test_rejects_nonconvergent_or_nonfinite_inputs(self) -> None:
        for exponent in (1.0, 0.5, math.inf, math.nan):
            with self.subTest(exponent=exponent), self.assertRaises(ValueError):
                p_series_integral_certificate(exponent, 0.01, 100)

    def test_result_is_frozen(self) -> None:
        result = p_series_integral_certificate(2.0, 0.1, 100)
        with self.assertRaises(FrozenInstanceError):
            result.status = "changed"
```

- [ ] **Step 4: Add a failing rendered-site contract**

In `tests/test_mkdocs_site.py`, add representative expectations:

```python
def test_checks_chapter_twenty_three_cauchy_and_integral_pages(self) -> None:
    for page, anchors in {
        "chapters/chapter-23/u-06-23-02-cauchy-tail/index.html": (
            "thm-u-06-23-02-cauchy-tail",
            "tbl-u-06-23-02-evidence-boundary",
        ),
        "chapters/chapter-23/u-06-23-05-integral-condensation/index.html": (
            "thm-u-06-23-05-integral-test",
            "alg-u-06-23-05-certified-truncation",
        ),
    }.items():
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        for anchor in anchors:
            self.assertIn(anchor, REQUIRED_RENDERED_ANCHORS[page])
        self.assertEqual(
            [
                "md-sidebar",
                "第六部：无穷级数与函数逼近",
                "第 23 章：数项级数的收敛与正项判别",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )
```

- [ ] **Step 5: Run the focused tests and verify red**

Run:

```bash
python3.12 -m unittest tests.test_chapter_23 tests.test_series tests.test_mkdocs_site -v
```

Expected: failures for missing Chapter 23 files, missing `mathbook_examples.series`, and missing rendered-site mappings. Do not weaken assertions.

- [ ] **Step 6: Commit the red contracts**

```bash
git add tests/test_chapter_23.py tests/test_series.py tests/test_mkdocs_site.py
git commit -m "test: lock chapter 23 series contracts"
```

### Task 2: Establish the Part VI dependency map and Chapter 23 guide

**Files:**

- Create: `docs/curriculum/part-06-dependencies.md`
- Create: `content/chapters/chapter-23/index.md`

- [ ] **Step 1: Write the Part VI dependency map**

Create `docs/curriculum/part-06-dependencies.md` with these exact top-level statements:

```markdown
# 第六部依赖与职责图谱

**范围：** 第 23–27 章，24 个核心单元，42 学时

**当前发布边界：第 23 章。** 当前已发布第六部 5 个核心单元、8.5 学时；第 24–27 章
只保留依赖路线，在对应章节正式撰写前不创建空白页面。
```

Include:

- the Part V input interface;
- separate number-series and function-series stages;
- all 24 rows from Section 12 of the approved Part VI design;
- chapter totals `5/6.5/2/8.5`, `5/7.5/2/9.5`, `5/7/2/9`, `5/6/2/8`, `4/3.5/3.5/7`;
- the unique-responsibility boundaries;
- a current-publication table that distinguishes `5/8.5` published from `24/42` approved.

- [ ] **Step 2: Write the Chapter 23 guide**

Create `content/chapters/chapter-23/index.md` with:

```markdown
---
title: 第 23 章：数项级数的收敛与正项判别
---

# 第 23 章：数项级数的收敛与正项判别 {#chapter-23}
```

The guide must:

- state the exact 5-unit/8.5-hour total;
- link each locked unit exactly once;
- derive the route
  `部分和 → Cauchy 尾部 → 正项比较 → 比值与根值 → 积分与凝聚 → 余项证书`;
- explain the inheritance from Chapter 22 without using improper-integral tests as proofs of series tests;
- distinguish theorem conditions, observed finite behavior, and error certificates;
- state that Chapter 24 introduces sign cancellation, rearrangement, and products;
- state that function series begin only in Chapter 25;
- include ten chapter-entry or chapter-exit questions.

- [ ] **Step 3: Run the guide and dependency tests**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_chapter_guide_lists_units_hours_route_and_boundaries \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_dependency_map_and_publication_scope -v
```

Expected: guide route passes; publication checks remain red until Task 8.

- [ ] **Step 4: Commit the Part VI shell**

```bash
git add docs/curriculum/part-06-dependencies.md content/chapters/chapter-23/index.md
git commit -m "docs: establish part 6 and chapter 23 route"
```

### Task 3: Write Unit 23.1 — partial sums, remainder, and baseline examples

**Files:**

- Create: `content/chapters/chapter-23/u-06-23-01-partial-sums.md`

- [ ] **Step 1: Confirm the Unit 23.1 contract is red**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_unit_one_does_not_confuse_terms_and_partial_sums -v
```

Expected: FAIL because the page is missing.

- [ ] **Step 2: Create exact front matter and learning contract**

Use:

```yaml
---
title: 无限求和怎样由部分和定义？
unit_id: u-06-23-01
hours: {theory: 1.25, applied: 0.25}
difficulty: 3
prerequisites:
  book: [u-02-05-01, u-02-06-01, u-02-07-01]
  higher_algebra: [有限求和, 等比数列, 部分分式]
  analytic_geometry: []
  python: [有限循环仅作观察]
capabilities: [series_definition, partial_sums, remainder, geometric_series, telescoping_series]
learning_goals: [用部分和定义无穷级数, 区分通项与部分和, 证明通项趋零的必要性, 计算几何与伸缩级数]
content_standard: 2
---

# 无限求和怎样由部分和定义？ {#u-06-23-01}
```

- [ ] **Step 3: Write the proof core**

Include these anchored sections:

```markdown
### 数项级数的收敛 {#def-u-06-23-01-series-convergence}
### 余项与截断误差 {#def-u-06-23-01-remainder}
### 收敛级数的通项必趋于零 {#thm-u-06-23-01-term-necessary}
### 例 1：几何级数 {#ex-u-06-23-01-geometric}
### 例 2：伸缩级数 {#ex-u-06-23-01-telescoping}
```

Prove `a_n = S_n - S_{n-1} -> 0`; use the harmonic series to refute the converse; prove finite insertion/deletion and finite linear combinations via partial sums; state remainder only after convergence is known.

- [ ] **Step 4: Add training and answers**

Add at least two immediate checks, seven exercises with anchors
`pr-u-06-23-01-01` through `-07`, and nine folded answers. Cover:

- converting notation to partial sums;
- geometric convergence for positive and negative ratios;
- telescoping after partial fractions;
- divergence by nonzero term limit;
- harmonic divergence deferred to Unit 23.2 but clearly identified;
- finite-term changes;
- a diagnosis of illegal infinite algebra.

- [ ] **Step 5: Run Unit 23.1 and content validation**

Run:

```bash
python3.12 -m unittest tests.test_chapter_23 -v
python3.12 scripts/check_content.py
```

Expected: Unit 23.1 assertions pass; missing Units 23.2–23.5 remain red; content validation reports no structural issue for Unit 23.1.

- [ ] **Step 6: Commit Unit 23.1**

```bash
git add content/chapters/chapter-23/u-06-23-01-partial-sums.md
git commit -m "docs: define number series through partial sums"
```

### Task 4: Write Unit 23.2 — the series Cauchy tail criterion

**Files:**

- Create: `content/chapters/chapter-23/u-06-23-02-cauchy-tail.md`

- [ ] **Step 1: Confirm the Unit 23.2 contract is red**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_unit_two_uses_arbitrary_finite_tails -v
```

Expected: FAIL because the page is missing.

- [ ] **Step 2: Create metadata**

Use `unit_id: u-06-23-02`, hours `{theory: 1.5, applied: 0.25}`, difficulty `4`,
book prerequisites `[u-02-08-02, u-06-23-01]`, capabilities
`[series_cauchy_criterion, finite_tail_control, epsilon_budget, evidence_boundary]`,
and `content_standard: 2`.

- [ ] **Step 3: Write the complete Cauchy proof**

Include:

```markdown
### 级数的 Cauchy 尾部判据 {#thm-u-06-23-02-cauchy-tail}
### 例 1：调和级数为何不满足尾部判据 {#ex-u-06-23-02-harmonic-failure}
### 例 2：从尾部上界反解指标 {#ex-u-06-23-02-epsilon-budget}
### 证据层级对照 {#tbl-u-06-23-02-evidence-boundary}
```

Prove equivalence with the Cauchy property of partial sums. In the harmonic example choose \(n=2m\) and bound the block below by \(1/2\). The evidence table must separate:

- terms tending to zero;
- adjacent partial-sum differences becoming small;
- a finite numerical plateau;
- arbitrary finite-tail control;
- a proved remainder bound.

- [ ] **Step 4: Add training and answers**

Add seven exercises and nine folded answers. At least one problem must construct a divergent sequence with adjacent differences tending to zero, and one must require solving an explicit epsilon budget.

- [ ] **Step 5: Run focused tests**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_unit_two_uses_arbitrary_finite_tails \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_units_have_final_metadata_hours_anchors_and_training -v
python3.12 scripts/check_content.py
```

Expected: Unit 23.2 focused test passes; registry aggregate remains red only for missing later pages.

- [ ] **Step 6: Commit Unit 23.2**

```bash
git add content/chapters/chapter-23/u-06-23-02-cauchy-tail.md
git commit -m "docs: prove the series Cauchy tail criterion"
```

### Task 5: Write Unit 23.3 — direct and limit comparison

**Files:**

- Create: `content/chapters/chapter-23/u-06-23-03-comparison-tests.md`

- [ ] **Step 1: Confirm the comparison contract is red**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_unit_three_keeps_both_comparison_directions -v
```

Expected: FAIL because the page is missing.

- [ ] **Step 2: Create metadata**

Use hours `{theory: 1.25, applied: 0.5}`, difficulty `4`, prerequisites
`[u-02-07-01, u-06-23-02]`, and capabilities
`[positive_series, direct_comparison, limit_comparison, comparison_tail_bound]`.

- [ ] **Step 3: Write the proof core**

Include:

```markdown
### 正项级数的单调部分和 {#thm-u-06-23-03-positive-monotone}
### 直接比较判别 {#thm-u-06-23-03-direct-comparison}
### 极限比较判别 {#thm-u-06-23-03-limit-comparison}
### 比较同时给出余项控制 {#cor-u-06-23-03-tail-bound}
```

Prove:

- nonnegative series converges iff its partial sums are bounded above;
- if \(0\le a_n\le b_n\) eventually and \(\sum b_n\) converges, then \(\sum a_n\) converges;
- if \(0\le a_n\le b_n\) eventually and \(\sum a_n\) diverges, then \(\sum b_n\) diverges;
- if \(a_n/b_n\to L\in(0,\infty)\), the two positive series have the same behavior;
- legal one-sided conclusions for \(L=0\) and \(L=\infty\);
- a comparison tail bound retaining constants and its starting index.

- [ ] **Step 4: Add examples, exercises, and diagnoses**

Add at least three examples, two checks, eight exercises, and ten answers. Include rational-term comparison, a logarithmic factor, a reversed-comparison error, a limit-comparison constant, and a tail-budget problem.

- [ ] **Step 5: Run focused tests and validation**

```bash
python3.12 -m unittest \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_unit_three_keeps_both_comparison_directions -v
python3.12 scripts/check_content.py
```

Expected: PASS.

- [ ] **Step 6: Commit Unit 23.3**

```bash
git add content/chapters/chapter-23/u-06-23-03-comparison-tests.md
git commit -m "docs: prove positive series comparison tests"
```

### Task 6: Write Unit 23.4 — ratio, root, and limsup tests

**Files:**

- Create: `content/chapters/chapter-23/u-06-23-04-ratio-root-tests.md`

- [ ] **Step 1: Confirm the ratio/root contract is red**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_unit_four_keeps_critical_value_and_limsup_boundaries -v
```

Expected: FAIL because the page is missing.

- [ ] **Step 2: Create metadata**

Use hours `{theory: 1.25, applied: 0.5}`, difficulty `4`, prerequisites
`[u-02-08-05, u-06-23-01, u-06-23-03]`, and capabilities
`[ratio_test, root_test, limsup_test, critical_case_diagnosis]`.

- [ ] **Step 3: Write theorem proofs and boundaries**

Include:

```markdown
### 比值判别 {#thm-u-06-23-04-ratio-test}
### 根值判别 {#thm-u-06-23-04-root-test}
### 上极限形式 {#thm-u-06-23-04-limsup-forms}
### 例：临界值 1 为什么没有结论 {#ex-u-06-23-04-critical-one}
```

Derive eventual geometric domination with an explicit \(q<1\). Give both convergence and divergence conclusions. For limsup, explicitly choose \(q\) strictly between the limsup and \(1\). Use harmonic and \(p=2\) series to show critical value \(1\) can accompany either behavior. Include a sequence whose ratio limit fails but root limsup succeeds.

- [ ] **Step 4: Add method-selection training**

Add eight exercises and ten answers covering factorials, exponentials, powers, oscillating ratios, critical failure, and a comparison-vs-ratio cost table.

- [ ] **Step 5: Run focused tests**

```bash
python3.12 -m unittest \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_unit_four_keeps_critical_value_and_limsup_boundaries -v
python3.12 scripts/check_content.py
```

Expected: PASS.

- [ ] **Step 6: Commit Unit 23.4**

```bash
git add content/chapters/chapter-23/u-06-23-04-ratio-root-tests.md
git commit -m "docs: derive ratio root and limsup tests"
```

### Task 7: Implement certified truncation and write Unit 23.5

**Files:**

- Create: `src/mathbook_examples/series.py`
- Create: `content/chapters/chapter-23/u-06-23-05-integral-condensation.md`
- Test: `tests/test_series.py`

- [ ] **Step 1: Run the algorithm tests and verify red**

Run:

```bash
python3.12 -m unittest tests.test_series -v
```

Expected: ERROR importing `mathbook_examples.series`.

- [ ] **Step 2: Implement the frozen result and input validation**

Create `src/mathbook_examples/series.py`:

```python
"""Certified truncation helpers for the Chapter 23 examples."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class SeriesCertificate:
    approximation: float
    error_bound: float
    terms_used: int
    status: str
    assumptions: tuple[str, ...]


def _positive_finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return value


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value
```

- [ ] **Step 3: Implement the geometric certificate**

Add:

```python
def geometric_series_certificate(
    first_term: float,
    ratio: float,
    tolerance: float,
    max_terms: int,
) -> SeriesCertificate:
    first_term = float(first_term)
    ratio = float(ratio)
    tolerance = _positive_finite(tolerance, "tolerance")
    max_terms = _positive_integer(max_terms, "max_terms")
    if not math.isfinite(first_term):
        raise ValueError("first_term must be finite")
    if not math.isfinite(ratio) or abs(ratio) >= 1.0:
        raise ValueError("ratio must be finite with absolute value below 1")

    partial = 0.0
    term = first_term
    error_bound = abs(first_term) / (1.0 - abs(ratio))
    terms_used = 0
    while terms_used < max_terms:
        partial += term
        terms_used += 1
        term *= ratio
        error_bound = abs(term) / (1.0 - abs(ratio))
        if error_bound <= tolerance:
            return SeriesCertificate(
                partial,
                error_bound,
                terms_used,
                "certified",
                ("|r| < 1", "geometric tail formula"),
            )
    return SeriesCertificate(
        partial,
        error_bound,
        terms_used,
        "budget_unmet",
        ("|r| < 1", "geometric tail formula"),
    )
```

The locked example uses eight terms: after summing through \(r^7\), the
remaining geometric bound is \(2^{-7}<0.01\). Keep term counting, the
approximation, and the tail bound on this same convention.

- [ ] **Step 4: Implement the \(p\)-series integral certificate**

Add:

```python
def p_series_integral_certificate(
    exponent: float,
    tolerance: float,
    max_terms: int,
) -> SeriesCertificate:
    exponent = float(exponent)
    tolerance = _positive_finite(tolerance, "tolerance")
    max_terms = _positive_integer(max_terms, "max_terms")
    if not math.isfinite(exponent) or exponent <= 1.0:
        raise ValueError("exponent must be finite and greater than 1")

    required = max(
        1,
        math.ceil(
            ((exponent - 1.0) * tolerance)
            ** (-1.0 / (exponent - 1.0))
        ),
    )
    terms_used = min(required, max_terms)
    approximation = math.fsum(
        1.0 / (n**exponent) for n in range(1, terms_used + 1)
    )
    error_bound = (
        terms_used ** (1.0 - exponent) / (exponent - 1.0)
    )
    status = "certified" if error_bound <= tolerance else "budget_unmet"
    return SeriesCertificate(
        approximation,
        error_bound,
        terms_used,
        status,
        (
            "p > 1",
            "x^-p is positive and decreasing on [1, infinity)",
            "integral-test tail upper bound",
        ),
    )
```

Check the boundary case where floating rounding makes `required` one too small: increment while the proved bound exceeds tolerance, without exceeding `max_terms`.

- [ ] **Step 5: Run algorithm tests**

Run:

```bash
python3.12 -m unittest tests.test_series -v
```

Expected: all series certificate tests pass.

- [ ] **Step 6: Write Unit 23.5**

Create metadata with hours `{theory: 1.25, applied: 0.5}`, difficulty `4`, prerequisites
`[u-05-19-04, u-05-22-02, u-06-23-03]`, Python prerequisite
`[mathbook_examples.series]`, and capabilities
`[integral_test, integral_tail_bound, cauchy_condensation, p_series, certified_truncation]`.

Include these anchors:

```markdown
### 积分判别 {#thm-u-06-23-05-integral-test}
### 积分余项的上下界 {#cor-u-06-23-05-integral-tail-bounds}
### Cauchy 凝聚判别 {#thm-u-06-23-05-cauchy-condensation}
### 例 1：\(p\)-级数 {#ex-u-06-23-05-p-series}
### 例 2：对数修正族 {#ex-u-06-23-05-logarithmic-family}
### 带条件的截断证书 {#alg-u-06-23-05-certified-truncation}
```

Prove the integral inequalities by rectangles for a finally nonnegative decreasing function. Prove condensation by dyadic blocks. Treat:

\[
\sum_{n=1}^{\infty}\frac1{n^p},
\qquad
\sum_{n\ge2}\frac1{n(\log n)^q}.
\]

The algorithm section must use:

> 问题来源 → 数学转化 → 算法思想 → 误差与适用条件 → 伪代码 → Python → 结果解释

State that the caller proves monotonicity and the comparison model; the code checks only finite scalar inputs and the formulas it implements. Add ten exercises and thirteen folded answers.

- [ ] **Step 7: Run Chapter 23 content and algorithm tests**

```bash
python3.12 -m unittest tests.test_chapter_23 tests.test_series -v
python3.12 scripts/check_content.py
```

Expected: content, hours, anchors, training totals, mathematical contracts, and algorithm tests pass except publication integration not yet added.

- [ ] **Step 8: Commit Unit 23.5 and the shared implementation**

```bash
git add \
  src/mathbook_examples/series.py \
  tests/test_series.py \
  content/chapters/chapter-23/u-06-23-05-integral-condensation.md
git commit -m "docs: add certified positive series truncation"
```

### Task 8: Publish Chapter 23 and migrate the live release boundary

**Files:**

- Modify: `README.md`
- Modify: `content/course-map.md`
- Modify: `mkdocs.yml`
- Modify: `scripts/check_site.py`
- Modify: `tests/test_chapter_15.py`
- Modify: `tests/test_chapter_16.py`
- Modify: `tests/test_chapter_17.py`
- Modify: `tests/test_chapter_18.py`
- Modify: `tests/test_chapter_19.py`
- Modify: `tests/test_chapter_20.py`
- Modify: `tests/test_chapter_21.py`
- Modify: `tests/test_chapter_22.py`
- Modify: `tests/test_part_04_consistency.py`
- Modify: `tests/test_zensical_structure.py`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Update release-boundary regression assertions**

Replace live assertions of:

```text
第五部第 22 章，共 98 个学习单元
```

with:

```text
第六部第 23 章，共 103 个学习单元
```

Only update tests whose purpose is the current live publication boundary. Keep historical review assertions unchanged.

Update dependency-boundary assertions to inspect `part-06-dependencies.md` for:

```text
当前发布边界：第 23 章
24 个核心单元，42 学时
当前已发布第六部 5 个核心单元、8.5 学时
```

- [ ] **Step 2: Update README and course map**

Set the README sentence to:

```markdown
Material 3 阅读模式；当前发布第一至第五部及第六部第 23 章，共 103 个学习单元。
```

In `content/course-map.md`:

- update the top release sentence to Chapter 23/103;
- add `## 第六部：无穷级数与函数逼近`;
- state the approved total `42 小时（理论 30.5，应用 11.5）`;
- add the Chapter 23 heading, exact 8.5-hour row, and five links;
- state that Chapter 24–27 remain approved routes without pages;
- change the final future-route prose to start at Chapter 24, not Part VI.

- [ ] **Step 3: Add navigation**

Append after Part V in `mkdocs.yml`:

```yaml
  - 第六部：无穷级数与函数逼近:
      - 第 23 章：数项级数的收敛与正项判别:
          - 本章导学: chapters/chapter-23/index.md
          - 23.1 无限求和怎样由部分和定义？: chapters/chapter-23/u-06-23-01-partial-sums.md
          - 23.2 Cauchy 尾部判据怎样控制无限求和？: chapters/chapter-23/u-06-23-02-cauchy-tail.md
          - 23.3 正项级数怎样通过比较判断收敛？: chapters/chapter-23/u-06-23-03-comparison-tests.md
          - 23.4 局部增长率怎样产生比值与根值判别？: chapters/chapter-23/u-06-23-04-ratio-root-tests.md
          - 23.5 积分与凝聚怎样提供判别和余项证书？: chapters/chapter-23/u-06-23-05-integral-condensation.md
```

Do not add Chapter 24–27 entries.

- [ ] **Step 4: Add rendered anchor and sidebar expectations**

In `scripts/check_site.py`, add:

```python
"chapters/chapter-23/u-06-23-02-cauchy-tail/index.html": [
    "thm-u-06-23-02-cauchy-tail",
    "tbl-u-06-23-02-evidence-boundary",
],
"chapters/chapter-23/u-06-23-05-integral-condensation/index.html": [
    "thm-u-06-23-05-integral-test",
    "thm-u-06-23-05-cauchy-condensation",
    "alg-u-06-23-05-certified-truncation",
],
```

Both pages require:

```python
[
    "md-sidebar",
    "第六部：无穷级数与函数逼近",
    "第 23 章：数项级数的收敛与正项判别",
]
```

Mirror these dictionaries in `tests/test_mkdocs_site.py`.

- [ ] **Step 5: Run publication tests**

```bash
python3.12 -m unittest \
  tests.test_chapter_23 \
  tests.test_zensical_structure \
  tests.test_mkdocs_site -v
```

Expected: PASS after a strict site build exists; if site files are absent, run `zensical build --clean --strict` and rerun.

- [ ] **Step 6: Commit publication**

```bash
git add \
  README.md \
  content/course-map.md \
  mkdocs.yml \
  scripts/check_site.py \
  tests/test_chapter_*.py \
  tests/test_part_04_consistency.py \
  tests/test_zensical_structure.py \
  tests/test_mkdocs_site.py
git commit -m "docs: publish chapter 23 number series"
```

### Task 9: Audit Chapter 23 and close at the chapter boundary

**Files:**

- Create: `docs/reviews/2026-07-30-chapter-23-consistency-review.md`

- [ ] **Step 1: Run focused mathematical searches**

Run:

```bash
rg -n \
  '必要条件|充分条件|临界值 1|最终非负|单调递减|上极限|余项|误差证书|相邻部分和差' \
  content/chapters/chapter-23
```

Expected: every theorem condition and certificate boundary is visible in the relevant page.

Run:

```bash
rg -n \
  '交错级数判别|Riemann 重排|Cauchy 乘积|Mertens 定理|函数项级数|一致收敛|幂级数|Fourier 级数|Lebesgue 积分' \
  content/chapters/chapter-23
```

Expected: occurrences only in chapter/unit boundary sections after `## 常见误区与后续`, never in the proof core.

- [ ] **Step 2: Verify exact totals**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_23.ChapterTwentyThreeTests.test_units_have_final_metadata_hours_anchors_and_training -v
```

Expected: 5 units, theory `6.5`, application `2.0`, 40 exercises, 51 answers.

- [ ] **Step 3: Run the full quality gate**

```bash
make verify
python3.12 scripts/check_content.py
zensical build --clean --strict
python3.12 scripts/check_site.py
```

Expected: all unit tests pass, content validation succeeds, strict build succeeds, and site validation succeeds. Record the actual test count and build result; do not copy the baseline count.

- [ ] **Step 4: Inspect representative rendered pages**

Inspect:

- `site/chapters/chapter-23/u-06-23-02-cauchy-tail/index.html`
- `site/chapters/chapter-23/u-06-23-05-integral-condensation/index.html`

Confirm rendered mathematics, stable anchors, folded answers, code blocks, Part VI sidebar, and Chapter 23 order.

- [ ] **Step 5: Write the consistency review**

Create `docs/reviews/2026-07-30-chapter-23-consistency-review.md` with:

- scope and reviewed commit;
- summary verdict;
- five-unit proof-chain audit;
- comparison-direction and critical-case audit;
- certificate-semantics audit;
- training counts and hours;
- publication and rendered-anchor audit;
- exact verification commands/results;
- deferred Chapter 24–27 boundaries;
- explicit statement that no high- or medium-priority issue remains.

- [ ] **Step 6: Run final verification after the review**

```bash
make verify
git diff --check
git status --short
```

Expected: full verification passes; only the new review is uncommitted.

- [ ] **Step 7: Commit the review**

```bash
git add docs/reviews/2026-07-30-chapter-23-consistency-review.md
git commit -m "docs: review chapter 23 consistency"
```

- [ ] **Step 8: Stop**

Do not create Chapter 24 files or navigation. Report the branch, commits, tests, publication count, and review result. Wait for explicit approval before designing or implementing Chapter 24.

## Plan self-review

- Spec coverage: all five approved Chapter 23 units, the 24-unit Part VI dependency map, algorithm contracts, release migration, rendered verification, and chapter stop point map to explicit tasks.
- Placeholder scan: no `TBD`, `TODO`, “similar to”, or unspecified error-handling step remains.
- Type consistency: `SeriesCertificate` fields and function signatures are identical in tests, implementation snippets, and Unit 23.5 documentation requirements.
- Scope: Chapter 24–27 are represented only in the dependency map and prose route; no future page or navigation placeholder is authorized.
