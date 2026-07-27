# Chapter 17 Convexity, Newton, and Part IV Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Chapter 17 as four self-study units with a tested pure/safeguarded Newton implementation, then audit and reconcile all of Part IV before release.

**Architecture:** Markdown remains the single teaching source, while `src/mathbook_examples/newton.py` is the single executable Newton implementation. Chapter tests freeze the mathematical/content contract before pages exist; algorithm tests freeze result semantics and safeguards before implementation. After the chapter passes its own gate, a Part IV consistency test, dependency document, and manual review report reconcile Chapters 13–17 and their Chapter 12/18 interfaces.

**Tech Stack:** Python 3.12 standard library, `unittest`, frozen dataclasses, PyYAML, Markdown with Material/Zensical extensions, Zensical strict build.

---

## File map

**Create**

- `content/chapters/chapter-17/index.md` — chapter question arc, dependencies, unit order, hours, outputs, and boundaries.
- `content/chapters/chapter-17/u-04-17-01-function-shape.md` — derivative sign charts, extrema, concavity, and inflection points.
- `content/chapters/chapter-17/u-04-17-02-convexity-optimization.md` — convexity definitions, equivalences, supporting lines, and global minimization.
- `content/chapters/chapter-17/u-04-17-03-newton-convergence-failure.md` — Newton derivation, strong interval theorem, local quadratic convergence, repeated roots, and failure.
- `content/chapters/chapter-17/u-04-17-04-safeguarded-newton.md` — algorithm workflow, certificate semantics, source usage, and method comparison.
- `src/mathbook_examples/newton.py` — frozen result type, pure Newton, safeguarded Newton, validation, and bracket helpers.
- `tests/test_chapter_17.py` — metadata, hours, anchors, proof/case markers, boundaries, and publication contract.
- `tests/test_newton.py` — pure and safeguarded Newton behavior, failure, convergence-rate, invariant, and certificate tests.
- `tests/test_part_04_consistency.py` — Part IV totals, unit uniqueness, design/dependency/publication synchronization, and certificate-source boundaries.
- `docs/curriculum/part-04-dependencies.md` — Chapter 12 → Chapters 13–17 → Chapter 18 dependency and unique-placement map.
- `docs/reviews/2026-07-27-part-04-consistency-review.md` — 20-unit manual review matrix, findings, repairs, evidence, and remaining limitations.

**Modify**

- `docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md` — reconcile Part IV and whole-book hours to the current expanded baseline.
- `docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md` — set Chapter 17 to 8 hours, Part IV to 36.5 hours, and remove stale 34/35.5-hour statements.
- `mkdocs.yml` — publish the Chapter 17 guide and four units after Chapter 16.
- `content/course-map.md` — add Chapter 17 and close the published Part IV route.
- `README.md` — change the release boundary to Chapter 17 and the published unit count to 72.
- `scripts/check_site.py` — add a representative Chapter 17 page, anchors, and navigation markers.
- `tests/test_chapter_15.py` — replace stale Part IV/release totals with the final values.
- `tests/test_chapter_16.py` — replace the Chapter 16 release-boundary assertion with the completed Part IV boundary.
- `tests/test_zensical_structure.py` — expect the completed Chapter 17/72-unit publication statement.

## Task 1: Freeze the Chapter 17 teaching contract

**Files:**

- Create: `tests/test_chapter_17.py`

- [ ] **Step 1: Write the failing metadata, anchor, proof, and boundary tests**

Create `tests/test_chapter_17.py` with this contract:

```python
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-17"

EXPECTED_UNITS = [
    (
        "u-04-17-01",
        "导数怎样还原函数的增减、极值与弯曲形态？",
        1.50,
        0.50,
        "function-shape",
    ),
    (
        "u-04-17-02",
        "凸性为何能把局部极小升级为整体极小？",
        1.50,
        0.50,
        "convexity-optimization",
    ),
    (
        "u-04-17-03",
        "Newton 迭代为什么可能快速收敛，也可能失败？",
        1.25,
        0.75,
        "newton-convergence-failure",
    ),
    (
        "u-04-17-04",
        "怎样实现具有保护机制和停止证书的 Newton 算法？",
        0.25,
        1.75,
        "safeguarded-newton",
    ),
]

REQUIRED_ANCHORS = {
    "u-04-17-01": (
        "thm-u-04-17-01-first-derivative-test",
        "thm-u-04-17-01-second-derivative-test",
        "def-u-04-17-01-inflection",
    ),
    "u-04-17-02": (
        "def-u-04-17-02-convex",
        "thm-u-04-17-02-supporting-line",
        "thm-u-04-17-02-derivative-monotone",
        "thm-u-04-17-02-strict-minimizer",
    ),
    "u-04-17-03": (
        "thm-u-04-17-03-interval-newton",
        "thm-u-04-17-03-quadratic-convergence",
        "thm-u-04-17-03-multiple-root",
        "ex-u-04-17-03-two-cycle",
    ),
    "u-04-17-04": (
        "alg-u-04-17-04-safeguarded-newton",
        "thm-u-04-17-04-bracket-contraction",
        "def-u-04-17-04-verifiable-certificate",
        "tbl-u-04-17-04-certificate-comparison",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "Riemann 积分",
    "积分型 Taylor 余项",
    "幂级数展开",
    "多元 Newton",
    "Fréchet",
)


def unit_path(unit):
    unit_id, _title, _theory, _applied, suffix = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path):
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterSeventeenTests(unittest.TestCase):
    def test_units_have_final_metadata_hours_and_anchors(self):
        theory = 0.0
        applied = 0.0
        for unit in EXPECTED_UNITS:
            unit_id, title, theory_hours, applied_hours, _suffix = unit
            path = unit_path(unit)
            with self.subTest(unit=unit_id):
                self.assertTrue(path.is_file(), f"missing {path.name}")
                if not path.is_file():
                    continue
                metadata, text = read_unit(path)
                self.assertEqual(unit_id, metadata["unit_id"])
                self.assertEqual(title, metadata["title"])
                self.assertEqual(theory_hours, metadata["hours"]["theory"])
                self.assertEqual(applied_hours, metadata["hours"]["applied"])
                self.assertEqual(2, metadata["content_standard"])
                for anchor in REQUIRED_ANCHORS[unit_id]:
                    self.assertIn(f"{{#{anchor}}}", text)
                theory += metadata["hours"]["theory"]
                applied += metadata["hours"]["applied"]
        self.assertEqual(4.5, theory)
        self.assertEqual(3.5, applied)

    def test_chapter_guide_lists_units_hours_and_boundaries(self):
        guide = (CHAPTER / "index.md").read_text(encoding="utf-8")
        self.assertIn("本章共4个核心单元，8学时（理论4.5，应用3.5）。", guide)
        self.assertIn("第 12 章", guide)
        self.assertIn("第 18 章", guide)
        self.assertIn("不引入积分型余项、无穷级数或多元方法", guide)
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_shape_unit_keeps_candidate_and_inflection_boundaries(self):
        text = unit_path(EXPECTED_UNITS[0]).read_text(encoding="utf-8")
        for marker in (
            "第 15.2 单元已经证明",
            "端点、驻点和不可导点",
            "局部极值不自动是整体极值",
            r"f''(x_0)=0",
            "凹凸性发生改变",
            r"x^4",
        ):
            self.assertIn(marker, text)

    def test_convexity_unit_separates_existence_and_uniqueness(self):
        text = unit_path(EXPECTED_UNITS[1]).read_text(encoding="utf-8")
        for marker in (
            "弦不等式",
            "支撑线不等式",
            "当且仅当",
            "至多有一个整体极小点",
            "不保证极小点存在",
            r"e^x-x",
        ):
            self.assertIn(marker, text)

    def test_newton_unit_keeps_local_and_global_assumptions(self):
        text = unit_path(EXPECTED_UNITS[2]).read_text(encoding="utf-8")
        for marker in (
            r"f(a)f(b)<0",
            r"f(x_0)f''(x_0)>0",
            r"|f'(x)|\ge \mu>0",
            r"|e_{n+1}|\le \frac{M}{2\mu}|e_n|^2",
            r"1-\frac1m",
            r"x^3-x-1",
            r"x^3-2x+2",
            r"(x-1)^2",
            "局部结论",
        ):
            self.assertIn(marker, text)

    def test_algorithm_unit_distinguishes_stop_signal_and_certificate(self):
        text = unit_path(EXPECTED_UNITS[3]).read_text(encoding="utf-8")
        for marker in (
            "可验证误差证书",
            "连续性由调用者证明",
            "程序能够检查",
            r"[a+w/4,b-w/4]",
            r"\left(\frac34\right)^n",
            "converged",
            "certified",
            "step_types",
            "src/mathbook_examples/newton.py",
            "safeguarded_newton",
        ):
            self.assertIn(marker, text)

    def test_core_does_not_use_later_topics(self):
        for unit in EXPECTED_UNITS:
            path = unit_path(unit)
            if not path.is_file():
                continue
            core = path.read_text(encoding="utf-8").split(
                "## 常见误区与后续", 1
            )[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)
```

- [ ] **Step 2: Run the contract tests and verify the missing chapter failure**

Run:

```bash
python3.12 -m unittest tests.test_chapter_17 -v
```

Expected: FAIL because `content/chapters/chapter-17/` and its five Markdown files do not yet exist.

- [ ] **Step 3: Commit the red contract**

```bash
git add tests/test_chapter_17.py
git commit -m "test: define chapter 17 content contract"
```

## Task 2: Implement pure Newton with diagnostic results

**Files:**

- Create: `tests/test_newton.py`
- Create: `src/mathbook_examples/newton.py`

- [ ] **Step 1: Write failing tests for result semantics and pure Newton**

Create `tests/test_newton.py` with imports from `src`, then add tests that require:

```python
from dataclasses import FrozenInstanceError
from math import inf, isclose, nan

from mathbook_examples.newton import NewtonResult, newton


def cubic(point):
    return point**3 - point - 1


def cubic_prime(point):
    return 3 * point**2 - 1
```

The tests must assert:

```python
result = newton(cubic, cubic_prime, 1.5)
self.assertIsInstance(result, NewtonResult)
self.assertTrue(result.converged)
self.assertFalse(result.certified)
self.assertEqual("residual", result.reason)
self.assertLess(result.residual, 1e-10)
self.assertIsNone(result.bracket)
self.assertIsNone(result.error_bound)
self.assertTrue(all(step == "newton" for step in result.step_types))
self.assertTrue(isclose(result.value, 1.3247179572447458, abs_tol=1e-10))
```

Also cover:

- assigning to a result field raises `FrozenInstanceError`;
- `newton(lambda x: x - 2, lambda x: 1, 2)` stops at iteration 0 by
  `residual`;
- `newton(lambda x: x * x + 1, lambda x: 2 * x, 0)` returns
  `derivative_too_small`, `converged=False`;
- non-finite initial function or derivative values return `nonfinite_value`;
- \(x^3-2x+2\) from `0` alternates `0,1,0,1` and exits by
  `max_iterations`;
- a deliberately loose `step_tolerance` can exit by `step` while remaining
  `certified=False`;
- iteration-zero results have `last_step=None`; after a completed update,
  `last_step` is the absolute distance between the final two iterates;
- invalid arguments raise these exact messages:

```text
initial must be finite
residual_tolerance must be positive and finite
step_tolerance must be positive and finite
derivative_tolerance must be positive and finite
max_iterations must be a positive integer
```

- [ ] **Step 2: Run the pure Newton tests and verify the import failure**

Run:

```bash
python3.12 -m unittest tests.test_newton -v
```

Expected: FAIL with `ModuleNotFoundError` for `mathbook_examples.newton`.

- [ ] **Step 3: Implement the frozen result and validation helpers**

Start `src/mathbook_examples/newton.py` with:

```python
"""Pure and safeguarded Newton iterations with explicit certificate semantics."""

from collections.abc import Callable
from dataclasses import dataclass
from math import inf, isfinite


@dataclass(frozen=True)
class NewtonResult:
    value: float
    converged: bool
    certified: bool
    iterations: int
    reason: str
    residual: float
    last_step: float | None
    bracket: tuple[float, float] | None
    error_bound: float | None
    step_types: tuple[str, ...]


def _positive_finite(value: float, name: str) -> None:
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")


def _iteration_budget(value: int) -> None:
    if type(value) is not int or value <= 0:
        raise ValueError("max_iterations must be a positive integer")


def _failure(
    value: float,
    iterations: int,
    reason: str,
    residual: float,
    last_step: float | None,
    step_types: list[str],
) -> NewtonResult:
    return NewtonResult(
        value=value,
        converged=False,
        certified=False,
        iterations=iterations,
        reason=reason,
        residual=residual,
        last_step=last_step,
        bracket=None,
        error_bound=None,
        step_types=tuple(step_types),
    )
```

- [ ] **Step 4: Implement the minimal pure Newton loop**

Implement this exact public signature:

```python
def newton(
    function: Callable[[float], float],
    derivative: Callable[[float], float],
    initial: float,
    *,
    residual_tolerance: float = 1e-12,
    step_tolerance: float = 1e-12,
    derivative_tolerance: float = 1e-14,
    max_iterations: int = 50,
) -> NewtonResult:
```

The loop must:

1. validate the initial point and all three tolerances;
2. evaluate the initial residual before taking a step;
3. return `nonfinite_value` rather than raise when the supplied function or
   derivative produces a non-finite iteration value;
4. test derivative magnitude before division;
5. append `"newton"` only after a finite candidate and finite candidate
   function value have been obtained;
6. test residual before step length so an exact root reports `residual`;
7. return the last finite iterate on diagnostic failure;
8. use `inf` as residual only when no finite residual is available;
9. return `max_iterations` with the final finite state after the budget.

- [ ] **Step 5: Run the pure Newton tests**

Run:

```bash
python3.12 -m unittest tests.test_newton -v
```

Expected: all pure Newton tests PASS; safeguarded tests have not been added yet.

- [ ] **Step 6: Commit the pure implementation**

```bash
git add tests/test_newton.py src/mathbook_examples/newton.py
git commit -m "feat: add diagnostic pure Newton iteration"
```

## Task 3: Add safeguarded Newton and certificate tests

**Files:**

- Modify: `tests/test_newton.py`
- Modify: `src/mathbook_examples/newton.py`

- [ ] **Step 1: Add failing safeguard, invariant, and certificate tests**

Import `safeguarded_newton` and add tests for:

```python
result = safeguarded_newton(
    lambda x: x * x - 2,
    lambda x: 2 * x,
    1.0,
    2.0,
    interval_tolerance=1e-12,
)
self.assertTrue(result.converged)
self.assertTrue(result.certified)
self.assertEqual("bracket", result.reason)
self.assertLessEqual(result.error_bound, 5e-13)
self.assertIn("newton", result.step_types)
self.assertLessEqual(abs(result.value - 2**0.5), result.error_bound)
```

Add the following independent cases:

- an exact left or right endpoint root returns `endpoint`, zero iterations,
  `certified=True`, and `error_bound=0`;
- an exact interior candidate root returns `endpoint`, a collapsed bracket
  `(candidate, candidate)`, and `error_bound=0`;
- an initially narrow enough valid bracket returns `bracket` at iteration zero;
- unordered endpoints, non-finite endpoints, same-sign endpoint values,
  non-finite endpoint function values, and invalid tolerances raise these exact
  messages:

```text
endpoints must be finite
left endpoint must be smaller than right endpoint
function value at left endpoint must be finite
function value at right endpoint must be finite
endpoint values must have opposite signs
interval_tolerance must be positive and finite
derivative_tolerance must be positive and finite
max_iterations must be a positive integer
```

- \(x^3-2x+2\) on \([-2,-1]\) rejects the first outside-central-region
  Newton candidate and records `"bisection"`;
- \(x^2-2\) on \([1,2]\) accepts the first Newton candidate \(1.5\);
- a derivative of zero or a non-finite derivative falls back to bisection;
- a non-finite accepted Newton function value retries the midpoint before
  reporting failure;
- for budgets \(n=1,\ldots,8\), the returned bracket still changes sign and
  its midpoint error bound is at most
  \(\tfrac12(3/4)^n(b_0-a_0)\);
- budget exhaustion returns `max_iterations`, `converged=False`,
  `certified=True`, the midpoint of the final bracket, and its valid
  half-width bound;
- the `step_types` length equals the number of completed candidate
  evaluations.

- [ ] **Step 2: Run the new tests and verify the missing API failure**

Run:

```bash
python3.12 -m unittest tests.test_newton -v
```

Expected: FAIL because `safeguarded_newton` is not defined.

- [ ] **Step 3: Add overflow-aware bracket helpers**

Add:

```python
def _midpoint(left: float, right: float) -> float:
    if left < 0.0 < right:
        return (left + right) / 2.0
    return left + (right - left) / 2.0


def _half_width(left: float, midpoint: float, right: float) -> float:
    return max(midpoint - left, right - midpoint)


def _same_sign(first: float, second: float) -> bool:
    return (first > 0.0) == (second > 0.0)
```

Compute the central acceptance interval without directly multiplying an
overflowing width:

```python
midpoint = _midpoint(left, right)
central_left = _midpoint(left, midpoint)
central_right = _midpoint(midpoint, right)
accepted = central_left <= candidate <= central_right
```

- [ ] **Step 4: Implement safeguarded Newton**

Use this signature and document that continuity is a caller-proved
precondition:

```python
def safeguarded_newton(
    function: Callable[[float], float],
    derivative: Callable[[float], float],
    left: float,
    right: float,
    *,
    interval_tolerance: float = 1e-10,
    derivative_tolerance: float = 1e-14,
    max_iterations: int = 100,
) -> NewtonResult:
```

Implement this order:

1. validate numeric parameters and finite ordered endpoints;
2. evaluate finite endpoint values and handle exact endpoint roots;
3. reject same-sign endpoints;
4. return the initial midpoint immediately if the already-valid interval meets
   `interval_tolerance`;
5. choose the endpoint with smaller residual as the first Newton base point;
6. form a Newton candidate only for a finite derivative above the threshold;
7. accept it only inside the central half; otherwise use the midpoint;
8. if an accepted Newton candidate gives a non-finite function value, retry
   the midpoint and record only the completed bisection step;
9. if even the midpoint value is non-finite, return `nonfinite_value`,
   `converged=False`, `certified=False`;
10. if the finite candidate is an exact root, return `endpoint` with a
    collapsed bracket and zero error;
11. update the sign-changing bracket after each finite non-root candidate;
12. stop when the full interval width is at most `interval_tolerance`, evaluate
    and return its midpoint, and compute the half-width with `_half_width`;
13. on budget exhaustion evaluate and return the current midpoint and
    half-width with `converged=False`, `certified=True`;
14. if a final returned midpoint has a non-finite function value, return
    `nonfinite_value`, `converged=False`, `certified=False`.

- [ ] **Step 5: Run algorithm and full Python tests**

Run:

```bash
python3.12 -m unittest tests.test_newton -v
python3.12 -m unittest discover -s tests -v
```

Expected: all tests PASS.

- [ ] **Step 6: Commit the protected algorithm**

```bash
git add tests/test_newton.py src/mathbook_examples/newton.py
git commit -m "feat: add safeguarded Newton certificates"
```

## Task 4: Write Unit 17.1 on complete function-shape analysis

**Files:**

- Create: `content/chapters/chapter-17/u-04-17-01-function-shape.md`

- [ ] **Step 1: Create exact v2 front matter and section skeleton**

Use:

```yaml
---
title: 导数怎样还原函数的增减、极值与弯曲形态？
unit_id: u-04-17-01
hours: {theory: 1.50, applied: 0.50}
difficulty: 3
prerequisites:
  book: [u-04-15-02, u-04-16-02]
  higher_algebra: [多项式因式分解, 不等式与符号表]
  analytic_geometry: [函数图像, 切线, 凹凸与曲率直观]
  python: [函数, 条件分支, 数值表格]
capabilities: [proof, shape_analysis, counterexample, interpretation]
learning_goals: [建立完整候选点清单, 使用一阶与二阶判别, 判断凹凸区间与拐点, 区分局部与整体结论]
content_standard: 2
---
```

Include every required v2 heading in the repository’s standard order.

- [ ] **Step 2: Write the dependency-aware theory**

The theory section must:

- cite rather than reprove the Fermat and derivative-sign monotonicity theorems
  from Unit 15.2;
- give a complete candidate checklist: endpoints, stationary points,
  nondifferentiable domain points, and domain boundaries;
- prove the first-derivative sign-change test;
- prove the second-derivative test from the Chapter 16 Taylor expansion,
  including the inconclusive \(f''(x_0)=0\) case;
- define convex-up/convex-down intervals consistently with Unit 17.2;
- define an inflection point by a change of concavity, not by a zero second
  derivative.

- [ ] **Step 3: Add examples, checks, exercises, and complete answers**

Use these anchored examples:

- `{#ex-u-04-17-01-cubic-shape}` — complete sign chart and shape analysis of
  \(f(x)=x^3-3x\);
- `{#ex-u-04-17-01-zero-second-derivative}` — compare \(x^3\) and \(x^4\) at
  zero to separate “\(f''=0\)” from an actual inflection point.

Add two immediate checks and five graded exercises. At least one exercise must
analyze a closed interval and include endpoint comparison; at least one must
include a nondifferentiable candidate; at least one must ask for a counterexample
to a false converse. Supply seven page-local collapsed full answers.

- [ ] **Step 4: Run the unit contract and content checker**

Run:

```bash
python3.12 -m unittest tests.test_chapter_17.ChapterSeventeenTests.test_shape_unit_keeps_candidate_and_inflection_boundaries -v
python3.12 scripts/check_content.py
```

Expected: the shape-unit test PASS; the content checker PASS for all published
units.

- [ ] **Step 5: Commit Unit 17.1**

```bash
git add content/chapters/chapter-17/u-04-17-01-function-shape.md
git commit -m "docs: add derivative-based function shape unit"
```

## Task 5: Write Unit 17.2 on convexity and global optimization

**Files:**

- Create: `content/chapters/chapter-17/u-04-17-02-convexity-optimization.md`

- [ ] **Step 1: Create exact v2 front matter**

Use theory/application hours `1.50/0.50`, `difficulty: 3`, book prerequisite
`u-04-17-01`, and learning goals covering the chord definition, supporting
lines, derivative monotonicity, second-derivative criterion, and unique global
minimizers.

- [ ] **Step 2: Write the complete convexity proof chain**

Use the anchors frozen in Task 1 and prove, in order:

1. the chord-inequality definition on an interval;
2. the supporting-line inequality for differentiable convex functions;
3. differentiable \(f\) is convex if and only if \(f'\) is nondecreasing;
4. the second-derivative criterion;
5. a strictly convex function has at most one global minimizer;
6. a stationary point of a differentiable strictly convex function, when it
   exists, is its unique global minimizer.

State separately how compactness/continuity or explicit coercive behavior can
provide existence. Never write that strict convexity alone guarantees
attainment.

- [ ] **Step 3: Integrate the approved cases and v2 practice**

Use:

- `{#ex-u-04-17-02-exp-minus-linear}` — prove that \(e^x-x\) is strictly
  convex and has the unique global minimum \(1\) at \(x=0\);
- `{#ex-u-04-17-02-strict-with-zero-second}` — prove \(x^4\) is strictly
  convex even though \(f''(0)=0\).

Add two immediate checks, five exercises, and seven complete collapsed answers.
Include one exercise on a convex but not strictly convex function, one on a
strictly convex function without an attained minimum on its domain, and one
supporting-line inequality.

- [ ] **Step 4: Run the unit tests and content checker**

Run:

```bash
python3.12 -m unittest tests.test_chapter_17.ChapterSeventeenTests.test_convexity_unit_separates_existence_and_uniqueness -v
python3.12 scripts/check_content.py
```

Expected: PASS.

- [ ] **Step 5: Commit Unit 17.2**

```bash
git add content/chapters/chapter-17/u-04-17-02-convexity-optimization.md
git commit -m "docs: add convexity and global optimization unit"
```

## Task 6: Write Unit 17.3 on Newton convergence and failure

**Files:**

- Create: `content/chapters/chapter-17/u-04-17-03-newton-convergence-failure.md`

- [ ] **Step 1: Create exact v2 front matter**

Use theory/application hours `1.25/0.75`, `difficulty: 4`, book prerequisites
`u-04-16-02` and `u-04-17-02`, and Python prerequisites covering functions,
loops, tuples, and floating-point values.

- [ ] **Step 2: Derive Newton and prove the strong interval theorem**

Derive the tangent-intercept formula before showing code. State all strong
interval assumptions exactly as in the design, then prove:

- the root is unique because \(f'\) does not vanish and therefore has fixed
  sign;
- the tangent geometry and fixed sign of \(f''\) keep the iterates on one side
  of the root and inside the interval;
- the sequence is monotone and bounded;
- its limit is the unique root.

Use \(x^3-x-1\) on \([1,2]\) as the main successful example and identify which
endpoint satisfies \(f(x_0)f''(x_0)>0\).

- [ ] **Step 3: Prove local quadratic convergence and repeated-root loss**

Use Taylor with Lagrange remainder around a simple root to derive

\[
|e_{n+1}|\le \frac{M}{2\mu}|e_n|^2.
\]

Explain the invariant-neighborhood requirement. Then factor
\(f(x)=(x-r)^m g(x)\), with \(g(r)\ne0\), and derive

\[
e_{n+1}=\left(1-\frac1m\right)e_n+O(e_n^2).
\]

For \((x-1)^2\), compute the exact recurrence
\(x_{n+1}-1=(x_n-1)/2\).

- [ ] **Step 4: Add the pure-Newton failure story and v2 practice**

Create `{#ex-u-04-17-03-two-cycle}` and calculate explicitly:

\[
N(0)=1,\qquad N(1)=0
\]

for \(f(x)=x^3-2x+2\). Explain why a finite plot or a few successful starts
cannot prove global convergence.

Add at least two other anchored examples total, two immediate checks, five
graded exercises, and seven collapsed full answers. Include exercises on a
zero derivative, a bad initial value, and distinguishing linear from quadratic
error ratios.

- [ ] **Step 5: Run chapter and content tests**

Run:

```bash
python3.12 -m unittest tests.test_chapter_17.ChapterSeventeenTests.test_newton_unit_keeps_local_and_global_assumptions -v
python3.12 scripts/check_content.py
```

Expected: PASS.

- [ ] **Step 6: Commit Unit 17.3**

```bash
git add content/chapters/chapter-17/u-04-17-03-newton-convergence-failure.md
git commit -m "docs: add Newton convergence and failure unit"
```

## Task 7: Write Unit 17.4 on safeguarded Newton and certificates

**Files:**

- Create: `content/chapters/chapter-17/u-04-17-04-safeguarded-newton.md`

- [ ] **Step 1: Create exact v2 front matter**

Use theory/application hours `0.25/1.75`, `difficulty: 4`, book prerequisites
`u-03-12-02`, `u-04-17-02`, and `u-04-17-03`, and capabilities covering
algorithmic thinking, invariant proofs, error analysis, experiments, and
interpretation.

- [ ] **Step 2: Write the fixed algorithm exposition**

Follow this order:

\[
\text{问题来源}
\to
\text{数学转化}
\to
\text{算法思想}
\to
\text{误差与适用条件}
\to
\text{伪代码}
\to
\text{Python 调用}
\to
\text{结果解释}.
\]

Define “可验证误差证书” at
`{#def-u-04-17-04-verifiable-certificate}`. Explicitly separate:

- caller-proved continuity;
- program-checked finite ordered endpoints and sign change;
- residual and step stopping signals;
- interval half-width error bounds.

- [ ] **Step 3: Prove the safeguard invariant and contraction**

At `{#alg-u-04-17-04-safeguarded-newton}`, give pseudocode with the accepted
region \([a+w/4,b-w/4]\). At
`{#thm-u-04-17-04-bracket-contraction}`, prove the sign-changing invariant and

\[
b_n-a_n\le(3/4)^n(b_0-a_0).
\]

Explain why a budget-exhausted result can be `converged=False` while retaining
`certified=True` and a wider valid bound.

- [ ] **Step 4: Use the tested source and compare guarantees**

Reference only `src/mathbook_examples/newton.py`. Show calls for:

- pure Newton on \(x^3-x-1\);
- the pure two-cycle for \(x^3-2x+2\);
- safeguarded Newton on \([-2,-1]\);
- a budget-exhausted result with a valid bracket certificate.

At `{#tbl-u-04-17-04-certificate-comparison}`, compare IVT, bisection, pure
Newton, safeguarded Newton, and strict convex optimization across existence,
uniqueness, convergence, error bound, and speed. Every positive entry must name
its conditions.

- [ ] **Step 5: Add v2 examples and practice**

Provide at least two anchored examples, two immediate checks, five exercises,
and seven complete collapsed answers. Include one trace reconstruction, one
central-region acceptance decision, one worst-case iteration bound, one invalid
certificate claim to diagnose, and one method-selection problem.

- [ ] **Step 6: Run algorithm-unit and source tests**

Run:

```bash
python3.12 -m unittest tests.test_chapter_17.ChapterSeventeenTests.test_algorithm_unit_distinguishes_stop_signal_and_certificate -v
python3.12 -m unittest tests.test_newton -v
python3.12 scripts/check_content.py
```

Expected: PASS.

- [ ] **Step 7: Commit Unit 17.4**

```bash
git add content/chapters/chapter-17/u-04-17-04-safeguarded-newton.md
git commit -m "docs: add safeguarded Newton algorithm unit"
```

## Task 8: Add the Chapter 17 guide and close the chapter contract

**Files:**

- Create: `content/chapters/chapter-17/index.md`
- Modify: `tests/test_chapter_17.py`

- [ ] **Step 1: Write the guide**

The guide must contain:

- `# 第 17 章：凸性、优化、函数形态与 Newton 方法 {#chapter-17}`;
- the exact 4-unit/8-hour sentence;
- four links in the approved order and their hour splits;
- the proof ladder from derivative signs to certificates;
- the roles of all four approved cases;
- inherited results from Chapters 12, 15, and 16;
- the Chapter 18 handoff;
- the explicit boundary sentence
  `不引入积分型余项、无穷级数或多元方法`;
- a chapter self-check list that distinguishes existence, uniqueness,
  convergence, and certified error.

- [ ] **Step 2: Add the final guide/publication assertions**

Extend `tests/test_chapter_17.py` to assert that:

- the guide lists each unit exactly once;
- `README.md` will say `第四部第 17 章，共 72 个学习单元`;
- the Part IV design will contain the exact Chapter 17 and Part IV total rows;
- navigation and course-map paths will be unique and ordered.

These publication assertions should remain red until Task 9.

- [ ] **Step 3: Run the chapter-only content contract**

Run:

```bash
python3.12 -m unittest tests.test_chapter_17.ChapterSeventeenTests.test_units_have_final_metadata_hours_and_anchors -v
python3.12 -m unittest tests.test_chapter_17.ChapterSeventeenTests.test_chapter_guide_lists_units_hours_and_boundaries -v
python3.12 scripts/check_content.py
```

Expected: PASS. The publication method in `tests.test_chapter_17` still FAILS.

- [ ] **Step 4: Commit the chapter guide**

```bash
git add content/chapters/chapter-17/index.md tests/test_chapter_17.py
git commit -m "docs: close chapter 17 teaching arc"
```

## Task 9: Publish Chapter 17 and reconcile controlled totals

**Files:**

- Create: `docs/curriculum/part-04-dependencies.md`
- Modify: `docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md`
- Modify: `docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md`
- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `README.md`
- Modify: `scripts/check_site.py`
- Modify: `tests/test_chapter_15.py`
- Modify: `tests/test_chapter_16.py`
- Modify: `tests/test_zensical_structure.py`
- Modify: `tests/test_chapter_17.py`

- [ ] **Step 1: Extend failing publication tests**

Require:

```python
self.assertIn("| 第 17 章 | 4.5 | 3.5 | 8 |", part_design)
self.assertIn("| **第四部** | **25.5** | **11** | **36.5** |", part_design)
self.assertNotIn("第四部学时 \\(24+10=34\\)", part_design)
self.assertNotIn("理论 24、应用 10", part_design)
self.assertIn("第四部第 17 章，共 72 个学习单元", readme)
```

Add tests for the master design’s reconciled current baseline:

```text
Part IV: 25.5 theory + 11 application = 36.5
Whole book: 291.5 theory + 95 application = 386.5
```

The increase from the prior 384-hour baseline is exactly:

- Chapter 15 expansion: `+1.0 theory`, `+0.5 application`;
- Chapter 17 expansion: `+0.5 theory`, `+0.5 application`.

Run the affected tests and confirm they FAIL on stale publication data.

- [ ] **Step 2: Update the authoritative designs**

In the Part IV design:

- replace Chapter 17’s four hour rows with `1.50/0.50`,
  `1.50/0.50`, `1.25/0.75`, `0.25/1.75`;
- replace its chapter row with `4.5/3.5/8`;
- replace every current Part IV total with `25.5/11/36.5`;
- replace the stale test and completion statements `24+10=34`;
- update algorithm/result/certificate wording to match the approved design.

In the whole-book design, change the Part IV row and current total row to
`25.5/11/36.5` and `291.5/95/386.5`, and explain the 2.5-hour cumulative
increase instead of silently changing the number.

- [ ] **Step 3: Write the dependency and unique-placement document**

`docs/curriculum/part-04-dependencies.md` must contain:

- a table for each Chapter 13–17 unit with incoming theorem dependencies and
  outgoing uses;
- Chapter 12’s unique ownership of IVT and certified bisection;
- Chapter 15.2’s unique ownership of Fermat, derivative-sign monotonicity, and
  Darboux;
- Chapter 16’s unique ownership of finite Taylor remainder theorems and
  numerical differentiation;
- Chapter 17’s unique ownership of convexity, function-shape synthesis,
  Newton convergence order, and safeguarded Newton;
- the Chapter 18 interface limited to antiderivatives and integration methods;
- explicit prohibitions on integral remainder, power series, multivariable
  differentiation, and multivariable Newton.

- [ ] **Step 4: Update navigation, course map, README, and site checks**

Add the guide and four units after Chapter 16 in `mkdocs.yml`.

In `content/course-map.md`:

- add the Chapter 17 heading, 8-hour sentence, and four ordered links;
- replace the “Chapter 17 not published” language;
- change the forward route to begin with Chapter 18.

In `README.md`, set the release boundary to Chapter 17 and count to 72.

In `scripts/check_site.py`, add:

```python
"chapters/chapter-17/u-04-17-04-safeguarded-newton/index.html": [
    "alg-u-04-17-04-safeguarded-newton",
    "thm-u-04-17-04-bracket-contraction",
    "tbl-u-04-17-04-certificate-comparison",
]
```

and require the Part IV/Chapter 17 navigation markers on that page.

- [ ] **Step 5: Update stale earlier-chapter release assertions**

Change only the cumulative release and Part IV-total assertions in
`tests/test_chapter_15.py`, `tests/test_chapter_16.py`, and
`tests/test_zensical_structure.py`. Do not weaken their chapter-specific
mathematical tests.

- [ ] **Step 6: Run publication and strict-build checks**

Run:

```bash
python3.12 -m unittest tests.test_chapter_15 tests.test_chapter_16 tests.test_chapter_17 tests.test_zensical_structure tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: all tests PASS, strict build reports `No issues found`, and site
check exits 0.

- [ ] **Step 7: Commit publication integration**

```bash
git add docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md docs/curriculum/part-04-dependencies.md mkdocs.yml content/course-map.md README.md scripts/check_site.py tests/test_chapter_15.py tests/test_chapter_16.py tests/test_chapter_17.py tests/test_zensical_structure.py
git commit -m "docs: publish chapter 17 and close part 4 totals"
```

## Task 10: Audit all 20 Part IV units and repair findings

**Files:**

- Create: `tests/test_part_04_consistency.py`
- Create: `docs/reviews/2026-07-27-part-04-consistency-review.md`
- Review and modify only after a failing regression proves a defect:
  - `content/chapters/chapter-13/u-04-13-01-average-instantaneous-rate.md`
  - `content/chapters/chapter-13/u-04-13-02-derivative-existence-failure.md`
  - `content/chapters/chapter-13/u-04-13-03-local-linearization.md`
  - `content/chapters/chapter-13/u-04-13-04-sensitivity-linear-model.md`
  - `content/chapters/chapter-14/u-04-14-01-algebraic-derivative-rules.md`
  - `content/chapters/chapter-14/u-04-14-02-chain-rule.md`
  - `content/chapters/chapter-14/u-04-14-03-inverse-elementary-derivatives.md`
  - `content/chapters/chapter-14/u-04-14-04-implicit-higher-derivatives.md`
  - `content/chapters/chapter-15/u-04-15-01-fermat-rolle-lagrange.md`
  - `content/chapters/chapter-15/u-04-15-02-monotonicity-darboux.md`
  - `content/chapters/chapter-15/u-04-15-03-cauchy-mean-value.md`
  - `content/chapters/chapter-15/u-04-15-04-lhopital-rule.md`
  - `content/chapters/chapter-16/u-04-16-01-peano-expansion.md`
  - `content/chapters/chapter-16/u-04-16-02-lagrange-remainder.md`
  - `content/chapters/chapter-16/u-04-16-03-cauchy-remainder.md`
  - `content/chapters/chapter-16/u-04-16-04-trusted-approximation.md`
  - `content/chapters/chapter-17/u-04-17-01-function-shape.md`
  - `content/chapters/chapter-17/u-04-17-02-convexity-optimization.md`
  - `content/chapters/chapter-17/u-04-17-03-newton-convergence-failure.md`
  - `content/chapters/chapter-17/u-04-17-04-safeguarded-newton.md`
  - `src/mathbook_examples/differentiation.py`
  - `src/mathbook_examples/newton.py`
  - `tests/test_chapter_13.py`
  - `tests/test_chapter_14.py`
  - `tests/test_chapter_15.py`
  - `tests/test_chapter_16.py`
  - `tests/test_chapter_17.py`
  - `tests/test_differentiation.py`
  - `tests/test_newton.py`
  - `docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md`
  - `docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md`

- [ ] **Step 1: Write the failing automated consistency gate**

`tests/test_part_04_consistency.py` must:

- discover exactly 20 non-index Markdown units under Chapters 13–17;
- parse every front matter block and assert unique `unit_id`;
- sum hours to theory `25.5` and application `11.0`;
- require `content_standard == 2` for all 20 units;
- require the Part IV and master designs to contain the reconciled totals and no
  stale current completion total;
- require `part-04-dependencies.md` to mention Chapters 12–18 and all Part IV
  unit IDs;
- require `differentiation.py` and `newton.py` to be the sole named source
  modules for their algorithms;
- require the review report path and its five chapter sections;
- require README, course map, navigation, and site checker to agree on Chapter
  17 and 72 published units.

Run:

```bash
python3.12 -m unittest tests.test_part_04_consistency -v
```

Expected: FAIL because the review report has not been created.

- [ ] **Step 2: Create the review report structure**

Write `docs/reviews/2026-07-27-part-04-consistency-review.md` with:

1. scope and method;
2. verified hour/unit totals;
3. Chapter 12 and Chapter 18 interface findings;
4. separate Chapter 13, 14, 15, 16, and 17 review sections;
5. a 20-row unit matrix with columns for prerequisites, definitions/theorems,
   proof assumptions, examples/exercises, algorithms/certificates, and result;
6. a findings table containing severity, exact file/anchor, issue, repair, and
   verification;
7. known limitations;
8. final commands and observed results.

Every result cell in the published report must contain a verified conclusion
or an explicitly described remaining limitation.

- [ ] **Step 3: Perform the dependency-order manual review**

Read the pages in this order:

```text
Chapter 12 certificate comparison
Chapter 13 units 1–4
Chapter 14 units 1–4
Chapter 15 units 1–4
Chapter 16 units 1–4
Chapter 17 units 1–4
Chapter 18 interface in the master curriculum design
```

For every unit, verify and record:

- prerequisites are available at that point;
- theorem hypotheses match the proof;
- local/global and existence/uniqueness claims are separated;
- endpoints, one-sided domains, exceptional points, and non-finite algorithm
  states are handled;
- notation and quantifiers remain consistent;
- examples genuinely instantiate the theorem assumptions;
- exercises and full answers do not assert a stronger conclusion than the
  theory;
- later-part material appears only in the boundary/handoff section.

- [ ] **Step 4: Run targeted textual diagnostics**

Run:

```bash
rg -n "显然|容易看出|不妨|必然|误差不超过|误差证书|停止|收敛|唯一|拐点|严格凸" content/chapters/chapter-{13,14,15,16,17}
rg -n "Riemann 积分|积分型 Taylor 余项|无穷 Taylor 级数|幂级数|Fréchet|多元" content/chapters/chapter-{13,14,15,16,17}
python3.12 scripts/check_content.py
```

Inspect every match in context; these searches identify review sites but do
not themselves prove an error.

- [ ] **Step 5: Repair each confirmed defect with a regression test**

For each confirmed mathematical, dependency, or certificate defect:

1. add the narrowest failing assertion to the owning chapter test or
   `tests/test_part_04_consistency.py`;
2. run that test and observe the intended failure;
3. correct only the affected page/source/design;
4. rerun the narrow test and the owning chapter test;
5. record the exact repair and verification in the findings table.

Known defects that must be represented in the report even though Task 9 fixes
them are:

- stale `24+10=34` statements in the Part IV design;
- missing `part-04-dependencies.md`;
- stale whole-book 384-hour baseline after the Chapter 15 and 17 expansions;
- duplicate-proof risk between Unit 15.2 and Unit 17.1.

- [ ] **Step 6: Run the Part IV review gate**

Run:

```bash
python3.12 -m unittest tests.test_part_04_consistency -v
python3.12 -m unittest tests.test_chapter_13 tests.test_chapter_14 tests.test_chapter_15 tests.test_chapter_16 tests.test_chapter_17 tests.test_newton tests.test_differentiation -v
python3.12 scripts/check_content.py
```

Expected: PASS.

- [ ] **Step 7: Commit the audit and repairs**

Stage only the review report, consistency test, and files actually repaired:

```bash
git add -u content/chapters/chapter-13 content/chapters/chapter-14 content/chapters/chapter-15 content/chapters/chapter-16 content/chapters/chapter-17
git add -u src/mathbook_examples
git add -u docs/superpowers/specs/2026-07-18-mathematical-analysis-textbook-design.md docs/superpowers/specs/2026-07-25-part-04-differentiation-design.md docs/curriculum/part-04-dependencies.md
git add -u tests/test_chapter_13.py tests/test_chapter_14.py tests/test_chapter_15.py tests/test_chapter_16.py tests/test_chapter_17.py tests/test_newton.py tests/test_differentiation.py
git add tests/test_part_04_consistency.py docs/reviews/2026-07-27-part-04-consistency-review.md
git commit -m "docs: audit and reconcile part 4 content"
```

The `git add -u` commands stage only tracked modifications inside the reviewed
Part IV scope; they do not stage unrelated untracked files.

## Task 11: Perform final release verification

**Files:**

- Modify: `docs/reviews/2026-07-27-part-04-consistency-review.md`

- [ ] **Step 1: Run the full acceptance gate from a clean generated-site state**

Run:

```bash
make verify
```

Expected:

- all Python tests PASS;
- `scripts/check_content.py` exits 0;
- both strict-build invocations report `No issues found`;
- `scripts/check_site.py` exits 0.

- [ ] **Step 2: Inspect the generated Chapter 17 pages**

Confirm these files exist and contain their required anchors:

```text
site/chapters/chapter-17/index.html
site/chapters/chapter-17/u-04-17-01-function-shape/index.html
site/chapters/chapter-17/u-04-17-02-convexity-optimization/index.html
site/chapters/chapter-17/u-04-17-03-newton-convergence-failure/index.html
site/chapters/chapter-17/u-04-17-04-safeguarded-newton/index.html
```

Also inspect the rendered navigation on the algorithm page for the Part IV and
Chapter 17 labels.

- [ ] **Step 3: Record observed final evidence**

Replace the report’s command-results section with the actual:

- test count and pass result;
- content-check result;
- strict-build result;
- site-check result;
- Chapter 17 rendered-page count;
- final Part IV hours and published unit count.

Do not claim a result that is not present in the fresh command output.

- [ ] **Step 4: Re-run the report consistency test**

Run:

```bash
python3.12 -m unittest tests.test_part_04_consistency -v
git diff --check
git status --short
```

Expected: test PASS, no whitespace errors, and only the review report is
modified.

- [ ] **Step 5: Commit final verification evidence**

```bash
git add docs/reviews/2026-07-27-part-04-consistency-review.md
git commit -m "docs: record part 4 release verification"
```

- [ ] **Step 6: Verify the committed state**

Run:

```bash
git status --short
git log -1 --oneline
```

Expected: clean status and the final verification-evidence commit at `HEAD`.
