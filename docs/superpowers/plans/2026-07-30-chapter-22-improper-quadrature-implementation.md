# Chapter 22 Improper Integrals and Certified Quadrature Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Chapter 22 as six rigorous self-study units, add one tested quadrature implementation, close Part V at 25 units and 42.5 hours, and record a Chapter 22 plus Part V consistency review.

**Architecture:** Add a chapter guide and six `content_standard: 2` pages under `content/chapters/chapter-22/`. Lock mathematical, training, algorithm, publication, and rendered-anchor contracts in failing tests before implementation; build the shared quadrature module before the numerical units; publish only after every unit contract is green. Keep infinite-series theory, general limit–integral interchange, advanced quadrature, Lebesgue integration, and parameter-dependent improper integrals outside the chapter.

**Tech Stack:** Markdown with YAML front matter and MathJax, Python 3.12 standard library, `unittest`, PyYAML, Zensical/MkDocs, existing content and site validation scripts.

---

## File map

**Create**

- `content/chapters/chapter-22/index.md` — chapter route, prerequisites, two-track error-control story, and Part V exit.
- `content/chapters/chapter-22/u-05-22-01-improper-definition.md` — endpoint definitions, Cauchy tails, and \(p\)-integrals.
- `content/chapters/chapter-22/u-05-22-02-comparison-tests.md` — direct and limit comparison plus tail bounds.
- `content/chapters/chapter-22/u-05-22-03-absolute-conditional-oscillation.md` — absolute convergence, Dirichlet, Abel, conditional convergence, and principal-value boundary.
- `content/chapters/chapter-22/u-05-22-04-midpoint-trapezoid.md` — composite midpoint and trapezoid rules with second-derivative bounds.
- `content/chapters/chapter-22/u-05-22-05-simpson-certificates.md` — composite Simpson, fourth-derivative error, grid budget, and stop states.
- `content/chapters/chapter-22/u-05-22-06-certified-improper-quadrature.md` — combined tail and finite-quadrature certificate workflow.
- `src/mathbook_examples/quadrature.py` — the only executable midpoint, trapezoid, Simpson, and budgeted-Simpson implementation.
- `tests/test_quadrature.py` — behavioral and failure-boundary tests for the shared implementation.
- `tests/test_chapter_22.py` — metadata, mathematics, training density, scope, publication, and anchor contract.
- `docs/reviews/2026-07-30-chapter-22-and-part-05-consistency-review.md` — mathematical, pedagogical, publication, and engineering audit.

**Modify**

- `README.md` — release boundary and 98-unit count.
- `content/course-map.md` — Chapter 22 section, six links, 12 hours, and closed Part V route.
- `docs/curriculum/part-05-dependencies.md` — sixth Chapter 22 unit, 25-unit/42.5-hour totals, and current boundary.
- `docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md` — current total row only: 292.75 theory, 101.25 application, 394 total.
- `mkdocs.yml` — Chapter 22 guide and six pages after Chapter 21.
- `scripts/check_site.py` — representative Chapter 22 URLs, anchors, and sidebar expectations.
- `tests/test_chapter_15.py`
- `tests/test_chapter_16.py`
- `tests/test_chapter_17.py`
- `tests/test_chapter_18.py`
- `tests/test_chapter_19.py`
- `tests/test_chapter_20.py`
- `tests/test_chapter_21.py`
- `tests/test_part_04_consistency.py`
- `tests/test_zensical_structure.py`
- `tests/test_mkdocs_site.py`

Historical chapter design documents retain the numbers that were current when they were approved. Only the master current-total row, current dependency map, current course map, README, and live tests move to the new baseline.

### Task 1: Lock Chapter 22 and quadrature contracts in failing tests

**Files:**

- Create: `tests/test_chapter_22.py`
- Create: `tests/test_quadrature.py`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Write the Chapter 22 contract test**

Create constants with the exact approved registry:

```python
ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-22"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-05-dependencies.md"

EXPECTED_UNITS = [
    ("u-05-22-01", "反常积分怎样由逐端点极限定义？", 1.50, 0.25, "improper-definition", 6, 8),
    ("u-05-22-02", "正函数怎样比较收敛并控制尾部？", 1.50, 0.25, "comparison-tests", 7, 9),
    ("u-05-22-03", "绝对、条件与振荡收敛怎样区分？", 1.50, 0.50, "absolute-conditional-oscillation", 8, 10),
    ("u-05-22-04", "中点与梯形公式怎样产生可证明误差界？", 1.25, 0.75, "midpoint-trapezoid", 7, 9),
    ("u-05-22-05", "Simpson 方法怎样给出预算与误差证书？", 1.00, 1.50, "simpson-certificates", 8, 10),
    ("u-05-22-06", "反常积分怎样完成可靠数值计算？", 0.50, 1.50, "certified-improper-quadrature", 12, 16),
]
```

Lock these anchors:

```python
REQUIRED_ANCHORS = {
    "u-05-22-01": (
        "def-u-05-22-01-infinite-interval-improper-integral",
        "def-u-05-22-01-singular-endpoint-improper-integral",
        "thm-u-05-22-01-cauchy-tail-criterion",
        "ex-u-05-22-01-p-integrals",
    ),
    "u-05-22-02": (
        "thm-u-05-22-02-direct-comparison",
        "thm-u-05-22-02-limit-comparison",
        "cor-u-05-22-02-tail-bound",
        "ex-u-05-22-02-tail-budget",
    ),
    "u-05-22-03": (
        "thm-u-05-22-03-absolute-implies-convergence",
        "thm-u-05-22-03-dirichlet-test",
        "cor-u-05-22-03-abel-test",
        "ex-u-05-22-03-conditional-sine-over-x",
        "ex-u-05-22-03-principal-value-boundary",
    ),
    "u-05-22-04": (
        "alg-u-05-22-04-composite-midpoint",
        "thm-u-05-22-04-midpoint-error",
        "alg-u-05-22-04-composite-trapezoid",
        "thm-u-05-22-04-trapezoid-error",
    ),
    "u-05-22-05": (
        "alg-u-05-22-05-composite-simpson",
        "thm-u-05-22-05-simpson-error",
        "alg-u-05-22-05-certified-simpson-budget",
        "ex-u-05-22-05-budget-exhaustion",
    ),
    "u-05-22-06": (
        "alg-u-05-22-06-total-error-workflow",
        "thm-u-05-22-06-total-error-certificate",
        "ex-u-05-22-06-exponential-baseline",
        "ex-u-05-22-06-gaussian-tail-budget",
        "ex-u-05-22-06-uncertified-grid-difference",
    ),
}
```

Implement `test_units_have_final_metadata_hours_anchors_and_training` by following the Chapter 21 parser pattern. Assert exact theory total `7.25`, application total `4.75`, exercise total `48`, answer total `62`, at least two examples per unit, two immediate checks in Units 22.1–22.5, and four immediate checks in Unit 22.6.

Add the guide contract:

```python
def test_chapter_guide_lists_units_hours_routes_and_boundaries(self) -> None:
    guide = self.required_text(CHAPTER / "index.md")
    self.assertIn("本章共6个核心单元，12学时（理论7.25，应用4.75）。", guide)
    for marker in (
        "逐端点极限",
        "Cauchy 尾部",
        "局部近似",
        "误差界",
        "预算与停止状态",
        "第 19 章",
        "第 20 章",
        "第 21 章",
        "第五部",
        "第六部",
    ):
        self.assertIn(marker, guide)
    for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
        self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))
```

Add focused tests with exact markers:

```python
def test_unit_one_defines_every_improper_endpoint_separately(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[0]))
    for marker in (
        "局部 Riemann 可积",
        "逐端点",
        "Cauchy 尾部判据",
        "切分点无关",
        "内部奇点",
        "对称主值",
    ):
        self.assertIn(marker, text)
    self.assertIn(r"\int_1^\infty x^{-p}\,dx", text)
    self.assertIn(r"\int_0^1 x^{-p}\,dx", text)

def test_unit_two_keeps_comparison_directions_and_tail_bounds(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[1]))
    for marker in (
        "最终成立",
        "直接比较",
        "极限比较",
        "上方函数收敛",
        "下方函数发散",
        "L=0",
        "L=\\infty",
        "尾部误差",
    ):
        self.assertIn(marker, text)

def test_unit_three_proves_oscillation_contracts(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[2]))
    for marker in (
        "绝对收敛推出收敛",
        "Dirichlet 判别",
        "Abel 判别",
        "条件收敛",
        "有界原函数",
        "单调递减",
        "Cauchy 主值",
    ):
        self.assertIn(marker, text)
    self.assertIn(r"\int_1^\infty\frac{\sin x}{x}\,dx", text)

def test_unit_four_has_both_second_derivative_error_constants(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[3]))
    self.assertIn(r"\frac{b-a}{24}M_2h^2", text)
    self.assertIn(r"\frac{b-a}{12}M_2h^2", text)
    self.assertIn("整个区间", text)

def test_unit_five_keeps_simpson_certificate_semantics(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[4]))
    self.assertIn(r"\frac{b-a}{180}M_4h^4", text)
    for marker in (
        "正偶数",
        "三次多项式",
        "反复 Rolle",
        "调用者",
        "budget_exhausted",
        "target_met",
        "浮点舍入误差",
    ):
        self.assertIn(marker, text)

def test_unit_six_has_locked_total_error_training(self) -> None:
    text = self.required_text(unit_path(EXPECTED_UNITS[5]))
    self.assertEqual(4, text.count("{#pr-u-05-22-06-mixed-"))
    self.assertEqual(3, text.count("{#pr-u-05-22-06-diagnosis-"))
    self.assertEqual(2, text.count("{#pr-u-05-22-06-boundary-"))
    self.assertEqual(3, text.count("{#pr-u-05-22-06-verification-"))
    for marker in (
        "先证明收敛",
        "尾部误差预算",
        "求积误差预算",
        "三角不等式",
        "导数界",
        "总误差证书",
    ):
        self.assertIn(marker, text)
```

Add publication assertions for Chapter 22, 98 published units, Part V `25 个核心单元` and `42.5 学时`, and the master current totals `292.75`, `101.25`, and `394`.

Define `FORBIDDEN_CORE_TERMS` as:

```python
FORBIDDEN_CORE_TERMS = (
    "无穷级数判别",
    "幂级数展开",
    "一致收敛",
    "Euler–Maclaurin",
    "Romberg",
    "自适应求积",
    "Gauss 求积",
    "Lebesgue 积分",
    "含参反常积分",
    "Gamma 函数",
    "Beta 函数",
)
```

Check only the text before `## 常见误区与后续`, so boundary notes may name later topics.

- [ ] **Step 2: Write failing quadrature behavior tests**

Create `tests/test_quadrature.py` with imports from `mathbook_examples.quadrature` and these behaviors:

```python
def test_midpoint_and_trapezoid_return_frozen_fixed_grid_results(self) -> None:
    midpoint = composite_midpoint(lambda x: x * x, 0.0, 1.0, 8, 2.0)
    trapezoid = composite_trapezoid(lambda x: x * x, 0.0, 1.0, 8, 2.0)
    self.assertEqual("midpoint", midpoint.method)
    self.assertEqual("trapezoid", trapezoid.method)
    self.assertEqual("fixed_grid", midpoint.status)
    self.assertIsNone(midpoint.target_tolerance)
    self.assertIsNone(midpoint.target_met)
    self.assertEqual(8, midpoint.evaluations)
    self.assertEqual(9, trapezoid.evaluations)
    self.assertLessEqual(abs(midpoint.value - 1 / 3), midpoint.error_bound)
    self.assertLessEqual(abs(trapezoid.value - 1 / 3), trapezoid.error_bound)
    with self.assertRaises(FrozenInstanceError):
        midpoint.value = 0.0  # type: ignore[misc]

def test_simpson_is_exact_for_a_cubic_and_requires_even_grid(self) -> None:
    result = composite_simpson(lambda x: x**3 - 2 * x + 1, -1.0, 2.0, 6, 0.0)
    self.assertTrue(isclose(result.value, 3.75, rel_tol=0.0, abs_tol=1e-14))
    self.assertEqual(0.0, result.error_bound)
    with self.assertRaisesRegex(ValueError, "subdivisions must be a positive even integer"):
        composite_simpson(lambda x: x, 0.0, 1.0, 3, 0.0)

def test_budgeted_simpson_distinguishes_target_and_budget_exhaustion(self) -> None:
    met = certified_simpson(math.exp, 0.0, 1.0, 1e-8, math.e, 1000)
    exhausted = certified_simpson(math.exp, 0.0, 1.0, 1e-12, math.e, 4)
    self.assertEqual("target_met", met.status)
    self.assertTrue(met.target_met)
    self.assertLessEqual(met.error_bound, 1e-8)
    self.assertEqual("budget_exhausted", exhausted.status)
    self.assertFalse(exhausted.target_met)
    self.assertEqual(4, exhausted.subdivisions)
    self.assertGreater(exhausted.error_bound, 1e-12)
```

Add table-driven validation tests:

- endpoints must be finite;
- left endpoint must be smaller than right endpoint;
- subdivisions must be a positive integer;
- Simpson subdivisions must be even;
- derivative bounds must be nonnegative and finite;
- tolerance must be positive and finite;
- maximum subintervals must be an integer at least two;
- nonfinite function values raise `QuadratureEvaluationError`;
- caller exceptions are wrapped as `QuadratureEvaluationError` with the original exception as `__cause__`;
- a budget of five uses the largest permitted even grid, four;
- the returned analytic error bound follows the exact midpoint, trapezoid, and Simpson formulas.

- [ ] **Step 3: Add rendered-site test expectations**

Extend `tests/test_mkdocs_site.py` with one method per representative page,
using the dictionaries already imported by that module:

```python
def test_checks_chapter_twenty_two_definition_page(self) -> None:
    page = "chapters/chapter-22/u-05-22-01-improper-definition/index.html"
    self.assertEqual(
        [
            "def-u-05-22-01-infinite-interval-improper-integral",
            "thm-u-05-22-01-cauchy-tail-criterion",
        ],
        REQUIRED_RENDERED_ANCHORS[page],
    )
    self.assertEqual(
        [
            "md-sidebar",
            "第五部：积分、累积与数值求积",
            "第 22 章：反常积分与数值求积",
        ],
        REQUIRED_NAVIGATION_MARKERS[page],
    )

def test_checks_chapter_twenty_two_simpson_page(self) -> None:
    page = "chapters/chapter-22/u-05-22-05-simpson-certificates/index.html"
    self.assertEqual(
        [
            "thm-u-05-22-05-simpson-error",
            "alg-u-05-22-05-certified-simpson-budget",
        ],
        REQUIRED_RENDERED_ANCHORS[page],
    )
    self.assertEqual(
        [
            "md-sidebar",
            "第五部：积分、累积与数值求积",
            "第 22 章：反常积分与数值求积",
        ],
        REQUIRED_NAVIGATION_MARKERS[page],
    )

def test_checks_chapter_twenty_two_total_error_page(self) -> None:
    page = (
        "chapters/chapter-22/"
        "u-05-22-06-certified-improper-quadrature/index.html"
    )
    self.assertEqual(
        [
            "alg-u-05-22-06-total-error-workflow",
            "thm-u-05-22-06-total-error-certificate",
        ],
        REQUIRED_RENDERED_ANCHORS[page],
    )
    self.assertEqual(
        [
            "md-sidebar",
            "第五部：积分、累积与数值求积",
            "第 22 章：反常积分与数值求积",
        ],
        REQUIRED_NAVIGATION_MARKERS[page],
    )
```

- [ ] **Step 4: Verify RED**

Run:

```bash
python3.12 -m unittest tests.test_chapter_22 tests.test_quadrature tests.test_mkdocs_site -v
```

Expected: failures for missing Chapter 22 pages and publication entries plus an import error for missing `mathbook_examples.quadrature`. Existing non-Chapter-22 site tests remain green.

- [ ] **Step 5: Commit the failing contracts**

```bash
git add tests/test_chapter_22.py tests/test_quadrature.py tests/test_mkdocs_site.py
git commit -m "test: lock chapter 22 and quadrature contracts"
```

### Task 2: Implement the shared quadrature module with TDD

**Files:**

- Create: `src/mathbook_examples/quadrature.py`
- Test: `tests/test_quadrature.py`

- [ ] **Step 1: Define the result and evaluation error**

Implement:

```python
from collections.abc import Callable
from dataclasses import dataclass, replace
from math import ceil, fsum, isfinite


class QuadratureEvaluationError(ValueError):
    """Report a failed or nonfinite black-box function evaluation."""


@dataclass(frozen=True)
class QuadratureResult:
    method: str
    value: float
    subdivisions: int
    evaluations: int
    error_bound: float
    target_tolerance: float | None
    target_met: bool | None
    status: str
```

Add helpers that reject booleans as integers, require finite interval width, require nonnegative finite derivative bounds, and wrap failed/nonfinite samples in `QuadratureEvaluationError`.

- [ ] **Step 2: Implement fixed-grid midpoint and trapezoid**

Use `h = (b - a) / subdivisions`, `fsum`, and the exact bounds:

```python
midpoint_error = (b - a) * second_derivative_bound * h**2 / 24.0
trapezoid_error = (b - a) * second_derivative_bound * h**2 / 12.0
```

Return `status="fixed_grid"`, `target_tolerance=None`, and `target_met=None`. Reject a nonfinite computed value or bound instead of returning it.

- [ ] **Step 3: Implement fixed-grid Simpson**

Require a positive even subdivision count. Use odd weight four and positive-even interior weight two:

```python
weighted = values[0] + values[-1]
weighted += 4.0 * fsum(values[index] for index in range(1, subdivisions, 2))
weighted += 2.0 * fsum(values[index] for index in range(2, subdivisions, 2))
value = h * weighted / 3.0
error_bound = (b - a) * fourth_derivative_bound * h**4 / 180.0
```

Return exactly `subdivisions + 1` evaluations.

- [ ] **Step 4: Implement budgeted Simpson**

Compute the raw requirement

\[
n\ge\left(\frac{M_4(b-a)^5}{180\tau}\right)^{1/4}.
\]

Round upward and then to the next even integer, with minimum two. Adjust by two around the rounded candidate until the implemented error formula confirms that the chosen even count is the smallest permitted count meeting the tolerance. When that count exceeds `max_subintervals`, use the largest positive even count not exceeding the budget and return `status="budget_exhausted"`.

Call `composite_simpson` once, then replace only the target fields using `dataclasses.replace`:

```python
return replace(
    fixed,
    target_tolerance=tolerance,
    target_met=fixed.error_bound <= tolerance,
    status="target_met" if fixed.error_bound <= tolerance else "budget_exhausted",
)
```

Validate the budget before computing the grid. A nonfinite raw requirement or analytic bound raises `ValueError` with a specific finite-bound message.

- [ ] **Step 5: Run the focused algorithm tests**

Run:

```bash
python3.12 -m unittest tests.test_quadrature -v
```

Expected: all quadrature tests pass, including frozen result, exact cubic, parameter failures, evaluation failures, smallest-even budget, and budget exhaustion.

- [ ] **Step 6: Commit**

```bash
git add src/mathbook_examples/quadrature.py tests/test_quadrature.py
git commit -m "feat: add certified composite quadrature"
```

### Task 3: Establish the Chapter 22 guide

**Files:**

- Create: `content/chapters/chapter-22/index.md`
- Test: `tests/test_chapter_22.py`

- [ ] **Step 1: Write the guide**

Use H1 anchor `{#chapter-22}` and the exact sentence:

```markdown
本章共6个核心单元，12学时（理论7.25，应用4.75）。
```

List the six units in registry order with exact relative links and hours. Explain both routes:

```tex
\text{逐端点极限}\to\text{Cauchy 尾部}\to\text{判别与尾部估计}
```

and

```tex
\text{局部近似}\to\text{复合公式}\to\text{误差界}\to\text{预算与停止状态}.
```

State that Chapter 19 supplies Riemann integration, Chapter 20 supplies normal-integral calculation, Chapter 21 supplies finite models, and Chapter 22 closes Part V. State that infinite series and general interchange theorems begin later and no Part VI blank pages are created.

- [ ] **Step 2: Run the guide contract**

Run:

```bash
python3.12 -m unittest tests.test_chapter_22.ChapterTwentyTwoTests.test_chapter_guide_lists_units_hours_routes_and_boundaries -v
```

Expected: pass.

- [ ] **Step 3: Commit**

```bash
git add content/chapters/chapter-22/index.md
git commit -m "docs: establish chapter 22 error control routes"
```

### Task 4: Write Unit 22.1 improper definitions

**Files:**

- Create: `content/chapters/chapter-22/u-05-22-01-improper-definition.md`
- Test: `tests/test_chapter_22.py`

- [ ] **Step 1: Add exact front matter**

```yaml
---
title: 反常积分怎样由逐端点极限定义？
unit_id: u-05-22-01
hours: {theory: 1.5, applied: 0.25}
difficulty: 4
prerequisites:
  book: [u-05-19-02, u-05-19-04, u-05-20-03]
  higher_algebra: [幂函数, 广义分式, 参数不等式]
  analytic_geometry: [区间, 单侧邻域, 无穷区间]
  python: [有限截断仅作观察]
capabilities: [improper_definition, endpoint_splitting, cauchy_tail, p_integral_classification]
learning_goals: [逐端点定义反常积分, 使用Cauchy尾部判据, 判定两类p积分, 区分通常收敛与主值]
content_standard: 2
---
```

- [ ] **Step 2: Close the definition and proof core**

Write the standard page sections through `## 概念与理论`. Include:

- local Riemann integrability away from every improper endpoint;
- both infinite-direction definitions;
- finite singular endpoint definitions;
- a fixed split point for two infinite ends and a proof that changing the split point adds and subtracts one proper integral;
- separate limits at an interior singularity;
- the Cauchy tail theorem in both directions;
- both \(p\)-integral thresholds;
- a principal-value counterexample using an odd integrand whose one-sided tails fail.

Use all four approved stable anchors.

- [ ] **Step 3: Add self-study material**

Add at least two complete examples and two immediate checks. Add exactly six exercises with anchors `{#pr-u-05-22-01-...}` and eight folded `??? note "答案"` blocks. Include one endpoint-splitting diagnosis and one principal-value boundary problem.

- [ ] **Step 4: Verify and commit**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_22.ChapterTwentyTwoTests.test_units_have_final_metadata_hours_anchors_and_training \
  tests.test_chapter_22.ChapterTwentyTwoTests.test_unit_one_defines_every_improper_endpoint_separately -v
python3.12 scripts/check_content.py
```

Expected: Unit 22.1 subtests pass; the content checker passes for all currently present pages.

```bash
git add content/chapters/chapter-22/u-05-22-01-improper-definition.md
git commit -m "docs: define improper integrals endpoint by endpoint"
```

### Task 5: Write Unit 22.2 comparison tests and tail estimates

**Files:**

- Create: `content/chapters/chapter-22/u-05-22-02-comparison-tests.md`
- Test: `tests/test_chapter_22.py`

- [ ] **Step 1: Add exact front matter**

```yaml
---
title: 正函数怎样比较收敛并控制尾部？
unit_id: u-05-22-02
hours: {theory: 1.5, applied: 0.25}
difficulty: 4
prerequisites:
  book: [u-05-22-01, u-05-19-04]
  higher_algebra: [不等式, 极限等价, 幂函数比较]
  analytic_geometry: [最终区间, 有限端点邻域]
  python: [尾部界数值核对]
capabilities: [direct_comparison, limit_comparison, one_sided_limit_cases, tail_estimation]
learning_goals: [选择比较函数, 判断比较方向, 使用极限比较, 计算显式尾部界]
content_standard: 2
---
```

- [ ] **Step 2: Prove comparison in the correct directions**

Prove direct comparison using proper-integral order followed by the endpoint limit. State eventual comparison explicitly. Prove limit comparison for \(L\in(0,\infty)\) by choosing constants such as \(L/2\) and \(3L/2\). State only these one-sided consequences:

- \(f/g\to0\) and \(\int g\) convergent imply \(\int f\) convergent for eventually nonnegative functions;
- \(f/g\to\infty\) and \(\int g\) divergent imply \(\int f\) divergent.

Derive the tail corollary and use it to solve a tolerance inequality for \(R\).

- [ ] **Step 3: Add exact training density**

Add at least two examples, two immediate checks, exactly seven exercises, and nine folded answers. Include direct-comparison direction errors, a limit-comparison case, a finite-endpoint singularity, and two explicit tail-budget calculations.

- [ ] **Step 4: Verify and commit**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_22.ChapterTwentyTwoTests.test_units_have_final_metadata_hours_anchors_and_training \
  tests.test_chapter_22.ChapterTwentyTwoTests.test_unit_two_keeps_comparison_directions_and_tail_bounds -v
python3.12 scripts/check_content.py
```

Expected: all Unit 22.1–22.2 content subtests pass.

```bash
git add content/chapters/chapter-22/u-05-22-02-comparison-tests.md
git commit -m "docs: prove comparison tests and tail bounds"
```

### Task 6: Write Unit 22.3 absolute, conditional, and oscillatory convergence

**Files:**

- Create: `content/chapters/chapter-22/u-05-22-03-absolute-conditional-oscillation.md`
- Test: `tests/test_chapter_22.py`

- [ ] **Step 1: Add exact front matter**

```yaml
---
title: 绝对、条件与振荡收敛怎样区分？
unit_id: u-05-22-03
hours: {theory: 1.5, applied: 0.5}
difficulty: 5
prerequisites:
  book: [u-05-22-01, u-05-22-02, u-05-20-04, u-04-15-01]
  higher_algebra: [绝对值不等式, 分部积分, 三角函数]
  analytic_geometry: [周期区间, 对称截断]
  python: [振荡截断仅作经验观察]
capabilities: [absolute_convergence, conditional_convergence, dirichlet_test, abel_extension, principal_value_boundary]
learning_goals: [证明绝对收敛蕴含收敛, 核对Dirichlet条件, 识别条件收敛, 区分主值与通常积分]
content_standard: 2
---
```

- [ ] **Step 2: Prove absolute convergence and Dirichlet**

Use the Cauchy tail criterion and

\[
\left|\int_A^B f\right|\le\int_A^B|f|
\]

for absolute convergence. For Dirichlet, state the approved \(C^1\) version. If
\(|F(x)|\le M\), define \(H_A(x)=F(x)-F(A)\), so \(|H_A|\le2M\). Integration by parts gives

\[
\int_A^B fg=H_A(B)g(B)-\int_A^B H_Ag',
\]

and therefore a bound no larger than \(2Mg(B)+2M(g(A)-g(B))\le2Mg(A)\). This tends to zero uniformly in \(B>A\).

- [ ] **Step 3: Prove the examples and Abel extension**

Apply Dirichlet to \(\sin x/x\). Prove non-absolute convergence by lower-bounding \(|\sin x|\) on fixed-width subintervals of each period and comparing the resulting block integrals with a divergent logarithmic integral; do not cite a series test.

For Abel, let \(g\) be bounded and monotone with limit \(\ell\); write \(g=\ell+(g-\ell)\), use convergence of \(\int f\) for the constant term, and Dirichlet for the monotone-to-zero remainder.

Show separately that symmetric truncation can cancel while the two one-sided improper integrals fail.

- [ ] **Step 4: Add training, verify, and commit**

Add at least three examples, two immediate checks, exactly eight exercises, and ten folded answers. Include two theorem-condition diagnostics and one principal-value counterexample.

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_22.ChapterTwentyTwoTests.test_units_have_final_metadata_hours_anchors_and_training \
  tests.test_chapter_22.ChapterTwentyTwoTests.test_unit_three_proves_oscillation_contracts -v
python3.12 scripts/check_content.py
```

Expected: all Unit 22.1–22.3 content subtests pass.

```bash
git add content/chapters/chapter-22/u-05-22-03-absolute-conditional-oscillation.md
git commit -m "docs: prove absolute and oscillatory convergence tests"
```

### Task 7: Write Unit 22.4 midpoint and trapezoid formulas

**Files:**

- Create: `content/chapters/chapter-22/u-05-22-04-midpoint-trapezoid.md`
- Test: `tests/test_chapter_22.py`
- Reuse: `src/mathbook_examples/quadrature.py`

- [ ] **Step 1: Add exact front matter**

```yaml
---
title: 中点与梯形公式怎样产生可证明误差界？
unit_id: u-05-22-04
hours: {theory: 1.25, applied: 0.75}
difficulty: 4
prerequisites:
  book: [u-04-16-02, u-05-19-02, u-05-19-04, u-05-20-03]
  higher_algebra: [有限求和, 二次函数, 误差不等式]
  analytic_geometry: [中点, 割线, 线性插值]
  python: [函数调用, 复合求积结果读取]
capabilities: [composite_midpoint, composite_trapezoid, second_derivative_error, grid_budget]
learning_goals: [从局部近似建立复合公式, 推导二阶误差界, 核对全区间导数界, 解释误差阶]
content_standard: 2
---
```

- [ ] **Step 2: Derive the midpoint bound**

Define the uniform grid and the midpoint sum. On one interval centered at \(m\), use

\[
|f(x)-f(m)-f'(m)(x-m)|\le\frac{M_2}{2}(x-m)^2.
\]

Integrate; the odd linear term vanishes and the local bound is \(M_2h^3/24\). Sum \(n\) local errors to obtain \((b-a)M_2h^2/24\).

- [ ] **Step 3: Derive the trapezoid bound**

Let \(\ell_i\) interpolate the two endpoints. Prove the interpolation remainder

\[
f(x)-\ell_i(x)=\frac{f''(\xi_x)}2(x-x_{i-1})(x-x_i)
\]

using Rolle's theorem. Integrate its absolute bound to obtain \(M_2h^3/12\) locally and \((b-a)M_2h^2/12\) globally.

Show the real module calls and explain every `QuadratureResult` field. State that the bound is conditional on the proved derivative bound and excludes floating rounding.

- [ ] **Step 4: Add training, verify, and commit**

Add at least three examples, two immediate checks, exactly seven exercises, and nine folded answers. Include one invalid pointwise-derivative-bound diagnosis and one midpoint-versus-trapezoid comparison.

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_22.ChapterTwentyTwoTests.test_units_have_final_metadata_hours_anchors_and_training \
  tests.test_chapter_22.ChapterTwentyTwoTests.test_unit_four_has_both_second_derivative_error_constants \
  tests.test_quadrature -v
python3.12 scripts/check_content.py
```

Expected: Unit 22.4 and all shared algorithm tests pass.

```bash
git add content/chapters/chapter-22/u-05-22-04-midpoint-trapezoid.md
git commit -m "docs: derive midpoint and trapezoid error bounds"
```

### Task 8: Write Unit 22.5 Simpson certificates

**Files:**

- Create: `content/chapters/chapter-22/u-05-22-05-simpson-certificates.md`
- Test: `tests/test_chapter_22.py`
- Reuse: `src/mathbook_examples/quadrature.py`

- [ ] **Step 1: Add exact front matter**

```yaml
---
title: Simpson 方法怎样给出预算与误差证书？
unit_id: u-05-22-05
hours: {theory: 1.0, applied: 1.5}
difficulty: 5
prerequisites:
  book: [u-04-15-01, u-04-16-02, u-05-22-04]
  higher_algebra: [三次插值, 偶数取整, 四次根不等式]
  analytic_geometry: [双区间面板, 抛物线插值]
  python: [不可变结果, 状态字段, 预算参数]
capabilities: [composite_simpson, fourth_derivative_error, even_grid_budget, certificate_semantics]
learning_goals: [推出Simpson权重, 证明四阶误差界, 计算最小偶数预算, 区分误差界与目标达成]
content_standard: 2
---
```

- [ ] **Step 2: Derive Simpson and its panel error**

Derive weights \(1,4,1\) by integrating the quadratic interpolant over a two-subinterval panel. Verify exactness for \(1,x,x^2,x^3\).

For the panel \([m-h,m+h]\), define the Simpson error functional. Subtract the cubic interpolant and construct the auxiliary function whose coefficient matches the error. Apply Rolle four times to obtain

\[
E_{\mathrm{panel}}=-\frac{h^5}{90}f^{(4)}(\xi).
\]

Sum \(n/2\) panels to obtain

\[
|E_S|\le\frac{b-a}{180}M_4h^4.
\]

Do not cite an integral-remainder formula that has not been proved.

- [ ] **Step 3: Explain the budgeted implementation**

Derive

\[
n\ge\left(\frac{M_4(b-a)^5}{180\tau}\right)^{1/4}
\]

and then require the smallest positive even integer. Document `target_met`, `budget_exhausted`, `error_bound`, and the caller's derivative-bound obligation. Include one complete successful budget example and the anchored budget-exhaustion example.

- [ ] **Step 4: Add training, verify, and commit**

Add at least three examples, two immediate checks, exactly eight exercises, and ten folded answers. Include weight reconstruction, error-bound calculation, odd-grid rejection, smallest-even rounding, budget exhaustion, and false-certificate diagnosis.

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_22.ChapterTwentyTwoTests.test_units_have_final_metadata_hours_anchors_and_training \
  tests.test_chapter_22.ChapterTwentyTwoTests.test_unit_five_keeps_simpson_certificate_semantics \
  tests.test_quadrature -v
python3.12 scripts/check_content.py
```

Expected: Unit 22.5 and all shared algorithm tests pass.

```bash
git add content/chapters/chapter-22/u-05-22-05-simpson-certificates.md
git commit -m "docs: derive Simpson budgets and certificates"
```

### Task 9: Write Unit 22.6 certified improper quadrature

**Files:**

- Create: `content/chapters/chapter-22/u-05-22-06-certified-improper-quadrature.md`
- Test: `tests/test_chapter_22.py`
- Reuse: `src/mathbook_examples/quadrature.py`

- [ ] **Step 1: Add exact front matter**

```yaml
---
title: 反常积分怎样完成可靠数值计算？
unit_id: u-05-22-06
hours: {theory: 0.5, applied: 1.5}
difficulty: 5
prerequisites:
  book: [u-05-22-01, u-05-22-02, u-05-22-03, u-05-22-04, u-05-22-05]
  higher_algebra: [误差预算分配, 指数不等式, 四阶导数界]
  analytic_geometry: [截断区间, 尾部区域]
  python: [调用求积模块, 读取状态与误差界]
capabilities: [total_error_budget, tail_truncation, finite_quadrature, diagnostic_review, independent_verification]
learning_goals: [先证明反常收敛, 分配两类误差预算, 证明截断与导数界, 合并总误差证书]
content_standard: 2
---
```

- [ ] **Step 2: Add the total-error theorem and workflow**

State and prove:

\[
\left|I-Q_R\right|
\le
\left|\int_R^\infty f\right|
+
\left|\int_a^R f-Q_R\right|.
\]

Give the exact workflow: prove convergence, split tolerance, derive tail bound, choose \(R\), prove the finite-interval derivative bound, compute a grid budget, run the shared module, combine bounds, and report any unmet target.

- [ ] **Step 3: Add complete baseline and Gaussian examples**

For \(\int_0^\infty e^{-x}\,dx\), use tail \(e^{-R}\), fourth derivative bound \(1\) on \([0,R]\), and a concrete tolerance split.

For \(\int_0^\infty e^{-x^2}\,dx\), prove

\[
\int_R^\infty e^{-x^2}\,dx
\le\frac{e^{-R^2}}{2R}
\]

from \(x/R\ge1\). Compute

\[
f^{(4)}(x)=(16x^4-48x^2+12)e^{-x^2}
\]

and use the valid coarse bound \(M_4=16R^4+48R^2+12\) on \([0,R]\). Explain that a sharper proved bound may reduce the budget but an observed maximum from sampling is not a certificate.

Add the anchored grid-difference counterexample: two close approximations without a theorem do not yield a strict error bound.

- [ ] **Step 4: Add the locked exercise bank**

Add four immediate checks and exactly twelve exercises:

- `{#pr-u-05-22-06-mixed-1}` through `mixed-4`;
- `{#pr-u-05-22-06-diagnosis-1}` through `diagnosis-3`;
- `{#pr-u-05-22-06-boundary-1}` through `boundary-2`;
- `{#pr-u-05-22-06-verification-1}` through `verification-3`.

Add exactly sixteen folded answers, one after every immediate check and exercise. Each answer must show the convergence basis, tail bound, derivative-bound source, finite-rule bound, and final inequality when those items apply.

- [ ] **Step 5: Verify all content contracts and commit**

Run:

```bash
python3.12 -m unittest tests.test_chapter_22 tests.test_quadrature -v
python3.12 scripts/check_content.py
```

Expected: algorithm tests pass; all Chapter 22 content tests pass except publication-surface assertions.

```bash
git add content/chapters/chapter-22/u-05-22-06-certified-improper-quadrature.md
git commit -m "docs: add certified improper quadrature practice"
```

### Task 10: Publish Chapter 22 and close Part V

**Files:**

- Modify: `README.md`
- Modify: `content/course-map.md`
- Modify: `docs/curriculum/part-05-dependencies.md`
- Modify: `docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md`
- Modify: `mkdocs.yml`
- Modify: `scripts/check_site.py`
- Modify: `tests/test_chapter_15.py`
- Modify: `tests/test_chapter_16.py`
- Modify: `tests/test_chapter_17.py`
- Modify: `tests/test_chapter_18.py`
- Modify: `tests/test_chapter_19.py`
- Modify: `tests/test_chapter_20.py`
- Modify: `tests/test_chapter_21.py`
- Modify: `tests/test_part_04_consistency.py`
- Modify: `tests/test_zensical_structure.py`
- Modify: `tests/test_mkdocs_site.py`
- Test: `tests/test_chapter_22.py`

- [ ] **Step 1: Add navigation and course-map entries**

In `mkdocs.yml`, append after Chapter 21:

```yaml
- 第 22 章：反常积分与数值求积:
  - 章节导学: chapters/chapter-22/index.md
  - 反常积分怎样由逐端点极限定义？: chapters/chapter-22/u-05-22-01-improper-definition.md
  - 正函数怎样比较收敛并控制尾部？: chapters/chapter-22/u-05-22-02-comparison-tests.md
  - 绝对、条件与振荡收敛怎样区分？: chapters/chapter-22/u-05-22-03-absolute-conditional-oscillation.md
  - 中点与梯形公式怎样产生可证明误差界？: chapters/chapter-22/u-05-22-04-midpoint-trapezoid.md
  - Simpson 方法怎样给出预算与误差证书？: chapters/chapter-22/u-05-22-05-simpson-certificates.md
  - 反常积分怎样完成可靠数值计算？: chapters/chapter-22/u-05-22-06-certified-improper-quadrature.md
```

Add a Chapter 22 course-map section with `本章学时：12 小时（理论 7.25，应用 4.75）。`, the six links once each, the two routes, and a statement that Part V is closed.

- [ ] **Step 2: Update release and dependency surfaces**

Update README to `第五部第 22 章，共 98 个学习单元`.

Update `docs/curriculum/part-05-dependencies.md`:

- scope `25 个核心单元，42.5 学时`;
- current boundary `第 22 章，第五部已闭合`;
- replace the five old Chapter 22 rows with the six approved rows;
- add `u-05-22-06` depending on `u-05-22-01`–`05`, with the unique output “尾部截断、有限求积与总误差证书”;
- retain the rules that endpoints are separate, principal value is not usual convergence, grid differences are not certificates, and infinite-series interchange is out of scope;
- add the Part V closure table with theory `27.00`, application `15.50`, total `42.50`.

Update only the current-total table and explanatory current-baseline sentence in the master design to `292.75 + 101.25 = 394`.

- [ ] **Step 3: Update rendered-site dictionaries**

In `scripts/check_site.py`, register the Chapter 22 guide and six pages. Require these representative anchors:

- `thm-u-05-22-01-cauchy-tail-criterion`;
- `thm-u-05-22-03-dirichlet-test`;
- `thm-u-05-22-05-simpson-error`;
- `alg-u-05-22-06-total-error-workflow`.

Require Chapter 22 navigation labels on representative pages and preserve the existing Chapter 18–21 checks.

- [ ] **Step 4: Update stale global assertions**

Use:

```bash
rg -n "第 21 章|92 个|24 个核心单元|40\\.5 学时|292\\D+100\\D+392|\\*\\*392\\*\\*" tests README.md content/course-map.md docs/curriculum docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md
```

Change only assertions and live-current statements. Keep historical design narratives when they explicitly describe an earlier approved state. Update release assertions in Chapter 15–21 tests, Part IV consistency tests, Zensical structure tests, and rendered-site tests to the new current surface.

- [ ] **Step 5: Run publication gates**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_15 \
  tests.test_chapter_16 \
  tests.test_chapter_17 \
  tests.test_chapter_18 \
  tests.test_chapter_19 \
  tests.test_chapter_20 \
  tests.test_chapter_21 \
  tests.test_chapter_22 \
  tests.test_quadrature \
  tests.test_part_04_consistency \
  tests.test_zensical_structure \
  tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: all focused tests pass, content validation reports no errors, strict build says `No issues found`, site validation exits zero, and diff check is empty.

- [ ] **Step 6: Commit**

```bash
git add README.md content/course-map.md docs/curriculum/part-05-dependencies.md \
  docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md \
  mkdocs.yml scripts/check_site.py tests
git commit -m "docs: publish chapter 22 and close part 5"
```

### Task 11: Audit Chapter 22 and Part V, then run the full quality gate

**Files:**

- Create: `docs/reviews/2026-07-30-chapter-22-and-part-05-consistency-review.md`
- Verify: all files above

- [ ] **Step 1: Count the delivered contracts**

Run:

```bash
rg -c '\{#pr-u-05-22-' content/chapters/chapter-22/u-05-22-*.md
rg -F -c '??? note "答案"' content/chapters/chapter-22/u-05-22-*.md
rg -n 'thm-u-05-22-01-cauchy-tail-criterion|thm-u-05-22-03-dirichlet-test|thm-u-05-22-05-simpson-error|alg-u-05-22-06-total-error-workflow' site
```

Expected exercise counts: `6, 7, 8, 7, 8, 12`. Expected answer counts: `8, 9, 10, 9, 10, 16`. All four representative anchors exist in rendered HTML.

- [ ] **Step 2: Write the consistency review**

The review must record:

- scope, date, release boundary, and conclusion;
- no unresolved high- or medium-priority findings;
- endpoint-by-endpoint definition and Cauchy-tail proof status;
- comparison direction, limit-comparison conditions, and tail-bound status;
- absolute/conditional/Dirichlet/Abel/principal-value boundary status;
- midpoint `1/24`, trapezoid `1/12`, and Simpson `1/180` constants;
- caller-proved derivative-bound obligation and floating-error exclusion;
- budgeted algorithm statuses and single-source check;
- Unit 22.6 total-error workflow;
- exact 48/62 training counts and the 4/3/2/3 comprehensive categories;
- Chapter 22 `7.25 + 4.75 = 12`;
- Part V `25` units and `42.5` hours;
- release at Chapter 22 and `98` published units;
- current whole-book `292.75 + 101.25 = 394`;
- no Part VI blank pages;
- final test, content, build, site, anchor, and diff evidence.

- [ ] **Step 3: Run fresh full verification**

Run:

```bash
make verify
git diff --check
git status --short
```

Expected: all tests pass; content, strict build, and site checks pass; diff check is empty; only the untracked review file remains.

- [ ] **Step 4: Commit the review and verify again**

```bash
git add docs/reviews/2026-07-30-chapter-22-and-part-05-consistency-review.md
git commit -m "docs: verify chapter 22 and part 5 consistency"
make verify
git diff --check
git status --short
```

Expected: full verification passes after the final commit and the worktree is clean.

- [ ] **Step 5: Hand off the branch**

Use `superpowers:verification-before-completion`, then `superpowers:finishing-a-development-branch`. Confirm that Chapter 22 started from the accepted Chapter 21 tip `e5eae35`, and that the integration target is `main`. Present exactly:

1. Merge back to `main` locally;
2. Push and create a Pull Request;
3. Keep the branch as-is;
4. Discard the work.

Do not merge, push, delete the branch, remove the worktree, or start Part VI without the user's explicit choice.
