# Part VIII Multiple Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Part VIII as 18 rigorous self-study units covering Riemann multiple integration, iterated integration, change of variables, improper multiple integrals, and mass and joint-density models, plus one non-core Jordan-content appendix and one tested two-dimensional midpoint implementation.

**Architecture:** Implement one dependency-closed chapter at a time behind locked metadata, proof, training, scope, and publication contracts. Keep the core at 24 theory plus 8 application hours; the optional appendix never becomes a prerequisite or enters the core totals. Put the only executable numerical method in `src/mathbook_examples/multiple_integration.py`, and make the textbook import that implementation instead of copying it.

**Tech Stack:** Python 3.12 standard library, frozen dataclasses, `unittest`, PyYAML, Markdown with Zensical/MkDocs, MathJax, existing `scripts/check_content.py`, `scripts/check_site.py`, and `make verify`.

---

## Locked curriculum registry

```python
PART_08_UNITS = [
    ("u-08-33-01", "小矩形上的局部贡献怎样累积成二重积分？", 1.50, 0.25, "riemann-double-integral", 8, 10),
    ("u-08-33-02", "连续函数为什么在闭矩形上可积？", 1.75, 0.00, "continuous-integrability", 9, 11),
    ("u-08-33-03", "线性、序关系与区域可加性怎样成立？", 1.50, 0.25, "integral-properties", 8, 10),
    ("u-08-33-04", "怎样在常用有界区域上定义重积分？", 1.50, 0.25, "bounded-regions", 9, 11),
    ("u-08-34-01", "矩形上的二重积分为什么可以逐次计算？", 1.50, 0.25, "iterated-integral-theorem", 9, 11),
    ("u-08-34-02", "x-型与 y-型区域怎样写出积分限？", 1.25, 0.50, "type-i-ii-regions", 10, 12),
    ("u-08-34-03", "改变积分次序怎样化简区域与被积函数？", 1.00, 0.75, "change-order", 10, 12),
    ("u-08-34-04", "三重积分怎样按截面或投影逐层计算？", 1.25, 0.50, "triple-integrals", 9, 11),
    ("u-08-34-05", "二维张量积中点法能保证什么、不能保证什么？", 1.00, 1.00, "tensor-midpoint", 12, 15),
    ("u-08-35-01", "Jacobian 行列式为什么描述局部面积与体积伸缩？", 1.50, 0.25, "jacobian-scaling", 9, 11),
    ("u-08-35-02", "重积分换元公式需要哪些条件？", 1.50, 0.25, "change-of-variables", 10, 12),
    ("u-08-35-03", "极坐标怎样处理圆形与径向对称区域？", 1.50, 0.25, "polar-coordinates", 10, 12),
    ("u-08-35-04", "柱面、球面坐标怎样处理三维区域？", 1.50, 0.25, "cylindrical-spherical", 11, 13),
    ("u-08-36-01", "无界区域上的重积分怎样由极限定义？", 1.50, 0.25, "unbounded-regions", 9, 11),
    ("u-08-36-02", "被积函数有奇点时怎样判断收敛？", 1.50, 0.25, "singular-integrands", 10, 12),
    ("u-08-36-03", "密度怎样产生质量、质心与转动惯量？", 1.00, 0.75, "mass-centroid-inertia", 10, 12),
    ("u-08-36-04", "联合密度怎样产生边缘密度、期望与协方差？", 0.75, 1.00, "joint-density", 10, 12),
    ("u-08-36-05", "怎样为空间累积模型选择区域、坐标与核验方法？", 1.00, 1.00, "spatial-modeling", 12, 15),
]
```

Locked core totals: 18 units, 24 theory hours, 8 application hours, 32 hours,
175 anchored exercises, and 213 collapsed answers. The optional appendix is
approximately 2 hours and is excluded from every core total.

## File map

### Create

- `docs/curriculum/part-08-dependencies.md` — direct prerequisites, unique outputs, hours, scope boundaries, and release status.
- `content/chapters/chapter-33/` through `content/chapters/chapter-36/` — four guides and 18 core unit pages.
- `content/appendices/part-08-jordan-content.md` — non-core bridge from common regions to Jordan content and the later measure viewpoint.
- `tests/test_chapter_33.py` through `tests/test_chapter_36.py` — locked chapter metadata, proof, boundary, training, and publication contracts.
- `src/mathbook_examples/multiple_integration.py` — the only two-dimensional tensor midpoint implementation.
- `tests/test_multiple_integration.py` — numerical behavior and failure semantics.
- `tests/test_part_08_consistency.py` — final dependency, totals, scope, navigation, appendix, and unique-source contracts.
- `docs/reviews/2026-07-31-chapter-33-consistency-review.md` through `docs/reviews/2026-07-31-chapter-36-consistency-review.md`.
- `docs/reviews/2026-07-31-part-08-consistency-review.md`.

### Modify

- `mkdocs.yml` — publish only the chapter or appendix reached by the current checkpoint.
- `content/course-map.md` — add the blueprint, then advance chapter status one checkpoint at a time.
- `README.md` — advance the publication boundary, unit count, and hours only after each green checkpoint.
- `tests/test_mkdocs_site.py` — register representative built pages, anchors, and navigation markers.
- `tests/test_mkdocs_structure.py` or the current navigation contract file — include Part VIII only when its first chapter is published.
- `src/mathbook_examples/__init__.py` — keep as a package marker; do not re-export the new API.

## Shared content contract

Every core unit uses `content_standard: 2`, declares exact book, higher-algebra,
analytic-geometry, and Python prerequisites, contains its stable unit anchor,
at least two anchored examples, at least two immediate checks, and the exact
exercise and answer counts in the registry. Use these headings in order:

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

The computational unit additionally uses:

```markdown
### 问题来源
### 数学转化
### 算法思想
### 误差与适用条件
### 伪代码
### Python
### 结果解释
```

No core page may require Jordan measure, Lebesgue measure, almost-everywhere
language, measure-theoretic Fubini–Tonelli, conditional distributions, line or
surface integrals, or Green/Gauss/Stokes.

## Task 1: Lock the Part VIII blueprint

**Files:**
- Create: `docs/curriculum/part-08-dependencies.md`
- Create: `tests/test_part_08_consistency.py`
- Modify: `content/course-map.md`

- [ ] **Step 1: Write the failing blueprint test**

Create `tests/test_part_08_consistency.py` with a compact copy of all 18
`(unit_id, theory, applied)` rows and these initial assertions:

```python
def test_locked_part_totals(self):
    theory = sum(unit[1] for unit in PART_08_UNITS)
    applied = sum(unit[2] for unit in PART_08_UNITS)
    self.assertEqual(
        (18, 24.0, 8.0, 32.0),
        (len(PART_08_UNITS), theory, applied, theory + applied),
    )

def test_blueprint_starts_after_part_seven(self):
    text = self.required_text(DEPENDENCIES)
    self.assertIn("当前发布边界：第 32 章", text)
    self.assertIn("18 个核心单元、32 学时", text)
    self.assertNotIn("chapters/chapter-33/", NAVIGATION)

def test_appendix_is_not_a_core_prerequisite(self):
    text = self.required_text(DEPENDENCIES)
    self.assertIn("选读附录不计入核心学时", text)
    for line in text.splitlines():
        if line.startswith("| `u-08-"):
            self.assertNotIn("Jordan", line)
```

- [ ] **Step 2: Run the test and verify the dependency map is missing**

Run: `python3.12 -m unittest tests.test_part_08_consistency -v`

Expected: FAIL because `docs/curriculum/part-08-dependencies.md` is absent.

- [ ] **Step 3: Write the dependency map and course blueprint**

Create one dependency row for every locked unit. Record direct prerequisites,
unique output, chapter totals, the core/appendix distinction, and these
boundaries: classical Riemann theory only; no measure-theoretic Fubini–Tonelli;
no curve or surface integration; no conditional distributions; no general
multidimensional cubature. Add all four chapters and the optional appendix to
the course map as “规划中”. Do not create content pages or navigation.

- [ ] **Step 4: Run the focused and baseline gates**

Run:

```bash
python3.12 -m unittest tests.test_part_08_consistency -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: all commands exit 0; the published site still stops at Chapter 32.

- [ ] **Step 5: Commit the blueprint**

```bash
git add docs/curriculum/part-08-dependencies.md content/course-map.md tests/test_part_08_consistency.py
git commit -m "docs: lock part 08 curriculum blueprint"
```

## Task 2: Publish Chapter 33

**Files:**
- Create: `content/chapters/chapter-33/index.md`
- Create: `content/chapters/chapter-33/u-08-33-01-riemann-double-integral.md`
- Create: `content/chapters/chapter-33/u-08-33-02-continuous-integrability.md`
- Create: `content/chapters/chapter-33/u-08-33-03-integral-properties.md`
- Create: `content/chapters/chapter-33/u-08-33-04-bounded-regions.md`
- Create: `tests/test_chapter_33.py`
- Create: `docs/reviews/2026-07-31-chapter-33-consistency-review.md`
- Modify: `docs/curriculum/part-08-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`

- [ ] **Step 1: Write the failing Chapter 33 contract**

Copy the four Chapter 33 registry rows into `tests/test_chapter_33.py`. Reuse the
metadata, guide-link, exercise, answer, and content-standard checks from
`tests/test_chapter_32.py`. Lock these content markers:

```python
REQUIRED_MARKERS = {
    "u-08-33-01": ("分割", "小矩形直径", "Riemann 和", "取样无关"),
    "u-08-33-02": ("一致连续", "振幅", "连续函数", "可积"),
    "u-08-33-03": ("线性", "单调性", "绝对值估计", "区域可加性"),
    "u-08-33-04": ("区域外补零", "分片光滑边界", "三重积分", "不发展 Jordan 测度"),
}
```

Require the anchors:

```python
REQUIRED_ANCHORS = {
    "u-08-33-01": ("def-u-08-33-01-riemann-double-integral",),
    "u-08-33-02": ("thm-u-08-33-02-continuous-integrable",),
    "u-08-33-03": ("thm-u-08-33-03-integral-properties",),
    "u-08-33-04": ("def-u-08-33-04-region-integral",),
}
```

- [ ] **Step 2: Run the contract and verify it fails**

Run: `python3.12 -m unittest tests.test_chapter_33 -v`

Expected: FAIL because `content/chapters/chapter-33/` is absent.

- [ ] **Step 3: Write 33.1 and 33.2**

In 33.1, derive the definition from volume sums over a tagged rectangular
partition. State the epsilon–mesh formulation and prove independence from
sample choices once the limit exists. Use one constant and one affine example,
plus a bounded discontinuous counterexample that exposes why boundedness alone
does not prove integrability.

In 33.2, prove continuous integrability by choosing a uniform-continuity scale,
bounding every subrectangle oscillation, and comparing upper and lower sums.
Mark exactly where compactness and continuity are used. Include a proof
workshop that reconstructs the global oscillation bound from local estimates.

- [ ] **Step 4: Write 33.3 and 33.4**

In 33.3, prove linearity, order preservation, the absolute-value inequality,
and finite additivity under rectangular subdivision. Distinguish an oriented
formula from a nonnegative geometric volume.

In 33.4, define integration over a bounded common region by zero extension to
a containing rectangle. Restrict the usable criterion to the named common
piecewise-smooth regions, extend notation to triple integrals, and state that
the appendix—not the core proof chain—explains Jordan content.

- [ ] **Step 5: Publish only Chapter 33**

Add Part VIII and Chapter 33 to `mkdocs.yml`. Update the course map and
dependency map to mark Chapter 33 published and Chapters 34–36 plus the
appendix planned. Update README totals by adding 4 units and 7 hours to the
currently published totals; derive the numbers from the current README rather
than copying stale plan-time totals.

- [ ] **Step 6: Run chapter gates and write the review**

Run:

```bash
python3.12 -m unittest tests.test_chapter_33 tests.test_part_08_consistency -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Record exact unit, hour, exercise, answer, dependency, scope, build, and
rendered-anchor results in the Chapter 33 review.

- [ ] **Step 7: Commit Chapter 33**

```bash
git add content/chapters/chapter-33 docs/curriculum/part-08-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_33.py docs/reviews/2026-07-31-chapter-33-consistency-review.md
git commit -m "docs: publish chapter 33 multiple integrals"
```

## Task 3: Build the two-dimensional midpoint implementation with TDD

**Files:**
- Create: `src/mathbook_examples/multiple_integration.py`
- Create: `tests/test_multiple_integration.py`

- [ ] **Step 1: Write failing result and exactness tests**

Create tests for this public API:

```python
from mathbook_examples.multiple_integration import (
    Midpoint2DResult,
    tensor_midpoint_2d,
)

result = tensor_midpoint_2d(
    lambda x, y: 3.0,
    x_bounds=(0.0, 2.0),
    y_bounds=(-1.0, 1.0),
    nx=4,
    ny=5,
)
self.assertIsInstance(result, Midpoint2DResult)
self.assertEqual(12.0, result.value)
self.assertEqual((4, 5, 20), (result.nx, result.ny, result.evaluations))
```

Also require exact integration, to floating-point tolerance, for
`f(x, y) = 2*x - 3*y + 4` on a nonsymmetric rectangle and for the separable
function `f(x, y) = x*y` on `[0, 2] × [1, 3]`.

- [ ] **Step 2: Write failing validation tests**

Require `ValueError` for reversed or equal bounds, zero or negative `nx`/`ny`,
boolean subdivisions, noninteger subdivisions, nonfinite bounds, a non-scalar
return, a nonfinite return, and a nonfinite accumulated result. Require the
result dataclass to be frozen.

- [ ] **Step 3: Run the tests and verify the import fails**

Run: `python3.12 -m unittest tests.test_multiple_integration -v`

Expected: FAIL with `ModuleNotFoundError` for
`mathbook_examples.multiple_integration`.

- [ ] **Step 4: Implement the minimal public API**

Implement this interface:

```python
from dataclasses import dataclass
import math
from typing import Callable


@dataclass(frozen=True)
class Midpoint2DResult:
    value: float
    x_bounds: tuple[float, float]
    y_bounds: tuple[float, float]
    nx: int
    ny: int
    evaluations: int


def tensor_midpoint_2d(
    function: Callable[[float, float], float],
    *,
    x_bounds: tuple[float, float],
    y_bounds: tuple[float, float],
    nx: int,
    ny: int,
) -> Midpoint2DResult:
    if isinstance(nx, bool) or not isinstance(nx, int) or nx <= 0:
        raise ValueError("nx must be a positive integer")
    if isinstance(ny, bool) or not isinstance(ny, int) or ny <= 0:
        raise ValueError("ny must be a positive integer")

    try:
        x0, x1 = (float(value) for value in x_bounds)
        y0, y1 = (float(value) for value in y_bounds)
    except (TypeError, ValueError) as error:
        raise ValueError("bounds must contain two finite numbers") from error
    if not all(math.isfinite(value) for value in (x0, x1, y0, y1)):
        raise ValueError("bounds must be finite")
    if not x0 < x1 or not y0 < y1:
        raise ValueError("bounds must be strictly increasing")

    dx = (x1 - x0) / nx
    dy = (y1 - y0) / ny
    values: list[float] = []
    for i in range(nx):
        x = x0 + (i + 0.5) * dx
        for j in range(ny):
            y = y0 + (j + 0.5) * dy
            try:
                value = float(function(x, y))
            except (TypeError, ValueError) as error:
                raise ValueError("integrand must return a finite scalar") from error
            if not math.isfinite(value):
                raise ValueError("integrand must return a finite scalar")
            values.append(value)

    integral = dx * dy * math.fsum(values)
    if not math.isfinite(integral):
        raise ValueError("integral accumulation must be finite")
    return Midpoint2DResult(
        value=integral,
        x_bounds=(x0, x1),
        y_bounds=(y0, y1),
        nx=nx,
        ny=ny,
        evaluations=nx * ny,
    )
```

Validate booleans before integers because `bool` subclasses `int`. Convert
accepted bounds and function values to `float`, check `math.isfinite`, evaluate
only at cell midpoints, and accumulate with `math.fsum`. Do not add automatic
refinement, tolerances, certification fields, arbitrary regions, NumPy, or
Monte Carlo.

- [ ] **Step 5: Run tests and inspect coverage of failure semantics**

Run:

```bash
python3.12 -m unittest tests.test_multiple_integration -v
python3.12 -m unittest discover -s tests -v
git diff --check
```

Expected: all tests pass. The result is immutable, evaluation count is exactly
`nx * ny`, and every invalid-input class has a test.

- [ ] **Step 6: Commit the numerical module**

```bash
git add src/mathbook_examples/multiple_integration.py tests/test_multiple_integration.py
git commit -m "feat: add tensor midpoint integration"
```

## Task 4: Publish Chapter 34

**Files:**
- Create: `content/chapters/chapter-34/index.md`
- Create: `content/chapters/chapter-34/u-08-34-01-iterated-integral-theorem.md`
- Create: `content/chapters/chapter-34/u-08-34-02-type-i-ii-regions.md`
- Create: `content/chapters/chapter-34/u-08-34-03-change-order.md`
- Create: `content/chapters/chapter-34/u-08-34-04-triple-integrals.md`
- Create: `content/chapters/chapter-34/u-08-34-05-tensor-midpoint.md`
- Create: `tests/test_chapter_34.py`
- Create: `docs/reviews/2026-07-31-chapter-34-consistency-review.md`
- Modify: `tests/test_mkdocs_site.py`
- Modify: publication files from Task 2.

- [ ] **Step 1: Write the failing Chapter 34 contract**

Lock the five registry rows, exact totals `(6.0, 3.0, 50, 61)`, guide links,
shared headings, and:

```python
REQUIRED_MARKERS = {
    "u-08-34-01": ("累次积分", "连续", "闭矩形", "完整证明"),
    "u-08-34-02": ("x-型区域", "y-型区域", "投影", "积分限"),
    "u-08-34-03": ("重新描述区域", "改变次序", "分片", "不能机械交换"),
    "u-08-34-04": ("三重积分", "截面", "投影", "积分次序"),
    "u-08-34-05": ("mathbook_examples.multiple_integration", "张量积中点法", "误差前提", "不能证明可积性"),
}
```

Assert that 34.5 imports `tensor_midpoint_2d`, does not contain
`def tensor_midpoint_2d(`, and contains all seven computational headings.

- [ ] **Step 2: Run the contract and verify it fails**

Run: `python3.12 -m unittest tests.test_chapter_34 -v`

Expected: FAIL because Chapter 34 pages are absent.

- [ ] **Step 3: Write 34.1 through 34.3**

Prove the continuous rectangular iterated-integral theorem by first showing
that the inner integral is a continuous function of the outer variable, then
matching iterated Riemann sums with the double Riemann sum. Do not call the
result measure-theoretic Fubini–Tonelli.

For type-I/type-II regions, derive limits from projections and boundary graphs.
For changing order, require a sketch or inequality description before every
new integral; include one region requiring a split and one example where
unjustified swapping changes the meaning of an improper expression.

- [ ] **Step 4: Write 34.4 and 34.5**

Teach triple integration through slices and projections without developing
general \(n\)-dimensional notation. In 34.5, derive the tensor rule from the
one-dimensional midpoint rule, state the smoothness and derivative-bound
requirements for an error claim, present pseudocode, import the tested source,
and compare one analytic integral with grid refinements. When derivative
constants are missing, label the result an approximation rather than a
certificate.

- [ ] **Step 5: Publish, render-check, review, and commit Chapter 34**

Add only Chapter 34 navigation. Add representative built anchors for 34.1 and
34.5 to `tests/test_mkdocs_site.py`. Update counts from the current published
state by 5 units and 9 hours. Run:

```bash
python3.12 -m unittest tests.test_chapter_34 tests.test_multiple_integration tests.test_part_08_consistency tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Write the Chapter 34 review, including unique-source and non-certificate
semantics, then commit:

```bash
git add content/chapters/chapter-34 docs/curriculum/part-08-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_34.py tests/test_mkdocs_site.py docs/reviews/2026-07-31-chapter-34-consistency-review.md
git commit -m "docs: publish chapter 34 iterated integration"
```

## Task 5: Publish Chapter 35

**Files:**
- Create: `content/chapters/chapter-35/index.md`
- Create: `content/chapters/chapter-35/u-08-35-01-jacobian-scaling.md`
- Create: `content/chapters/chapter-35/u-08-35-02-change-of-variables.md`
- Create: `content/chapters/chapter-35/u-08-35-03-polar-coordinates.md`
- Create: `content/chapters/chapter-35/u-08-35-04-cylindrical-spherical.md`
- Create: `tests/test_chapter_35.py`
- Create: `docs/reviews/2026-07-31-chapter-35-consistency-review.md`
- Modify: `tests/test_mkdocs_site.py`
- Modify: publication files.

- [ ] **Step 1: Write the failing Chapter 35 contract**

Lock the four registry rows and totals `(6.0, 1.0, 40, 48)`. Require:

```python
REQUIRED_MARKERS = {
    "u-08-35-01": ("线性变换", "行列式绝对值", "局部伸缩", "取向"),
    "u-08-35-02": ("一一对应", "连续可微", "Jacobian 不退化", "边界分片"),
    "u-08-35-03": ("极坐标", "r", "theta", "Jacobian"),
    "u-08-35-04": ("柱面坐标", "球面坐标", "rho^2", "sin"),
}
```

Require a theorem anchor for change of variables and derivation anchors for
polar and spherical volume factors. Reject pages that merely say “由公式可得”
without a Jacobian determinant calculation.

- [ ] **Step 2: Run the contract and verify it fails**

Run: `python3.12 -m unittest tests.test_chapter_35 -v`

Expected: FAIL because Chapter 35 pages are absent.

- [ ] **Step 3: Write 35.1 and 35.2**

Derive area and volume scaling first for diagonal maps, shears, and general
invertible linear maps. Explain why integration uses the absolute determinant
while orientation still matters elsewhere.

State the classical change-of-variables theorem with an injective \(C^1\)
transformation, nonvanishing Jacobian on the relevant interior, and finite
boundary decomposition. Give the complete proof route: local linearization,
small-cell distortion, finite covering/partition control, Riemann-sum
comparison, and boundary handling. Every hypothesis must have a named use and
a failure example. Do not invoke Lebesgue measure.

- [ ] **Step 4: Write 35.3 and 35.4**

Derive the polar Jacobian \(r\), state angle-range and origin-overlap cautions,
and solve both a disk and an annular-sector example. Derive cylindrical
`r` and spherical `rho^2 sin(phi)` factors from their coordinate maps. Include
one ball integral, one cone or spherical sector, and a method-selection table
that checks symmetry, injectivity, coordinate ranges, and Jacobian zeros.

- [ ] **Step 5: Publish, render-check, review, and commit Chapter 35**

Add Chapter 35 navigation and representative built anchors for 35.2 and 35.4.
Update current totals by 4 units and 7 hours. Run focused tests, content checks,
strict build, site checks, and `git diff --check`. Write the review with an
explicit statement that the proof is classical Riemann-level and does not
borrow measure theory. Commit:

```bash
git add content/chapters/chapter-35 docs/curriculum/part-08-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_35.py tests/test_mkdocs_site.py docs/reviews/2026-07-31-chapter-35-consistency-review.md
git commit -m "docs: publish chapter 35 change of variables"
```

## Task 6: Publish Chapter 36

**Files:**
- Create: `content/chapters/chapter-36/index.md`
- Create: `content/chapters/chapter-36/u-08-36-01-unbounded-regions.md`
- Create: `content/chapters/chapter-36/u-08-36-02-singular-integrands.md`
- Create: `content/chapters/chapter-36/u-08-36-03-mass-centroid-inertia.md`
- Create: `content/chapters/chapter-36/u-08-36-04-joint-density.md`
- Create: `content/chapters/chapter-36/u-08-36-05-spatial-modeling.md`
- Create: `tests/test_chapter_36.py`
- Create: `docs/reviews/2026-07-31-chapter-36-consistency-review.md`
- Modify: `tests/test_mkdocs_site.py`
- Modify: publication files.

- [ ] **Step 1: Write the failing Chapter 36 contract**

Lock the five rows and totals `(5.75, 3.25, 51, 62)`. Require:

```python
REQUIRED_MARKERS = {
    "u-08-36-01": ("无界区域", "区域穷竭", "非负函数", "极限方式"),
    "u-08-36-02": ("奇点", "挖去邻域", "绝对收敛", "路径风险"),
    "u-08-36-03": ("质量", "质心", "转动惯量", "单位"),
    "u-08-36-04": ("联合密度", "非负", "归一化", "边缘密度", "协方差"),
    "u-08-36-05": ("区域", "坐标", "量纲", "独立核验", "Monte Carlo 选读"),
}
```

Assert that no Chapter 36 page contains a section teaching conditional density,
sigma-algebras, or a Monte Carlo API.

- [ ] **Step 2: Run the contract and verify it fails**

Run: `python3.12 -m unittest tests.test_chapter_36 -v`

Expected: FAIL because Chapter 36 pages are absent.

- [ ] **Step 3: Write 36.1 and 36.2**

For nonnegative functions on unbounded regions, define the integral through
named increasing bounded subregions and compare standard radial or rectangular
exhaustions only in cases where the classical conclusion is justified.
Do not cite the Lebesgue monotone convergence theorem.

For isolated singularities, define punctured-domain limits and use polar or
spherical coordinates for comparison. Include one convergent and one divergent
power singularity. Show with a sign-changing example why absolute convergence
or explicit exhaustion information matters.

- [ ] **Step 4: Write 36.3 and 36.4**

Build mass, centroid, and inertia formulas from local density times area/volume,
with units and symmetry checks. For probability, first verify density
nonnegativity and normalization, then derive marginal densities, expectation,
second moments, and covariance by integration. Do not teach conditional
distributions or the probability axiom system.

- [ ] **Step 5: Write the capstone 36.5**

Use a bounded or convergent spatial-density model requiring region selection,
coordinate choice, an analytic computation, unit checking, and one independent
numerical or symmetry check. The Monte Carlo paragraph is explicitly labeled
选读观察, contains no reusable implementation, and makes no confidence-interval
or convergence-rate claim.

- [ ] **Step 6: Publish, render-check, review, and commit Chapter 36**

Add Chapter 36 navigation and representative built anchors for 36.2 and 36.4.
Update the current totals by 5 units and 9 hours. Mark all four core chapters
published but keep the appendix planned. Run:

```bash
python3.12 -m unittest tests.test_chapter_36 tests.test_part_08_consistency tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Write the Chapter 36 review, then commit:

```bash
git add content/chapters/chapter-36 docs/curriculum/part-08-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_36.py tests/test_mkdocs_site.py docs/reviews/2026-07-31-chapter-36-consistency-review.md
git commit -m "docs: publish chapter 36 improper multiple integrals"
```

## Task 7: Publish the optional Jordan-content appendix

**Files:**
- Create: `content/appendices/part-08-jordan-content.md`
- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `docs/curriculum/part-08-dependencies.md`
- Modify: `tests/test_part_08_consistency.py`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Extend the consistency test and verify failure**

Require the appendix page, one navigation occurrence, the label “选读，不计入
第八部核心学时”, and these markers:

```python
for marker in (
    "有限矩形并",
    "Jordan 内内容",
    "Jordan 外内容",
    "Jordan 可测",
    "边界",
    "Lebesgue 测度",
    "第十一部",
):
    self.assertIn(marker, appendix)
```

Assert the appendix has no core unit ID beginning with `u-08-`, no `hours:`
metadata counted by
core tests, and no dependency-map row uses it as a prerequisite.

Run: `python3.12 -m unittest tests.test_part_08_consistency -v`

Expected: FAIL because the appendix page is absent.

- [ ] **Step 2: Write the two-section appendix**

Section A.1 defines inner and outer Jordan content using finite unions of
rectangles and defines Jordan measurability by equality. Section A.2 gives the
boundary criterion for common piecewise-smooth regions, explains why the core
zero-extension convention works there, and exhibits a bounded set that exposes
Jordan theory’s limitation. End with a precise bridge to Part XI; do not define
sigma-algebras, measurable functions, or the Lebesgue integral.

- [ ] **Step 3: Publish and verify the appendix**

Add one appendix navigation entry after Chapter 36, mark it published in the
course map and dependency map, and keep README core unit/hour totals unchanged.
Run:

```bash
python3.12 -m unittest tests.test_part_08_consistency tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

- [ ] **Step 4: Commit the appendix**

```bash
git add content/appendices/part-08-jordan-content.md mkdocs.yml content/course-map.md docs/curriculum/part-08-dependencies.md tests/test_part_08_consistency.py tests/test_mkdocs_site.py
git commit -m "docs: add optional Jordan content appendix"
```

## Task 8: Audit and close Part VIII

**Files:**
- Create: `docs/reviews/2026-07-31-part-08-consistency-review.md`
- Modify: `tests/test_part_08_consistency.py`
- Modify: `README.md`
- Modify: `content/course-map.md`
- Modify: `docs/curriculum/part-08-dependencies.md`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Strengthen the final consistency contract**

Add tests that discover exactly 18 `u-08-*.md` core pages under Chapters 33–36,
sum metadata to `(24.0, 8.0, 32.0)`, match the exact locked ID set, and find
each page exactly once in navigation. Require 175 exercise anchors and 213
collapsed answers across the core.

Require:

```python
self.assertIn("第八部已经完整发布", README)
self.assertIn("当前发布边界：第 36 章", dependencies)
self.assertIn("18 个核心单元、32 学时", dependencies)
self.assertNotIn("chapters/chapter-37/", navigation)
```

Verify that only 34.5 imports `mathbook_examples.multiple_integration`, no page
copies `def tensor_midpoint_2d(`, and the appendix remains outside core totals.

- [ ] **Step 2: Run the final contract and fix publication drift**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_33 \
  tests.test_chapter_34 \
  tests.test_chapter_35 \
  tests.test_chapter_36 \
  tests.test_multiple_integration \
  tests.test_part_08_consistency \
  tests.test_mkdocs_site -v
```

Expected: all tests pass. Fix only Part VIII inconsistencies revealed by the
contract; do not refactor earlier parts.

- [ ] **Step 3: Run the full quality gate**

Run:

```bash
make verify
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: every command exits 0.

- [ ] **Step 4: Perform the 390 × 844 visual audit**

Serve the built site and inspect:

- 33.1 Riemann double-integral definition;
- 34.5 tensor midpoint code and result explanation;
- 35.2 change-of-variables theorem;
- 35.4 spherical-coordinate formulas;
- 36.4 joint-density model;
- the Jordan-content appendix.

For every page record MathJax visibility, stable anchors, collapsed answers,
code-block containment where applicable, sidebar context, and absence of
page-level horizontal overflow. Use the real rendered site; automated source
checks do not replace this audit.

- [ ] **Step 5: Write the final consistency review**

Record:

- 18 core units, 24 theory hours, 8 application hours, and 32 total hours;
- 175 core exercises and 213 collapsed answers;
- the appendix’s non-core status;
- proof dependency and scope audit results;
- unique numerical source and failure semantics;
- exact quality-gate commands and outcomes;
- the six narrow-screen page results;
- confirmation that navigation stops before Chapter 37.

- [ ] **Step 6: Commit the closure**

```bash
git add docs/reviews/2026-07-31-part-08-consistency-review.md tests/test_part_08_consistency.py README.md content/course-map.md docs/curriculum/part-08-dependencies.md tests/test_mkdocs_site.py
git commit -m "docs: close part 08 consistency audit"
```

## Plan self-review checklist

- [ ] Every design requirement maps to a task.
- [ ] Registry hours sum to 24 theory, 8 application, and 32 total.
- [ ] Registry training counts sum to 175 exercises and 213 answers.
- [ ] The appendix is optional, non-core, and never a prerequisite.
- [ ] Core proofs do not require Jordan or Lebesgue theory.
- [ ] Only one page imports the only new numerical source.
- [ ] No task creates Chapter 37 content or navigation.
- [ ] Every chapter has a failing contract, green gate, review, and commit.
- [ ] Final verification includes both automated and browser-visible checks.

## Execution checkpoints

Execute Tasks 1–8 in order. Do not create later chapter pages early. After each
task, confirm the worktree is clean and the published boundary matches that
checkpoint before continuing.
