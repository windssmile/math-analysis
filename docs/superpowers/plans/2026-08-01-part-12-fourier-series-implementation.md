# Part XII Fourier Series Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Part XII as 21 rigorous self-study units that derive Fourier series from finite-dimensional orthogonal projection, teach analytic coefficient computation, prove the selected pointwise and mean-square convergence results, and close the textbook with periodic modeling, Fejér means, and Gibbs phenomena.

**Architecture:** Implement one dependency-closed chapter at a time after locking a registry and a finite-only computation contract. Keep the proof chain one-way: finite trigonometric projection → coefficient calculation → Dirichlet convergence → Bessel and Parseval → Fejér means and modeling. Put all numerical verification in one `src/mathbook_examples/fourier_series.py` source whose result statuses explicitly deny infinite-series certification.

**Tech Stack:** Python 3.12 standard library, frozen dataclasses, `unittest`, Markdown with Zensical/MkDocs, MathJax, PyYAML-backed metadata tests, `scripts/check_content.py`, `scripts/check_site.py`, and `make verify`.

---

## Locked curriculum registry

```python
PART_12_UNITS = [
    ("u-12-51-01", "周期函数与三角函数系怎样构成正交族？", 1.25, 0.25, "trig-orthogonality"),
    ("u-12-51-02", "Fourier 系数为什么来自正交投影？", 1.25, 0.25, "fourier-projection"),
    ("u-12-51-03", "三角多项式怎样给出最佳平方逼近？", 1.50, 0.25, "best-square-approximation"),
    ("u-12-51-04", "复指数形式怎样统一正弦与余弦形式？", 1.00, 0.25, "complex-form"),
    ("u-12-51-05", "有限维投影计算怎样验证最佳逼近？", 1.00, 0.50, "finite-projection-check"),
    ("u-12-52-01", "Fourier 系数有哪些平移、伸缩与对称性质？", 1.00, 0.50, "symmetry-transformations"),
    ("u-12-52-02", "奇偶性和分段积分怎样简化系数计算？", 1.00, 0.75, "coefficient-calculation"),
    ("u-12-52-03", "半区间正弦展开与余弦展开怎样选择？", 1.00, 0.75, "half-range-expansions"),
    ("u-12-52-04", "Fourier 部分和怎样写成 Dirichlet 核卷积？", 1.25, 0.25, "dirichlet-kernel"),
    ("u-12-52-05", "Dirichlet 判别条件怎样保证逐点收敛？", 1.50, 0.25, "dirichlet-convergence"),
    ("u-12-52-06", "连续点与跳跃点的展开值应怎样判断？", 0.75, 0.50, "pointwise-values"),
    ("u-12-53-01", "Bessel 不等式怎样限制 Fourier 系数的能量？", 1.25, 0.25, "bessel-inequality"),
    ("u-12-53-02", "均方误差为何等于总能量减去投影能量？", 1.25, 0.25, "mean-square-error"),
    ("u-12-53-03", "Parseval 等式在什么条件下成立？", 1.50, 0.25, "parseval-identity"),
    ("u-12-53-04", "Parseval 等式怎样用于经典数项级数求和？", 1.00, 0.75, "parseval-series-sums"),
    ("u-12-53-05", "均方收敛与逐点、一致收敛有什么区别？", 1.00, 0.50, "convergence-comparison"),
    ("u-12-54-01", "有限 Fourier 部分和怎样重建周期信号？", 1.00, 0.50, "periodic-reconstruction"),
    ("u-12-54-02", "Gibbs 现象为何不会因增加项数而消失？", 1.25, 0.50, "gibbs-phenomenon"),
    ("u-12-54-03", "Fejér 平均为何比普通部分和更稳定？", 1.50, 0.25, "fejer-means"),
    ("u-12-54-04", "截断阶数、误差指标与采样分辨率怎样选择？", 0.75, 0.75, "truncation-error"),
    ("u-12-54-05", "一个周期模型怎样完成“建模—展开—误差—解释”闭环？", 1.00, 0.50, "periodic-model-closure"),
]
```

Locked totals: 21 units, 24 theory hours, 9 application hours, and 33 hours, below the 34-hour hard cap. The completed book totals become 255 core units and 438 hours. Every unit contains exactly 10 anchored formal exercises and at least 12 collapsed answers, including immediate checks. No Chapter 55 or Part XIII publication surface is created.

## File map

### Create

- `docs/curriculum/part-12-dependencies.md` — all unit prerequisites, unique outputs, proof order, hours, scope, and release state.
- `src/mathbook_examples/fourier_series.py` — the sole finite quadrature, partial-sum, and Fejér-mean source.
- `tests/test_fourier_series.py` — exact coefficients, truncations, statuses, frozen results, overflow, and invalid-input tests.
- `content/chapters/chapter-51/` through `content/chapters/chapter-54/` — four guides and 21 unit pages.
- `tests/test_chapter_51.py` through `tests/test_chapter_54.py` — metadata, proof, computation, exercise, answer, and scope contracts.
- `tests/test_part_12_consistency.py` — totals, dependencies, motivation recovery, publication, scope, and unique-source contracts.
- `docs/reviews/2026-08-01-chapter-51-consistency-review.md` through `docs/reviews/2026-08-01-chapter-54-consistency-review.md`.
- `docs/reviews/2026-08-01-part-12-consistency-review.md`.

### Modify

- `content/course-map.md` — record the locked blueprint, then advance chapter status after each gate.
- `mkdocs.yml` — publish only the chapter reached at the current checkpoint.
- `README.md` — advance the release boundary and totals only after a chapter gate passes.
- `tests/test_mkdocs_site.py`, `tests/test_zensical_structure.py`, and `scripts/check_site.py` — add representative Part XII rendered anchors and final navigation.
- `docs/curriculum/part-05-dependencies.md`, `part-06-dependencies.md`, `part-10-dependencies.md`, `part-11-dependencies.md` — replace future Fourier handoffs with precise published interfaces at final closure.
- `tests/test_part_11_consistency.py` — replace only the historical “Part XII absent” assertion with a Part XI snapshot assertion that permits its new published neighbor.

## Shared content contract

Every unit uses `content_standard: 2`, exact direct prerequisites, three learning goals, three capability IDs, a stable H1 unit anchor, at least two anchored examples, at least two immediate checks, 10 anchored formal exercises, and at least 12 collapsed answers. Use these headings in order:

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

Every core proof uses `### 障碍`, `### 证明路线`, `### 逐步证明`, `### 假设用在何处`, and `### 失败边界`. Computational material additionally uses the existing seven algorithm headings. Program output must say `finite_quadrature_only` or `finite_truncation_only`; no sampled or truncated result is an infinite-series certificate.

## Task 1: Lock the Part XII blueprint

**Files:**
- Create: `tests/test_part_12_consistency.py`
- Create: `docs/curriculum/part-12-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `tests/test_part_11_consistency.py`

- [ ] **Step 1: Write the failing Part XII registry test**

Create `tests/test_part_12_consistency.py` with `PART_12_UNITS` above and this structural core:

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs/curriculum/part-12-dependencies.md"
COURSE_MAP = ROOT / "content/course-map.md"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

class PartTwelveConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_locked_part_totals(self):
        theory = sum(row[2] for row in PART_12_UNITS)
        applied = sum(row[3] for row in PART_12_UNITS)
        self.assertEqual((21, 24.0, 9.0, 33.0),
                         (len(PART_12_UNITS), theory, applied, theory + applied))
        self.assertLessEqual(theory + applied, 34.0)

    def test_blueprint_starts_after_part_eleven(self):
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 50 章", text)
        self.assertIn("21 个核心单元、33 学时", text)
        self.assertNotIn("chapters/chapter-51/", NAVIGATION)

    def test_no_unplanned_neighbor(self):
        self.assertFalse((ROOT / "content/chapters/chapter-55").exists())
        self.assertNotIn("chapters/chapter-55/", NAVIGATION)
```

- [ ] **Step 2: Run red**

Run: `python3.12 -m unittest tests.test_part_12_consistency -v`

Expected: FAIL because `docs/curriculum/part-12-dependencies.md` is absent.

- [ ] **Step 3: Add the dependency registry and planned map**

Create all 21 rows with exact direct prerequisites and unique outputs. Record the方波 motivation, projection-to-Fejér proof chain, 34-hour hard cap, analytic-calculation assessment, the three finite-computation contracts, and all scope exclusions. Add Chapters 51–54 to `content/course-map.md` as planned; do not create pages or navigation.

- [ ] **Step 4: Remove only the stale neighbor lock from Part XI**

Replace `test_part_twelve_is_not_created` in `tests/test_part_11_consistency.py` with assertions that Chapters 46–50 still contain exactly 25 Part XI pages and precede any Part XII navigation. Do not change Part XI historical totals.

- [ ] **Step 5: Run green and commit**

```bash
python3.12 -m unittest tests.test_part_11_consistency tests.test_part_12_consistency -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
git add tests/test_part_11_consistency.py tests/test_part_12_consistency.py docs/curriculum/part-12-dependencies.md content/course-map.md
git commit -m "docs: lock part 12 curriculum blueprint"
```

Expected: all checks pass; the published site still stops at Chapter 50.

## Task 2: Implement the finite Fourier computation source

**Files:**
- Create: `tests/test_fourier_series.py`
- Create: `src/mathbook_examples/fourier_series.py`

- [ ] **Step 1: Write failing public-contract tests**

Use `math.isclose` with explicit tolerances and cover these exact cases:

```python
coeffs = sampled_fourier_coefficients(lambda x: 3.0, 2 * math.pi, 2, 200)
self.assertAlmostEqual(6.0, coeffs.a0, places=12)
self.assertTrue(all(abs(v) < 1e-12 for v in coeffs.cosine_coefficients))
self.assertTrue(all(abs(v) < 1e-12 for v in coeffs.sine_coefficients))
self.assertEqual("finite_quadrature_only", coeffs.status)

partial = fourier_partial_sum(math.pi / 2, 0.0, (), (1.0,), 2 * math.pi)
self.assertAlmostEqual(1.0, partial.value)
self.assertEqual((1, "finite_truncation_only"), (partial.order, partial.status))

fejer = fejer_mean(0.0, 0.0, (2.0, 4.0), (0.0, 0.0), 2 * math.pi)
self.assertAlmostEqual(8.0 / 3.0, fejer.value)
```

Reject booleans, strings, zero or negative periods, negative or non-integral harmonics, invalid panel counts, unequal coefficient lengths, nonfinite inputs, nonfinite callable results, nonfinite products, and overflowing sums. Assert all result dataclasses are frozen.

- [ ] **Step 2: Run red**

Run: `python3.12 -m unittest tests.test_fourier_series -v`

Expected: ERROR because `mathbook_examples.fourier_series` does not exist.

- [ ] **Step 3: Implement the exact result types and validation boundary**

Create these frozen public result types and keep `_finite_real` and `_coefficient_tuple` private:

```python
@dataclass(frozen=True)
class FourierCoefficients:
    a0: float
    cosine_coefficients: tuple[float, ...]
    sine_coefficients: tuple[float, ...]
    period: float
    harmonics: int
    panels: int
    method: str = "composite_midpoint"
    status: str = "finite_quadrature_only"

@dataclass(frozen=True)
class FourierValue:
    value: float
    order: int
    period: float
    method: str
    status: str = "finite_truncation_only"
```

Use the normalization

```python
a0 = (2.0 / period) * integral(f)
a_n = (2.0 / period) * integral(f(x) * cos(2*pi*n*x/period))
b_n = (2.0 / period) * integral(f(x) * sin(2*pi*n*x/period))
```

on the centered interval `[-period/2, period/2]`. Use the composite midpoint rule with exactly `panels` equal subintervals and `math.fsum`; evaluate the callable once per midpoint and reuse its value for all harmonics. The real partial sum is `a0/2 + Σ(a_n cos(nωx) + b_n sin(nωx))`. For `N` supplied harmonics, the Fejér weights are `1 - n/(N+1)` for `n=1,...,N`, with `method="fejer_mean"`.

- [ ] **Step 4: Run green and commit**

```bash
python3.12 -m unittest tests.test_fourier_series -v
make verify
git diff --check
git add tests/test_fourier_series.py src/mathbook_examples/fourier_series.py
git commit -m "feat: add finite fourier computations"
```

Expected: all computation tests pass and every returned status remains explicitly finite-only.

## Task 3: Publish Chapter 51

**Files:**
- Create: `tests/test_chapter_51.py`
- Create: `content/chapters/chapter-51/index.md`
- Create: five Chapter 51 unit files named from the registry slugs
- Create: `docs/reviews/2026-08-01-chapter-51-consistency-review.md`
- Modify: `docs/curriculum/part-12-dependencies.md`, `content/course-map.md`, `mkdocs.yml`, `README.md`, `tests/test_zensical_structure.py`

- [ ] **Step 1: Write the failing Chapter 51 content contract**

Lock exact metadata from the registry, the nine shared headings, 50 exercises, at least 60 answers, and these markers:

```python
MARKERS = {
    "u-12-51-01": ("正交", "周期", r"\int"),
    "u-12-51-02": ("正交投影", "Fourier 系数", "归一化"),
    "u-12-51-03": ("最佳平方逼近", "Pythagoras", "有限维"),
    "u-12-51-04": ("复指数", "共轭对称", "双向换算"),
    "u-12-51-05": ("finite_quadrature_only", "有限截断", "误差"),
}
```

Require the Part XII introduction to contain `方波`, `连续点`, `跳跃点`, `Gibbs`, and the four motivating questions, while forbidding Parseval or Fejér as already-proved results.

- [ ] **Step 2: Run red**

Run: `python3.12 -m unittest tests.test_chapter_51 -v`

Expected: FAIL because Chapter 51 is absent.

- [ ] **Step 3: Write and publish the five units**

Derive the trigonometric orthogonality integrals on a general period before specializing examples. Derive the real Fourier coefficients from minimizing the finite quadratic error. Prove best square approximation by an explicit orthogonal decomposition, not an abstract Hilbert projection theorem. Give both directions of the real/complex coefficient conversion. Import the finite computation source exactly once in Unit 51-05 and label quadrature and truncation outputs as non-certifying.

Advance totals to 239 units and 412.5 hours. Publish only Chapter 51.

- [ ] **Step 4: Verify, review, and commit**

```bash
python3.12 -m unittest tests.test_fourier_series tests.test_chapter_51 tests.test_part_12_consistency -v
make verify
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
git add content/chapters/chapter-51 tests/test_chapter_51.py docs/reviews/2026-08-01-chapter-51-consistency-review.md docs/curriculum/part-12-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_zensical_structure.py
git commit -m "docs: publish chapter 51 orthogonal projection"
```

## Task 4: Publish Chapter 52

**Files:** Create the Chapter 52 guide, six units, `tests/test_chapter_52.py`, and its review; modify the shared publication surfaces.

- [ ] **Step 1: Write the failing Chapter 52 contract**

Lock 60 exercises, at least 72 answers, exact metadata, and markers for coefficient transformations, parity, piecewise integration, odd/even half-range extension, Dirichlet-kernel convolution, the selected Dirichlet convergence hypotheses, and the half-sum rule. Require complete analytic expansions for square, sawtooth, triangle, and absolute-value functions across Units 52-02, 52-03, and 52-06.

The test must separately assert that every worked expansion includes an integral, a coefficient formula, a final series, and a pointwise convergence statement. It must reject claims that the series necessarily converges to the originally assigned value at a jump.

- [ ] **Step 2: Run red**

Run: `python3.12 -m unittest tests.test_chapter_52 -v`

Expected: FAIL because Chapter 52 is absent.

- [ ] **Step 3: Write the six units with a one-way proof chain**

Derive translation, scaling, and parity rules from the coefficient integrals. For half-range series, state the selected odd or even periodic extension before calculating. Derive the Dirichlet kernel from the finite trigonometric sum and prove its normalization. Prove the book's piecewise-smooth Dirichlet theorem from the kernel representation and oscillatory cancellation, with endpoint periodic identification explicit.

Advance totals to 245 units and 422 hours. Publish only through Chapter 52.

- [ ] **Step 4: Verify, review, and commit**

Run the Chapter 52, Part XII, content, strict-build, rendered-site, and diff checks. Commit only the chapter checkpoint with `docs: publish chapter 52 fourier convergence`.

## Task 5: Publish Chapter 53

**Files:** Create the Chapter 53 guide, five units, `tests/test_chapter_53.py`, and its review; modify the shared publication surfaces.

- [ ] **Step 1: Write the failing Chapter 53 contract**

Lock 50 exercises, at least 60 answers, exact metadata, the finite-error identity, Bessel inequality, Parseval hypotheses, classic series-sum calculations, and stable examples separating mean-square, pointwise, and uniform convergence. Require these proof-order assertions:

```python
self.assertNotIn("由 Parseval", bessel_proof_core)
self.assertIn("非负", bessel_proof_core)
self.assertIn("最佳平方逼近", mean_square_unit)
self.assertIn("先验证", parseval_sum_unit)
```

Forbid abstract Hilbert-space projection, Riesz–Fischer, general `L^p`, and unproved completeness claims in proof cores.

- [ ] **Step 2: Run red and write the five units**

Derive Bessel from nonnegative finite-order square error. Prove the exact error identity before taking limits. State and prove the book's Parseval version with its approximation input explicit. Use verified square-wave and absolute-value expansions to derive classic reciprocal-square or reciprocal-fourth sums, checking normalization before substitution.

- [ ] **Step 3: Publish, verify, review, and commit**

Advance totals to 250 units and 430 hours. Publish only through Chapter 53. Run focused and full gates, then commit with `docs: publish chapter 53 parseval theory`.

## Task 6: Publish Chapter 54

**Files:** Create the Chapter 54 guide, five units, `tests/test_chapter_54.py`, and its review; modify shared publication surfaces and rendered-site checks.

- [ ] **Step 1: Write the failing Chapter 54 contract**

Lock 50 exercises, at least 60 answers, exact metadata, finite reconstruction, the three distinct Gibbs claims, Fejér-kernel positivity/normalization/concentration, truncation and sampled-error limitations, and the six-step final model. Require `finite_truncation_only` wherever program output appears.

Require the final model to contain, in order, `问题定义`, `周期归一化`, `解析系数`, `有限重建`, `误差指标`, and `结论边界`. Forbid FFT, DFT, sampling-theorem, Fourier-transform, multidimensional-series, and PDE claims in proof cores.

- [ ] **Step 2: Run red and write Gibbs and Fejér without numerical substitution**

Distinguish the half-sum limit at the jump, persistent relative overshoot near the jump, and shrinking overshoot-region width. Derive the Fejér kernel from arithmetic means, then prove positivity, unit mass, and concentration. Use those properties to prove uniform convergence for continuous periodic functions and state the verified piecewise-continuous point conclusions.

- [ ] **Step 3: Close the opening square-wave problem and publish**

Return to the same square wave introduced in Chapter 51. Identify exactly where Chapters 51–54 answer the four opening questions. Advance totals to 255 units and 438 hours. Add representative Part XII pages and anchors to `tests/test_mkdocs_site.py`, `tests/test_zensical_structure.py`, and `scripts/check_site.py`. Keep Chapter 55 absent.

- [ ] **Step 4: Verify, review, and commit**

```bash
python3.12 -m unittest tests.test_fourier_series tests.test_chapter_54 tests.test_part_12_consistency -v
make verify
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
git add content/chapters/chapter-54 tests/test_chapter_54.py docs/reviews/2026-08-01-chapter-54-consistency-review.md docs/curriculum/part-12-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_mkdocs_site.py tests/test_zensical_structure.py scripts/check_site.py
git commit -m "docs: publish chapter 54 fourier models"
```

## Task 7: Close Part XII and whole-book consistency

**Files:**
- Create: `docs/reviews/2026-08-01-part-12-consistency-review.md`
- Modify: `tests/test_part_12_consistency.py`
- Modify: `docs/curriculum/part-05-dependencies.md`, `part-06-dependencies.md`, `part-10-dependencies.md`, `part-11-dependencies.md`, `part-12-dependencies.md`
- Modify: `README.md`, `content/course-map.md`, `mkdocs.yml`, `tests/test_mkdocs_site.py`, `tests/test_zensical_structure.py`, `scripts/check_site.py`

- [ ] **Step 1: Expand the final consistency test**

Assert 21 unique Part XII pages, 255 book units, 438 book hours, exact dependency rows, exact navigation order, exactly one implementation of each public Fourier computation, no Chapter 55, four chapter reviews, and one final review. Assert that the opening square wave appears in the Part XII introduction and every chapter, with no premature theorem use.

- [ ] **Step 2: Audit all critical mathematics line by line**

Record checks for trigonometric orthogonality and normalization; finite best approximation; real/complex conversion; all four analytic expansions; Dirichlet-kernel identity and convergence proof; half-sum values; Bessel proof order; finite-error identity; Parseval assumptions and series sums; convergence-mode distinctions; Gibbs claims; Fejér-kernel proof; and every counterexample calculation. Machine markers do not certify mathematical correctness.

- [ ] **Step 3: Update cross-part handoffs and publication language**

Record the exact Part XII units consuming Riemann integration, uniform convergence, parameter-integral exchange, and Lebesgue convergence. Replace every “future Fourier” statement in the touched dependency files with precise published interfaces. Preserve historical part totals and do not invent a Part XIII.

- [ ] **Step 4: Run the complete release audit**

```bash
make verify
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
git status --short
```

Expected: 0 failures; 21 Part XII pages; final totals 255 units and 438 hours; release boundary Chapter 54; only known pre-existing untracked artifacts may remain; Chapter 55 does not exist.

- [ ] **Step 5: Commit closure**

```bash
git add README.md content/course-map.md mkdocs.yml scripts/check_site.py tests docs/curriculum docs/reviews/2026-08-01-part-12-consistency-review.md
git commit -m "docs: close part 12 and textbook consistency audit"
```

## Plan self-review

- Every design requirement maps to a task: locked curriculum (Task 1), finite computation (Task 2), projection (Task 3), analytic expansions and pointwise convergence (Task 4), energy and mean-square convergence (Task 5), Gibbs/Fejér/modeling (Task 6), and whole-book publication closure (Task 7).
- The Bessel task explicitly prevents circular dependence on Parseval; the Dirichlet task derives the kernel before using it; the Fejér task proves kernel properties before convergence.
- All four required analytic expansions, both half-range choices, and Parseval-based series sums are core-assessed content rather than optional examples.
- The three numerical interfaces are finite and non-certifying by type, status, tests, and page language.
- Historical Part XI totals remain frozen while its stale future-neighbor assertion is scoped away.
- No placeholders, future chapters, or out-of-scope Hilbert, Fourier-transform, DFT/FFT, PDE, or sampling-theorem implementations remain.
