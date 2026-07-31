# Part X Parametric Integrals Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Part X as 20 rigorous self-study units covering normal and improper parameter-dependent Riemann integrals, exchange theorems, Gamma and Beta functions, and one tested certificate-aware numerical module.

**Architecture:** Implement one dependency-closed chapter at a time behind locked curriculum, proof, counterexample, training, scope, and publication contracts. Keep all core arguments in the classical Riemann framework and make every exchange theorem expose its uniform-control hypothesis. Put both Gamma and Beta computations in one `src/mathbook_examples/parametric_integrals.py` source that composes the existing certified Simpson routine.

**Tech Stack:** Python 3.12 standard library, frozen dataclasses, `unittest`, Markdown with Zensical/MkDocs, MathJax, existing `mathbook_examples.quadrature`, `scripts/check_content.py`, `scripts/check_site.py`, and `make verify`.

---

## Locked curriculum registry

```python
PART_10_UNITS = [
    ("u-10-42-01", "含参积分怎样定义函数，参数与积分变量怎样分工？", 1.25, 0.00, "parametric-integral-functions", 8, 10),
    ("u-10-42-02", "被积函数联合连续时，积分为什么连续依赖参数？", 1.25, 0.25, "continuity-under-integral", 9, 11),
    ("u-10-42-03", "一致收敛为什么允许极限进入积分号？", 1.25, 0.25, "uniform-limit-interchange", 9, 11),
    ("u-10-42-04", "哪些逐点收敛反例说明一致控制不可省略？", 1.00, 0.50, "pointwise-failure", 10, 12),
    ("u-10-42-05", "怎样为连续性与极限交换建立条件检查表？", 0.75, 0.50, "exchange-checklist", 10, 12),
    ("u-10-43-01", "什么条件允许对含参积分求导？", 1.25, 0.00, "differentiation-under-integral", 9, 11),
    ("u-10-43-02", "差商与偏导的一致控制怎样完成 Leibniz 公式证明？", 1.50, 0.25, "difference-quotient-control", 10, 12),
    ("u-10-43-03", "积分端点随参数变化时，边界项从哪里产生？", 1.25, 0.50, "variable-endpoints-leibniz", 10, 12),
    ("u-10-43-04", "对参数再积分时，怎样通过经典 Fubini 交换次序？", 1.00, 0.50, "parameter-integration-fubini", 10, 12),
    ("u-10-43-05", "可固定化的移动区域怎样化为固定区域问题？", 1.00, 0.75, "fixed-domain-transform", 11, 13),
    ("u-10-44-01", "含参反常积分的一致收敛应怎样定义？", 1.25, 0.00, "uniform-improper-definition", 9, 11),
    ("u-10-44-02", "一致 Cauchy 判据怎样把尾部转化为可检查条件？", 1.50, 0.25, "uniform-cauchy-criterion", 10, 12),
    ("u-10-44-03", "Weierstrass、Dirichlet 与 Abel 型判据怎样控制参数族？", 1.25, 0.50, "uniform-convergence-tests", 11, 13),
    ("u-10-44-04", "连续性、极限与参数积分何时可同反常积分交换？", 1.00, 0.50, "improper-exchange", 10, 12),
    ("u-10-44-05", "积分号下求导何时成立，反例揭示哪些条件缺口？", 1.00, 0.75, "improper-differentiation", 11, 13),
    ("u-10-45-01", "Gamma 积分在哪些参数上收敛，递推公式怎样得到？", 1.00, 0.25, "gamma-convergence-recurrence", 9, 11),
    ("u-10-45-02", "Beta 积分的端点奇性怎样控制？", 1.00, 0.25, "beta-endpoint-singularities", 9, 11),
    ("u-10-45-03", "Beta–Gamma 关系怎样由重积分与换元推出？", 1.25, 0.25, "beta-gamma-relation", 10, 12),
    ("u-10-45-04", "参数求导怎样产生含对数因子的积分与敏感性公式？", 0.75, 0.75, "logarithmic-parameter-derivatives", 10, 12),
    ("u-10-45-05", "怎样对 Gamma、Beta 积分作带状态的可靠近似？", 0.50, 1.00, "certified-gamma-beta", 12, 16),
]
```

Locked totals: 20 units, 22 theory hours, 8 application hours, and 30 hours. The completed book totals become 209 core units and 367 core hours. No Part XI page or navigation entry is created.

## File map

### Create

- `docs/curriculum/part-10-dependencies.md` — prerequisites, unique outputs, hours, exchange-proof order, scope, and release status.
- `content/chapters/chapter-42/` through `content/chapters/chapter-45/` — four guides and 20 core unit pages.
- `tests/test_chapter_42.py` through `tests/test_chapter_45.py` — metadata, proof, counterexample, exercise, answer, and scope contracts.
- `src/mathbook_examples/parametric_integrals.py` — the sole Gamma/Beta numerical implementation.
- `tests/test_parametric_integrals.py` — values, bounds, status semantics, immutability, and invalid-input tests.
- `tests/test_part_10_consistency.py` — totals, dependency, publication, scope, and unique-source contracts.
- `docs/reviews/2026-08-01-chapter-42-consistency-review.md` through `docs/reviews/2026-08-01-chapter-45-consistency-review.md`.
- `docs/reviews/2026-08-01-part-10-consistency-review.md`.

### Modify

- `mkdocs.yml` — publish only the chapter reached at the current checkpoint.
- `content/course-map.md` — add the blueprint, then advance status chapter by chapter.
- `README.md` — advance publication boundary and totals only after a chapter gate passes.
- `tests/test_mkdocs_site.py` and `tests/test_zensical_structure.py` — register representative Part X publication surfaces.
- `scripts/check_site.py` — require representative rendered anchors and final navigation.
- `docs/curriculum/part-06-dependencies.md`, `part-08-dependencies.md`, and `part-09-dependencies.md` — replace future-tense Part X handoffs with precise published interfaces only at final closure.
- `src/mathbook_examples/__init__.py` — remain a package marker; do not re-export the module.

## Shared content contract

Every unit uses `content_standard: 2`, declares exact direct prerequisites, contains its stable unit anchor, at least two anchored examples, at least two immediate checks, and the exact exercise/answer counts in the registry. Use these headings in order:

```markdown
## 先备知识
## 学习目标
## 牵引问题
## 探索与猜想
## 概念与理论
## 例题与迁移
## 即时检验与回望
## 常见误区与后续
## 习题与答案
```

Every exchange theorem must include `### 交换对象`, `### 定理条件`, `### 证明路线`, `### 条件用在何处`, and `### 失败边界`. Computational material additionally uses:

```markdown
### 问题来源
### 数学转化
### 算法思想
### 误差与适用条件
### 伪代码
### Python
### 结果解释
```

No core page may use Lebesgue measure, almost-everywhere language, dominated convergence, general moving-domain transport, complex Gamma theory, or numerical agreement as proof.

## Task 1: Lock the Part X blueprint

**Files:**
- Create: `docs/curriculum/part-10-dependencies.md`
- Create: `tests/test_part_10_consistency.py`
- Modify: `content/course-map.md`

- [ ] **Step 1: Write the failing blueprint test**

Create `tests/test_part_10_consistency.py` with the registry above and these initial assertions:

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs/curriculum/part-10-dependencies.md"
COURSE_MAP = ROOT / "content/course-map.md"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

class Part10ConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.exists(), f"missing {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8")

    def test_locked_part_totals(self):
        theory = sum(row[2] for row in PART_10_UNITS)
        applied = sum(row[3] for row in PART_10_UNITS)
        self.assertEqual((20, 22.0, 8.0, 30.0), (len(PART_10_UNITS), theory, applied, theory + applied))

    def test_blueprint_starts_after_part_nine(self):
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 41 章", text)
        self.assertIn("20 个核心单元、30 学时", text)
        self.assertNotIn("chapters/chapter-42/", NAVIGATION)

    def test_part_eleven_is_not_created(self):
        self.assertFalse((ROOT / "content/chapters/chapter-46").exists())
        self.assertNotIn("chapters/chapter-46/", NAVIGATION)
```

- [ ] **Step 2: Run the test and verify the dependency map is missing**

Run: `python3.12 -m unittest tests.test_part_10_consistency -v`

Expected: FAIL because `docs/curriculum/part-10-dependencies.md` is absent.

- [ ] **Step 3: Write the dependency map and planned course map**

Create all 20 dependency rows with direct prerequisites and unique outputs. Record the proof chain, the 30-hour cap, the fixed-domain boundary, the three numerical statuses, and the Part XI exclusion. Add Chapters 42–45 to `content/course-map.md` as “规划中”; do not add navigation or content pages.

- [ ] **Step 4: Run the focused and baseline gates**

```bash
python3.12 -m unittest tests.test_part_10_consistency -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: all commands exit 0 and the published site still stops at Chapter 41.

- [ ] **Step 5: Commit the blueprint**

```bash
git add docs/curriculum/part-10-dependencies.md content/course-map.md tests/test_part_10_consistency.py
git commit -m "docs: lock part 10 curriculum blueprint"
```

## Task 2: Publish Chapter 42

**Files:**
- Create: `content/chapters/chapter-42/index.md`
- Create: `content/chapters/chapter-42/u-10-42-01-parametric-integral-functions.md`
- Create: `content/chapters/chapter-42/u-10-42-02-continuity-under-integral.md`
- Create: `content/chapters/chapter-42/u-10-42-03-uniform-limit-interchange.md`
- Create: `content/chapters/chapter-42/u-10-42-04-pointwise-failure.md`
- Create: `content/chapters/chapter-42/u-10-42-05-exchange-checklist.md`
- Create: `tests/test_chapter_42.py`
- Create: `docs/reviews/2026-08-01-chapter-42-consistency-review.md`
- Modify: `docs/curriculum/part-10-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`
- Modify: `tests/test_zensical_structure.py`

- [ ] **Step 1: Write the failing Chapter 42 contract**

Reuse the metadata, guide-link, exercise, answer, and `content_standard` helpers from `tests/test_chapter_41.py`. Lock these markers:

```python
REQUIRED_MARKERS = {
    "u-10-42-01": ("积分变量", "参数变量", "固定紧区间", "Riemann"),
    "u-10-42-02": ("联合连续", "一致连续", "上确界估计", "连续依赖"),
    "u-10-42-03": ("一致收敛", "极限进入积分号", "积分区间长度", "误差界"),
    "u-10-42-04": ("逐点收敛", "移动尖峰", "不能交换", "失败边界"),
    "u-10-42-05": ("交换对象", "定理条件", "条件用在何处", "条件检查表"),
}
FORBIDDEN_CORE_TERMS = ("控制收敛定理", "几乎处处", "Reynolds 输运", "形状导数")
```

Also assert 46 anchored exercises, 56 collapsed answers, five guide links, exact hours, and absence of Chapter 43 navigation.

- [ ] **Step 2: Run the contract and verify red**

Run: `python3.12 -m unittest tests.test_chapter_42 -v`

Expected: FAIL because Chapter 42 files do not exist.

- [ ] **Step 3: Write the guide and five units**

Prove continuity from compact-uniform continuity, prove uniform-limit interchange by
`|∫(f_n-f)| ≤ (b-a)||f_n-f||∞`, and use a continuous moving-spike sequence with pointwise limit zero but non-vanishing integrals as the stable failure example. Finish with a decision table that distinguishes continuity in a parameter, sequence limits, and unsupported pointwise claims.

- [ ] **Step 4: Publish and verify Chapter 42**

Add only Chapter 42 navigation. Update the dependency map to “当前发布边界：第 42 章”, README totals to 194 units and 344 hours, and course-map status to “已发布”. Run:

```bash
python3.12 -m unittest tests.test_chapter_42 tests.test_part_10_consistency -v
make verify
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: all commands exit 0; no Chapter 43 page is published.

- [ ] **Step 5: Record review and commit**

Write the review with proof checks, counterexample calculations, scope scan, exercise/answer counts, and gate results.

```bash
git add content/chapters/chapter-42 docs/curriculum/part-10-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_42.py tests/test_part_10_consistency.py tests/test_zensical_structure.py docs/reviews/2026-08-01-chapter-42-consistency-review.md
git commit -m "docs: publish chapter 42 parametric integrals"
```

## Task 3: Publish Chapter 43

**Files:**
- Create: `content/chapters/chapter-43/index.md`
- Create: `content/chapters/chapter-43/u-10-43-01-differentiation-under-integral.md`
- Create: `content/chapters/chapter-43/u-10-43-02-difference-quotient-control.md`
- Create: `content/chapters/chapter-43/u-10-43-03-variable-endpoints-leibniz.md`
- Create: `content/chapters/chapter-43/u-10-43-04-parameter-integration-fubini.md`
- Create: `content/chapters/chapter-43/u-10-43-05-fixed-domain-transform.md`
- Create: `tests/test_chapter_43.py`
- Create: `docs/reviews/2026-08-01-chapter-43-consistency-review.md`
- Modify: `docs/curriculum/part-10-dependencies.md`, `content/course-map.md`, `mkdocs.yml`, `README.md`

- [ ] **Step 1: Write and run the failing Chapter 43 contract**

```python
REQUIRED_MARKERS = {
    "u-10-43-01": ("偏导数", "连续", "积分号下求导", "充分条件"),
    "u-10-43-02": ("差商", "中值定理", "一致控制", "极限交换"),
    "u-10-43-03": ("上端点", "下端点", "边界项", "链式法则"),
    "u-10-43-04": ("参数再积分", "经典 Fubini", "固定区域", "交换次序"),
    "u-10-43-05": ("固定参考域", "Jacobian", "换元", "后续去向"),
}
```

Assert 50 exercises, 60 answers, exact hours, explicit plus/minus endpoint terms, a chapter-end Reynolds/shape-derivative pointer, and no definition or exercise for those later topics.

Run: `python3.12 -m unittest tests.test_chapter_43 -v`

Expected: FAIL because Chapter 43 files do not exist.

- [ ] **Step 2: Write the five units with complete proofs**

Derive the fixed-endpoint rule from uniformly controlled difference quotients. Derive
`F'(t)=f(b(t),t)b'(t)-f(a(t),t)a'(t)+∫[a(t),b(t)] ∂_t f(x,t)dx`
by separating endpoint and integrand changes. Restrict parameter integration to classical Fubini hypotheses, and moving regions to explicit diffeomorphic fixed-domain changes already justified by Chapter 35.

- [ ] **Step 3: Publish, verify, review, and commit**

Advance totals to 199 units and 352 hours and the boundary to Chapter 43. Run the focused tests and all five gates from Task 2. Confirm Chapter 44 remains absent. Then:

```bash
git add content/chapters/chapter-43 docs/curriculum/part-10-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_43.py tests/test_part_10_consistency.py docs/reviews/2026-08-01-chapter-43-consistency-review.md
git commit -m "docs: publish chapter 43 Leibniz rules"
```

## Task 4: Publish Chapter 44

**Files:**
- Create: `content/chapters/chapter-44/index.md`
- Create: `content/chapters/chapter-44/u-10-44-01-uniform-improper-definition.md`
- Create: `content/chapters/chapter-44/u-10-44-02-uniform-cauchy-criterion.md`
- Create: `content/chapters/chapter-44/u-10-44-03-uniform-convergence-tests.md`
- Create: `content/chapters/chapter-44/u-10-44-04-improper-exchange.md`
- Create: `content/chapters/chapter-44/u-10-44-05-improper-differentiation.md`
- Create: `tests/test_chapter_44.py`
- Create: `docs/reviews/2026-08-01-chapter-44-consistency-review.md`
- Modify: `docs/curriculum/part-10-dependencies.md`, `content/course-map.md`, `mkdocs.yml`, `README.md`

- [ ] **Step 1: Write and run the failing Chapter 44 contract**

```python
REQUIRED_MARKERS = {
    "u-10-44-01": ("一致收敛", "无穷区间", "有限端点奇性", "统一截断"),
    "u-10-44-02": ("一致 Cauchy", "对所有参数", "统一尾项", "充要性"),
    "u-10-44-03": ("Weierstrass", "Dirichlet", "Abel", "单调"),
    "u-10-44-04": ("连续性", "极限", "参数积分", "统一尾项"),
    "u-10-44-05": ("积分号下求导", "导数积分一致收敛", "基点收敛", "反例"),
}
```

Assert 51 exercises, 61 answers, exact quantifier strings, both improper-endpoint types, and explicit rejection of finite-cutoff numerical stability as proof.

Run: `python3.12 -m unittest tests.test_chapter_44 -v`

Expected: FAIL because Chapter 44 files do not exist.

- [ ] **Step 2: Write the five units and inspect every quantifier**

Prove the uniform Cauchy criterion in both directions; state Weierstrass, Dirichlet, and Abel hypotheses separately; prove exchange results by uniform truncation followed by a uniform tail estimate. For differentiation, require convergence at one parameter value plus uniform convergence of the derivative integral on each compact parameter interval. Include a stable example where every parameter integral exists but uniformity fails near a boundary parameter.

- [ ] **Step 3: Publish, verify, review, and commit**

Advance totals to 204 units and 360 hours and the boundary to Chapter 44. Run focused tests, all five gates, and a manual formula/quantifier review. Then:

```bash
git add content/chapters/chapter-44 docs/curriculum/part-10-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_44.py tests/test_part_10_consistency.py docs/reviews/2026-08-01-chapter-44-consistency-review.md
git commit -m "docs: publish chapter 44 uniform improper integrals"
```

## Task 5: Implement certificate-aware Gamma and Beta quadrature

**Files:**
- Create: `src/mathbook_examples/parametric_integrals.py`
- Create: `tests/test_parametric_integrals.py`

- [ ] **Step 1: Write failing public-contract tests**

```python
from dataclasses import FrozenInstanceError
from math import gamma, isfinite
import unittest

from mathbook_examples.parametric_integrals import beta_integral, gamma_integral

class ParametricIntegralTests(unittest.TestCase):
    def test_gamma_two_is_certified_with_supplied_bound(self):
        result = gamma_integral(2.0, 1e-5, 4096, fourth_derivative_bound=10.0)
        self.assertEqual("target_met", result.status)
        self.assertTrue(result.target_met)
        self.assertLessEqual(abs(result.value - gamma(2.0)), result.total_error_bound)

    def test_missing_regular_bound_is_uncertified(self):
        result = beta_integral(2.0, 3.0, 1e-5, 512)
        self.assertEqual("uncertified", result.status)
        self.assertIsNone(result.quadrature_error_bound)
        self.assertIsNone(result.total_error_bound)

    def test_result_is_frozen(self):
        result = gamma_integral(1.0, 1e-3, 64)
        with self.assertRaises(FrozenInstanceError):
            result.status = "changed"
```

Add subtests rejecting `nan`, infinities, nonpositive function parameters, nonpositive/nonfinite tolerances, Boolean or nonpositive panel budgets, and negative/nonfinite derivative bounds. Add a low-budget case that returns `budget_exhausted` with a finite valid bound.

- [ ] **Step 2: Run tests and verify import failure**

Run: `python3.12 -m unittest tests.test_parametric_integrals -v`

Expected: ERROR with `ModuleNotFoundError: mathbook_examples.parametric_integrals`.

- [ ] **Step 3: Implement the frozen result and validation**

```python
@dataclass(frozen=True)
class ParametricIntegralResult:
    value: float
    truncation: tuple[float, float]
    endpoint_error_bound: float
    quadrature_error_bound: float | None
    total_error_bound: float | None
    evaluations: int
    status: str
    target_met: bool
```

Validate inputs before evaluating integrands. Choose positive finite truncations from the requested tolerance. For Gamma, bound the origin by `epsilon**parameter / parameter` and choose a right cutoff beyond `max(parameter - 1, 0)` so the logarithmic derivative supplies an exponential tail bound. For Beta, cut both endpoints and bound each omitted interval by the appropriate endpoint power times the maximum of the nonsingular factor on that interval.

- [ ] **Step 4: Compose `certified_simpson` without duplicating it**

When the derivative bound is absent, call the fixed-grid midpoint routine for a diagnostic value and return `uncertified`. When present, allocate the remaining tolerance to `certified_simpson`, sum its strict bound with the analytic endpoint bound, propagate `target_met` or `budget_exhausted`, and count all evaluations. Do not estimate a derivative bound from sampled values.

- [ ] **Step 5: Run focused and regression tests**

```bash
python3.12 -m unittest tests.test_parametric_integrals tests.test_quadrature -v
python3.12 -m unittest discover -s tests -v
git diff --check
```

Expected: all tests pass; the existing quadrature API is unchanged.

- [ ] **Step 6: Commit the numerical source**

```bash
git add src/mathbook_examples/parametric_integrals.py tests/test_parametric_integrals.py
git commit -m "feat: add certified parametric integral checks"
```

## Task 6: Publish Chapter 45 and connect the numerical source

**Files:**
- Create: `content/chapters/chapter-45/index.md`
- Create: `content/chapters/chapter-45/u-10-45-01-gamma-convergence-recurrence.md`
- Create: `content/chapters/chapter-45/u-10-45-02-beta-endpoint-singularities.md`
- Create: `content/chapters/chapter-45/u-10-45-03-beta-gamma-relation.md`
- Create: `content/chapters/chapter-45/u-10-45-04-logarithmic-parameter-derivatives.md`
- Create: `content/chapters/chapter-45/u-10-45-05-certified-gamma-beta.md`
- Create: `tests/test_chapter_45.py`
- Create: `docs/reviews/2026-08-01-chapter-45-consistency-review.md`
- Modify: `docs/curriculum/part-10-dependencies.md`, `content/course-map.md`, `mkdocs.yml`, `README.md`, `scripts/check_site.py`, `tests/test_mkdocs_site.py`

- [ ] **Step 1: Write and run the failing Chapter 45 contract**

```python
REQUIRED_MARKERS = {
    "u-10-45-01": ("Gamma", "参数大于 0", "分部积分", "递推公式"),
    "u-10-45-02": ("Beta", "两个参数大于 0", "端点奇性", "收敛"),
    "u-10-45-03": ("Beta–Gamma", "第一象限", "极坐标", "Jacobian"),
    "u-10-45-04": ("对数因子", "参数求导", "一致收敛", "敏感性"),
    "u-10-45-05": ("endpoint_error_bound", "total_error_bound", "budget_exhausted", "uncertified"),
}
```

Assert 50 exercises, 62 answers, direct import from `mathbook_examples.parametric_integrals`, no duplicated function definition, and no core claims about analytic continuation or complex parameters.

Run: `python3.12 -m unittest tests.test_chapter_45 -v`

Expected: FAIL because Chapter 45 pages do not exist.

- [ ] **Step 2: Write the five units with complete endpoint proofs**

Split Gamma at 1, prove near-zero and exponential-tail convergence, and justify the vanishing boundary term before integration by parts. For Beta, compare both endpoints separately. Derive Beta–Gamma by a first-quadrant double integral and polar substitution with all nonnegative truncation steps stated in the classical framework. Derive logarithmic parameter integrals only after Chapter 44 hypotheses are checked.

- [ ] **Step 3: Connect and explain the numerical module**

Use imports, not copied code:

```python
from mathbook_examples.parametric_integrals import beta_integral, gamma_integral
```

Show one `target_met`, one `budget_exhausted`, and one `uncertified` result. Explain that a supplied fourth-derivative bound is a mathematical input, not something certified by the function.

- [ ] **Step 4: Publish, verify, review, and commit**

Advance totals to 209 units and 367 hours and the boundary to Chapter 45. Add representative rendered anchors for the Beta–Gamma proof and the three result states. Run focused tests and all five gates. Then:

```bash
git add content/chapters/chapter-45 docs/curriculum/part-10-dependencies.md content/course-map.md mkdocs.yml README.md scripts/check_site.py tests/test_mkdocs_site.py tests/test_chapter_45.py tests/test_part_10_consistency.py docs/reviews/2026-08-01-chapter-45-consistency-review.md
git commit -m "docs: publish chapter 45 gamma beta functions"
```

## Task 7: Close the Part X consistency audit

**Files:**
- Create: `docs/reviews/2026-08-01-part-10-consistency-review.md`
- Modify: `docs/curriculum/part-06-dependencies.md`
- Modify: `docs/curriculum/part-08-dependencies.md`
- Modify: `docs/curriculum/part-09-dependencies.md`
- Modify: `docs/curriculum/part-10-dependencies.md`
- Modify: `tests/test_part_10_consistency.py`
- Modify: `scripts/check_site.py`

- [ ] **Step 1: Expand the failing final consistency contract**

Require every publication surface to contain “209 个学习单元”, “367 学时”, and “当前发布边界：第 45 章”. Assert 20 unique Part X pages, exact chapter totals, no Chapter 46, unique ownership of both public numerical functions, no forbidden core vocabulary, and precise Part VI/VIII/IX handoffs into the now-published Part X.

- [ ] **Step 2: Run the contract and verify stale handoffs fail**

Run: `python3.12 -m unittest tests.test_part_10_consistency -v`

Expected: FAIL on future-tense or stale Part X interface text in earlier dependency maps.

- [ ] **Step 3: Update cross-part interfaces and write the audit**

Record direct dependencies and non-dependencies across Parts VI, VIII, IX, X, and XI. Recount exercises and collapsed answers from source rather than copying planned minima. Review every exchange theorem for quantified uniformity, every improper proof for endpoint/tail separation, and every numerical claim for status accuracy. Record findings as Blocking, Important, Minor, or closed.

- [ ] **Step 4: Run the complete release gate**

```bash
python3.12 -m unittest discover -s tests -v
make verify
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
git status --short
```

Expected: every command exits 0; only known pre-existing untracked paths may remain; no Part XI content exists.

- [ ] **Step 5: Commit the closure**

```bash
git add docs/curriculum/part-06-dependencies.md docs/curriculum/part-08-dependencies.md docs/curriculum/part-09-dependencies.md docs/curriculum/part-10-dependencies.md docs/reviews/2026-08-01-part-10-consistency-review.md tests/test_part_10_consistency.py scripts/check_site.py
git commit -m "docs: close part 10 consistency audit"
```

- [ ] **Step 6: Re-run the complete gate on the committed tree**

Repeat Step 4 after the commit. Record the commit hash, exact test count, and all five gate results in the audit only if the recorded facts match the committed tree.
