# Part IX Vector Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Part IX as 21 rigorous self-study units covering parameterized curves and surfaces, line and surface integrals, Green, Gauss, and Stokes theorems, plus one non-core differential-forms appendix and one tested non-certifying oriented-integration module.

**Architecture:** Implement one dependency-closed chapter at a time behind locked metadata, proof, orientation, training, scope, and publication contracts. Keep the core at 24 theory plus 8 application hours; the optional appendix never becomes a prerequisite or enters the core totals. Put both executable midpoint checks in one `src/mathbook_examples/vector_analysis.py` source and make textbook code import it rather than duplicate it.

**Tech Stack:** Python 3.12 standard library, frozen dataclasses, `unittest`, PyYAML, Markdown with Zensical/MkDocs, MathJax, existing `scripts/check_content.py`, `scripts/check_site.py`, and `make verify`.

---

## Locked curriculum registry

```python
PART_09_UNITS = [
    ("u-09-37-01", "正则参数曲线怎样描述运动、方向与切向量？", 1.50, 0.00, "regular-parametric-curves", 8, 10),
    ("u-09-37-02", "弧长与第一类曲线积分怎样由参数化定义？", 1.25, 0.25, "arc-length-scalar-line-integral", 9, 11),
    ("u-09-37-03", "第二类曲线积分怎样表示功与环流？", 1.00, 0.50, "work-circulation", 9, 11),
    ("u-09-37-04", "重新参数化、反向与保守场怎样改变积分？", 0.75, 0.75, "reparameterization-conservative-fields", 10, 12),
    ("u-09-38-01", "正则参数曲面怎样产生切平面、法向量与取向？", 1.50, 0.00, "regular-parametric-surfaces", 8, 10),
    ("u-09-38-02", "曲面面积元为什么由叉积的模给出？", 1.25, 0.25, "surface-area-element", 9, 11),
    ("u-09-38-03", "第一类曲面积分怎样累积曲面上的标量分布？", 1.00, 0.50, "scalar-surface-integral", 9, 11),
    ("u-09-38-04", "通量积分怎样依赖参数化与曲面取向？", 0.75, 0.75, "flux-integral", 10, 12),
    ("u-09-39-01", "平面场的散度与旋度怎样描述局部变化？", 1.50, 0.00, "planar-divergence-curl", 8, 10),
    ("u-09-39-02", "Green 公式怎样从简单区域上的微积分基本定理得到？", 1.25, 0.25, "green-theorem", 10, 12),
    ("u-09-39-03", "分片区域、多连通区域与边界方向怎样处理？", 1.00, 0.50, "multiply-connected-green", 10, 12),
    ("u-09-39-04", "Green 公式怎样控制面积、环流、通量与路径无关？", 0.75, 0.75, "green-applications", 11, 13),
    ("u-09-40-01", "三维散度为什么表示局部源汇密度？", 1.50, 0.00, "spatial-divergence", 8, 10),
    ("u-09-40-02", "Gauss 公式为什么先在长方体上成立？", 1.25, 0.25, "gauss-box", 10, 12),
    ("u-09-40-03", "规则区域的分片与内部通量为什么会抵消？", 1.00, 0.50, "gauss-piecewise-regions", 10, 12),
    ("u-09-40-04", "Gauss 公式怎样分析流量、电通量与奇点？", 0.75, 0.75, "gauss-applications-singularities", 11, 13),
    ("u-09-41-01", "三维旋度为什么表示局部环流密度？", 1.50, 0.00, "spatial-curl", 8, 10),
    ("u-09-41-02", "曲面取向怎样诱导边界曲线的正方向？", 1.25, 0.25, "induced-boundary-orientation", 9, 11),
    ("u-09-41-03", "Stokes 公式怎样在单个参数曲面片上证明？", 1.25, 0.25, "stokes-parametric-patch", 10, 12),
    ("u-09-41-04", "分片曲面上的内部边界为什么成对抵消？", 1.00, 0.50, "stokes-piecewise-surfaces", 10, 12),
    ("u-09-41-05", "怎样选择并核验 Green、Gauss 与 Stokes 公式？", 1.00, 1.00, "vector-theorem-selection", 12, 15),
]
```

Locked core totals: 21 units, 24 theory hours, 8 application hours, 32 hours,
201 anchored exercises, and 247 collapsed answers. The optional appendix is
approximately 2–3 hours and is excluded from every core total.

## File map

### Create

- `docs/curriculum/part-09-dependencies.md` — direct prerequisites, unique outputs, hours, proof order, orientation rules, scope boundaries, and release status.
- `content/chapters/chapter-37/` through `content/chapters/chapter-41/` — five guides and 21 core unit pages.
- `content/appendices/part-09-differential-forms.md` — non-core classical-to-forms comparison after Chapter 41.
- `tests/test_chapter_37.py` through `tests/test_chapter_41.py` — locked metadata, proof, orientation, boundary, training, and publication contracts.
- `src/mathbook_examples/vector_analysis.py` — the only midpoint line-integral and parametric-flux implementation.
- `tests/test_vector_analysis.py` — numerical behavior, orientation reversal, and failure semantics.
- `tests/test_part_09_consistency.py` — dependency, totals, scope, navigation, appendix, and unique-source contracts.
- `docs/reviews/2026-07-31-chapter-37-consistency-review.md` through `docs/reviews/2026-07-31-chapter-41-consistency-review.md`.
- `docs/reviews/2026-07-31-part-09-consistency-review.md`.

### Modify

- `mkdocs.yml` — publish only the chapter or appendix reached by the current checkpoint.
- `content/course-map.md` — add the blueprint, then advance chapter status one checkpoint at a time.
- `README.md` — advance publication boundary, unit count, and hours only after each green checkpoint.
- `tests/test_mkdocs_site.py` — register representative pages, anchors, code, and navigation markers.
- `tests/test_zensical_structure.py` — admit Part IX navigation only when Chapter 37 is published.
- `src/mathbook_examples/__init__.py` — remain a package marker; do not re-export the new API.

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

Every direction-sensitive unit must include an `### 取向检查` subsection that
records parameter direction, chosen normal, induced boundary direction, or the
relevant right-hand rule. Computational material additionally uses:

```markdown
### 问题来源
### 数学转化
### 算法思想
### 误差与适用条件
### 伪代码
### Python
### 结果解释
```

No core page may use general manifolds, homology, weak derivatives,
distributional divergence or curl, measure-theoretic surface integration,
parameter-dependent integration theorems, or numerical agreement as proof.

## Task 1: Lock the Part IX blueprint

**Files:**
- Create: `docs/curriculum/part-09-dependencies.md`
- Create: `tests/test_part_09_consistency.py`
- Modify: `content/course-map.md`

- [ ] **Step 1: Write the failing blueprint test**

Create `tests/test_part_09_consistency.py` with all 21 `(unit_id, theory,
applied)` rows and these initial assertions:

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs/curriculum/part-09-dependencies.md"
COURSE_MAP = ROOT / "content/course-map.md"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")


class Part09ConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.exists(), f"missing {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8")

    def test_locked_part_totals(self):
        units = PART_09_UNITS
        theory = sum(unit[1] for unit in units)
        applied = sum(unit[2] for unit in units)
        self.assertEqual(
            (21, 24.0, 8.0, 32.0),
            (len(units), theory, applied, theory + applied),
        )

    def test_blueprint_starts_after_part_eight(self):
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 36 章", text)
        self.assertIn("21 个核心单元、32 学时", text)
        self.assertNotIn("chapters/chapter-37/", NAVIGATION)

    def test_appendix_is_not_a_core_prerequisite(self):
        text = self.required_text(DEPENDENCIES)
        self.assertIn("选读附录不计入核心学时", text)
        for line in text.splitlines():
            if line.startswith("| `u-09-"):
                self.assertNotIn("微分形式", line)
```

- [ ] **Step 2: Run the test and verify the dependency map is missing**

Run: `python3.12 -m unittest tests.test_part_09_consistency -v`

Expected: FAIL because `docs/curriculum/part-09-dependencies.md` is absent.

- [ ] **Step 3: Write the dependency map and planned course map**

Create one row for every locked unit. Record direct prerequisites, unique
output, chapter totals, the classical proof order, the mandatory orientation
check, and these exclusions: no general manifolds, no weak vector calculus, no
measure-theoretic line or surface integration, and no numerical theorem proof.
Add Chapters 37–41 and the optional appendix to `content/course-map.md` as
“规划中”. Do not create content pages or navigation.

- [ ] **Step 4: Run the focused and baseline gates**

Run:

```bash
python3.12 -m unittest tests.test_part_09_consistency -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: all commands exit 0; the published site still stops at Chapter 36.

- [ ] **Step 5: Commit the blueprint**

```bash
git add docs/curriculum/part-09-dependencies.md content/course-map.md tests/test_part_09_consistency.py
git commit -m "docs: lock part 09 curriculum blueprint"
```

## Task 2: Publish Chapter 37

**Files:**
- Create: `content/chapters/chapter-37/index.md`
- Create: `content/chapters/chapter-37/u-09-37-01-regular-parametric-curves.md`
- Create: `content/chapters/chapter-37/u-09-37-02-arc-length-scalar-line-integral.md`
- Create: `content/chapters/chapter-37/u-09-37-03-work-circulation.md`
- Create: `content/chapters/chapter-37/u-09-37-04-reparameterization-conservative-fields.md`
- Create: `tests/test_chapter_37.py`
- Create: `docs/reviews/2026-07-31-chapter-37-consistency-review.md`
- Modify: `docs/curriculum/part-09-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`
- Modify: `tests/test_zensical_structure.py`

- [ ] **Step 1: Write the failing Chapter 37 contract**

Copy the four Chapter 37 registry rows into `tests/test_chapter_37.py`. Reuse
the metadata, guide-link, exercise, answer, and `content_standard` checks from
`tests/test_chapter_36.py`. Lock these markers and anchors:

```python
REQUIRED_MARKERS = {
    "u-09-37-01": ("分段光滑", "正则", "切向量", "方向"),
    "u-09-37-02": ("弧长", "第一类曲线积分", "参数分割", "重新参数化"),
    "u-09-37-03": ("第二类曲线积分", "功", "环流", "取向检查"),
    "u-09-37-04": ("保向", "反向", "势函数", "路径无关"),
}

REQUIRED_ANCHORS = {
    "u-09-37-01": ("def-u-09-37-01-regular-curve",),
    "u-09-37-02": ("def-u-09-37-02-scalar-line-integral",),
    "u-09-37-03": ("def-u-09-37-03-vector-line-integral",),
    "u-09-37-04": ("thm-u-09-37-04-reparameterization",),
}
```

- [ ] **Step 2: Run the contract and verify it fails**

Run: `python3.12 -m unittest tests.test_chapter_37 -v`

Expected: FAIL because `content/chapters/chapter-37/` is absent.

- [ ] **Step 3: Write 37.1 and 37.2**

In 37.1, distinguish a curve image from a parameterization, define piecewise
smooth and regular curves, and treat endpoints and corners explicitly. In 37.2,
derive arc length from polygonal sums and define the scalar line integral from
local density times arc length. Prove invariance under admissible monotone
reparameterization and state exactly where regularity is used.

- [ ] **Step 4: Write 37.3 and 37.4**

In 37.3, define the vector line integral as
`integral F(r(t)) dot r'(t) dt`, distinguish work and circulation, and add
direction and unit checks. In 37.4, prove invariance under orientation-preserving
reparameterization and sign reversal under orientation reversal. Establish the
potential theorem and its path-independence converse on a connected domain;
defer Green-based planar closed-loop criteria to Chapter 39.

- [ ] **Step 5: Publish and review Chapter 37**

Create the guide, add only Chapter 37 to navigation, advance the course map and
README from Chapter 36 to Chapter 37, update the dependency map, and write the
review with evidence for parameterization invariance, reversal signs, proof
assumptions, counts, and no Chapter 38 placeholder.

- [ ] **Step 6: Run the checkpoint gates**

Run:

```bash
python3.12 -m unittest tests.test_chapter_37 tests.test_part_09_consistency tests.test_zensical_structure -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: all pass; navigation ends at Chapter 37.

- [ ] **Step 7: Commit Chapter 37**

```bash
git add content/chapters/chapter-37 docs/curriculum/part-09-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_37.py tests/test_zensical_structure.py docs/reviews/2026-07-31-chapter-37-consistency-review.md
git commit -m "docs: publish chapter 37 curve integrals"
```

## Task 3: Publish Chapter 38

**Files:**
- Create: `content/chapters/chapter-38/index.md`
- Create: `content/chapters/chapter-38/u-09-38-01-regular-parametric-surfaces.md`
- Create: `content/chapters/chapter-38/u-09-38-02-surface-area-element.md`
- Create: `content/chapters/chapter-38/u-09-38-03-scalar-surface-integral.md`
- Create: `content/chapters/chapter-38/u-09-38-04-flux-integral.md`
- Create: `tests/test_chapter_38.py`
- Create: `docs/reviews/2026-07-31-chapter-38-consistency-review.md`
- Modify: `docs/curriculum/part-09-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`

- [ ] **Step 1: Write the failing Chapter 38 contract**

Lock the four registry rows and these markers and anchors:

```python
REQUIRED_MARKERS = {
    "u-09-38-01": ("正则参数曲面", "切平面", "法向量", "取向检查"),
    "u-09-38-02": ("叉积", "局部线性化", "面积元", "重新参数化"),
    "u-09-38-03": ("第一类曲面积分", "曲面密度", "薄膜质量", "无向"),
    "u-09-38-04": ("通量", "有向面积元", "取向反转", "图形曲面"),
}

REQUIRED_ANCHORS = {
    "u-09-38-01": ("def-u-09-38-01-regular-surface",),
    "u-09-38-02": ("thm-u-09-38-02-area-element",),
    "u-09-38-03": ("def-u-09-38-03-scalar-surface-integral",),
    "u-09-38-04": ("def-u-09-38-04-flux-integral",),
}
```

- [ ] **Step 2: Run the contract and verify it fails**

Run: `python3.12 -m unittest tests.test_chapter_38 -v`

Expected: FAIL because `content/chapters/chapter-38/` is absent.

- [ ] **Step 3: Write 38.1 and 38.2**

Start with graph surfaces, then define regular parameterized surfaces using
linear independence of `r_u` and `r_v`. Separate local normals from a global
orientation. Derive `||r_u cross r_v|| du dv` from the derivative's local
parallelogram scaling and Chapter 35 change of variables; do not merely state
the formula.

- [ ] **Step 4: Write 38.3 and 38.4**

Define scalar surface integrals and oriented flux integrals. Prove the relevant
invariance under admissible parameter changes and show sign reversal when the
normal is reversed. Include graph, sphere, and piecewise surface examples with
explicit parameter ranges and normals. Keep implicit surfaces at the level of
constructing a local normal from a nonzero gradient.

- [ ] **Step 5: Publish, review, test, and commit Chapter 38**

Update only the Chapter 38 publication surfaces and review. Run:

```bash
python3.12 -m unittest tests.test_chapter_38 tests.test_part_09_consistency tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: all pass; navigation ends at Chapter 38. Then commit:

```bash
git add content/chapters/chapter-38 docs/curriculum/part-09-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_38.py tests/test_mkdocs_site.py docs/reviews/2026-07-31-chapter-38-consistency-review.md
git commit -m "docs: publish chapter 38 surface integrals"
```

## Task 4: Publish Chapter 39

**Files:**
- Create: `content/chapters/chapter-39/index.md`
- Create: `content/chapters/chapter-39/u-09-39-01-planar-divergence-curl.md`
- Create: `content/chapters/chapter-39/u-09-39-02-green-theorem.md`
- Create: `content/chapters/chapter-39/u-09-39-03-multiply-connected-green.md`
- Create: `content/chapters/chapter-39/u-09-39-04-green-applications.md`
- Create: `tests/test_chapter_39.py`
- Create: `docs/reviews/2026-07-31-chapter-39-consistency-review.md`
- Modify: `docs/curriculum/part-09-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Write and run the failing Chapter 39 contract**

Lock these markers and anchors, then run
`python3.12 -m unittest tests.test_chapter_39 -v` and expect missing pages:

```python
REQUIRED_MARKERS = {
    "u-09-39-01": ("平面散度", "标量旋度", "局部环流", "局部通量"),
    "u-09-39-02": ("Green 公式", "微积分基本定理", "简单区域", "内部边界抵消"),
    "u-09-39-03": ("多连通", "外边界", "内边界", "取向检查"),
    "u-09-39-04": ("面积公式", "路径无关", "环流", "不可压缩"),
}

REQUIRED_ANCHORS = {
    "u-09-39-01": ("def-u-09-39-01-planar-div-curl",),
    "u-09-39-02": ("thm-u-09-39-02-green",),
    "u-09-39-03": ("thm-u-09-39-03-multiply-connected-green",),
    "u-09-39-04": ("thm-u-09-39-04-path-independence",),
}
```

- [ ] **Step 2: Write the local operators and complete Green proof**

Derive planar divergence and scalar curl from small rectangles. Prove Green's
tangential form first for a region that is simple in both coordinate directions
by applying the one-dimensional fundamental theorem to each term. Extend by
finite subdivision and make the cancellation orientation explicit. Derive the
normal form from the tangential form rather than silently changing notation.

- [ ] **Step 3: Write topology-sensitive cases and applications**

Treat outer boundaries counterclockwise and hole boundaries clockwise. Show
why curl-free does not imply a global potential on a punctured domain without
additional hypotheses. Include area, circulation, flux, path independence, and
two-dimensional incompressible-flow applications after the proof.

- [ ] **Step 4: Publish, review, test, and commit Chapter 39**

Run:

```bash
python3.12 -m unittest tests.test_chapter_39 tests.test_part_09_consistency tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: all pass; navigation ends at Chapter 39. Then commit:

```bash
git add content/chapters/chapter-39 docs/curriculum/part-09-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_39.py tests/test_mkdocs_site.py docs/reviews/2026-07-31-chapter-39-consistency-review.md
git commit -m "docs: publish chapter 39 Green theorem"
```

## Task 5: Publish Chapter 40

**Files:**
- Create: `content/chapters/chapter-40/index.md`
- Create: `content/chapters/chapter-40/u-09-40-01-spatial-divergence.md`
- Create: `content/chapters/chapter-40/u-09-40-02-gauss-box.md`
- Create: `content/chapters/chapter-40/u-09-40-03-gauss-piecewise-regions.md`
- Create: `content/chapters/chapter-40/u-09-40-04-gauss-applications-singularities.md`
- Create: `tests/test_chapter_40.py`
- Create: `docs/reviews/2026-07-31-chapter-40-consistency-review.md`
- Modify: `docs/curriculum/part-09-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Write and run the failing Chapter 40 contract**

Lock these markers and anchors, then run
`python3.12 -m unittest tests.test_chapter_40 -v` and expect missing pages:

```python
REQUIRED_MARKERS = {
    "u-09-40-01": ("三维散度", "源汇", "净流出", "小长方体"),
    "u-09-40-02": ("Gauss 公式", "长方体", "外法向", "微积分基本定理"),
    "u-09-40-03": ("分片光滑", "内部通量抵消", "规则区域", "取向检查"),
    "u-09-40-04": ("不可压缩", "电通量", "奇点", "挖孔"),
}

REQUIRED_ANCHORS = {
    "u-09-40-01": ("def-u-09-40-01-divergence",),
    "u-09-40-02": ("thm-u-09-40-02-gauss-box",),
    "u-09-40-03": ("thm-u-09-40-03-gauss",),
    "u-09-40-04": ("ex-u-09-40-04-punctured-flux",),
}
```

- [ ] **Step 2: Write the divergence and box proof**

Obtain divergence from the first-order net-flux balance on a small rectangular
box. Prove Gauss on a box by applying the one-dimensional fundamental theorem
to each coordinate component, matching each endpoint term to the correct
outward face normal.

- [ ] **Step 3: Write the finite-subdivision extension and applications**

State the exact class of bounded piecewise smooth regions used in the text.
Explain why shared faces carry opposite outward normals and cancel. For singular
fields, remove a small neighborhood, apply Gauss only on the regular punctured
region, account for the new inner boundary, and then justify the limit. Keep
electromagnetic and fluid interpretations as models rather than new theories.

- [ ] **Step 4: Publish, review, test, and commit Chapter 40**

Run:

```bash
python3.12 -m unittest tests.test_chapter_40 tests.test_part_09_consistency tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: all pass; navigation ends at Chapter 40. Then commit:

```bash
git add content/chapters/chapter-40 docs/curriculum/part-09-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_40.py tests/test_mkdocs_site.py docs/reviews/2026-07-31-chapter-40-consistency-review.md
git commit -m "docs: publish chapter 40 Gauss theorem"
```

## Task 6: Implement the non-certifying oriented midpoint checks

**Files:**
- Create: `src/mathbook_examples/vector_analysis.py`
- Create: `tests/test_vector_analysis.py`

- [ ] **Step 1: Write the failing numerical tests**

Create `tests/test_vector_analysis.py`:

```python
import math
import unittest

from src.mathbook_examples.vector_analysis import (
    composite_midpoint_flux_integral,
    composite_midpoint_line_integral,
)


class VectorAnalysisTests(unittest.TestCase):
    def test_line_integral_of_constant_field(self):
        result = composite_midpoint_line_integral(
            lambda point: (2.0, -1.0),
            curve=lambda t: (t, t * t),
            curve_derivative=lambda t: (1.0, 2.0 * t),
            bounds=(0.0, 1.0),
            n=8,
        )
        self.assertAlmostEqual(result.value, 1.0)
        self.assertEqual(result.evaluations, 8)

    def test_line_direction_reversal_changes_sign(self):
        forward = composite_midpoint_line_integral(
            lambda point: point,
            curve=lambda t: (t, 0.0),
            curve_derivative=lambda t: (1.0, 0.0),
            bounds=(0.0, 1.0),
            n=20,
        )
        reverse = composite_midpoint_line_integral(
            lambda point: point,
            curve=lambda t: (1.0 - t, 0.0),
            curve_derivative=lambda t: (-1.0, 0.0),
            bounds=(0.0, 1.0),
            n=20,
        )
        self.assertAlmostEqual(reverse.value, -forward.value)

    def test_flux_of_vertical_field_through_unit_square(self):
        result = composite_midpoint_flux_integral(
            lambda point: (0.0, 0.0, 3.0),
            surface=lambda u, v: (u, v, 0.0),
            surface_u=lambda u, v: (1.0, 0.0, 0.0),
            surface_v=lambda u, v: (0.0, 1.0, 0.0),
            u_bounds=(0.0, 1.0),
            v_bounds=(0.0, 1.0),
            nu=4,
            nv=5,
        )
        self.assertAlmostEqual(result.value, 3.0)
        self.assertEqual(result.evaluations, 20)

    def test_flux_orientation_reversal_changes_sign(self):
        forward = composite_midpoint_flux_integral(
            lambda point: (0.0, 0.0, 1.0),
            surface=lambda u, v: (u, v, 0.0),
            surface_u=lambda u, v: (1.0, 0.0, 0.0),
            surface_v=lambda u, v: (0.0, 1.0, 0.0),
            u_bounds=(0.0, 1.0), v_bounds=(0.0, 1.0), nu=2, nv=2,
        )
        reverse = composite_midpoint_flux_integral(
            lambda point: (0.0, 0.0, 1.0),
            surface=lambda u, v: (v, u, 0.0),
            surface_u=lambda u, v: (0.0, 1.0, 0.0),
            surface_v=lambda u, v: (1.0, 0.0, 0.0),
            u_bounds=(0.0, 1.0), v_bounds=(0.0, 1.0), nu=2, nv=2,
        )
        self.assertAlmostEqual(reverse.value, -forward.value)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "positive integer"):
            composite_midpoint_line_integral(
                lambda p: (1.0, 0.0), curve=lambda t: (t, 0.0),
                curve_derivative=lambda t: (1.0, 0.0), bounds=(0.0, 1.0), n=True,
            )
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            composite_midpoint_line_integral(
                lambda p: (1.0, 0.0), curve=lambda t: (t, 0.0),
                curve_derivative=lambda t: (1.0, 0.0), bounds=(1.0, 1.0), n=2,
            )
        with self.assertRaisesRegex(ValueError, "same dimension"):
            composite_midpoint_line_integral(
                lambda p: (1.0, 0.0, 0.0), curve=lambda t: (t, 0.0),
                curve_derivative=lambda t: (1.0, 0.0), bounds=(0.0, 1.0), n=2,
            )
        with self.assertRaisesRegex(ValueError, "nondegenerate normal"):
            composite_midpoint_flux_integral(
                lambda p: (0.0, 0.0, 1.0), surface=lambda u, v: (u, v, 0.0),
                surface_u=lambda u, v: (1.0, 0.0, 0.0),
                surface_v=lambda u, v: (2.0, 0.0, 0.0),
                u_bounds=(0.0, 1.0), v_bounds=(0.0, 1.0), nu=2, nv=2,
            )
        with self.assertRaisesRegex(ValueError, "finite"):
            composite_midpoint_line_integral(
                lambda p: (math.inf, 0.0), curve=lambda t: (t, 0.0),
                curve_derivative=lambda t: (1.0, 0.0), bounds=(0.0, 1.0), n=2,
            )
```

- [ ] **Step 2: Run the numerical tests and verify import failure**

Run: `python3.12 -m unittest tests.test_vector_analysis -v`

Expected: ERROR with `ModuleNotFoundError` for `vector_analysis`.

- [ ] **Step 3: Implement the minimal public API**

Create `src/mathbook_examples/vector_analysis.py` with frozen result records
`LineIntegralResult(value, bounds, n, evaluations)` and
`FluxIntegralResult(value, u_bounds, v_bounds, nu, nv, evaluations)`. Implement
these exact signatures:

```python
def composite_midpoint_line_integral(
    field,
    *,
    curve,
    curve_derivative,
    bounds: tuple[float, float],
    n: int,
) -> LineIntegralResult:
    """Approximate integral F(r(t)) dot r'(t) dt without certification."""


def composite_midpoint_flux_integral(
    field,
    *,
    surface,
    surface_u,
    surface_v,
    u_bounds: tuple[float, float],
    v_bounds: tuple[float, float],
    nu: int,
    nv: int,
) -> FluxIntegralResult:
    """Approximate integral F(r) dot (r_u cross r_v) du dv without certification."""
```

Reuse private validation patterns from `multiple_integration.py`. Convert vector
results to finite tuples, require line field and derivative dimensions to match
and be either 2 or 3, require all flux vectors to be three-dimensional, compute
dot and cross products locally, reject a zero sampled normal, and accumulate
with `math.fsum`. Do not estimate errors or infer regularity between samples.

- [ ] **Step 4: Run focused and regression tests**

Run:

```bash
python3.12 -m unittest tests.test_vector_analysis -v
python3.12 -m unittest tests.test_multiple_integration tests.test_multivariate -v
```

Expected: all pass.

- [ ] **Step 5: Commit the numerical source**

```bash
git add src/mathbook_examples/vector_analysis.py tests/test_vector_analysis.py
git commit -m "feat: add oriented midpoint integration checks"
```

## Task 7: Publish Chapter 41 and connect the numerical source

**Files:**
- Create: `content/chapters/chapter-41/index.md`
- Create: `content/chapters/chapter-41/u-09-41-01-spatial-curl.md`
- Create: `content/chapters/chapter-41/u-09-41-02-induced-boundary-orientation.md`
- Create: `content/chapters/chapter-41/u-09-41-03-stokes-parametric-patch.md`
- Create: `content/chapters/chapter-41/u-09-41-04-stokes-piecewise-surfaces.md`
- Create: `content/chapters/chapter-41/u-09-41-05-vector-theorem-selection.md`
- Create: `tests/test_chapter_41.py`
- Create: `docs/reviews/2026-07-31-chapter-41-consistency-review.md`
- Modify: `docs/curriculum/part-09-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Write and run the failing Chapter 41 contract**

Lock these markers and anchors, require 41.5 to import both functions from
`src.mathbook_examples.vector_analysis`, and run the test expecting missing
pages:

```python
REQUIRED_MARKERS = {
    "u-09-41-01": ("三维旋度", "局部环流密度", "右手规则", "取向检查"),
    "u-09-41-02": ("诱导边界方向", "曲面取向", "右手规则", "边界分支"),
    "u-09-41-03": ("Stokes 公式", "参数域", "Green 公式", "拉回计算"),
    "u-09-41-04": ("分片光滑曲面", "内部边界抵消", "相反方向", "拼接"),
    "u-09-41-05": ("Green", "Gauss", "Stokes", "数值结果不能证明"),
}

REQUIRED_ANCHORS = {
    "u-09-41-01": ("def-u-09-41-01-curl",),
    "u-09-41-02": ("def-u-09-41-02-induced-orientation",),
    "u-09-41-03": ("thm-u-09-41-03-stokes-patch",),
    "u-09-41-04": ("thm-u-09-41-04-stokes",),
    "u-09-41-05": ("workflow-u-09-41-05-selection",),
}
```

- [ ] **Step 2: Write 41.1 through 41.3**

Derive curl from circulation around coordinate rectangles. Define induced
boundary direction from a chosen surface normal and verify it on a graph patch.
For a single parameter patch, expand the boundary line integral in parameter
coordinates, apply Green on the parameter domain, and identify the result with
`curl F dot (r_u cross r_v)`; state where regularity and orientation enter.

- [ ] **Step 3: Write 41.4 and 41.5**

Extend Stokes by a finite compatible patch decomposition and explicit internal
boundary cancellation. In 41.5, provide a decision workflow based on integration
object, boundary dimension, differential operator, regularity, and orientation.
Import both midpoint functions for one line-integral and one flux cross-check;
state that sampling does not certify the theorem or its assumptions.

- [ ] **Step 4: Publish, review, test, and commit Chapter 41**

Run:

```bash
python3.12 -m unittest tests.test_chapter_41 tests.test_vector_analysis tests.test_part_09_consistency tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: all pass; core navigation ends at Chapter 41. Then commit:

```bash
git add content/chapters/chapter-41 docs/curriculum/part-09-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_41.py tests/test_mkdocs_site.py docs/reviews/2026-07-31-chapter-41-consistency-review.md
git commit -m "docs: publish chapter 41 Stokes unification"
```

## Task 8: Publish the optional differential-forms appendix

**Files:**
- Create: `content/appendices/part-09-differential-forms.md`
- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `docs/curriculum/part-09-dependencies.md`
- Modify: `tests/test_part_09_consistency.py`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Extend the appendix contract and verify failure**

Add assertions requiring one appendix navigation entry, no `hours:` metadata,
no appendix name in any core prerequisite row, and these exact conceptual
markers:

```python
APPENDIX_MARKERS = (
    "0-形式", "1-形式", "2-形式", "3-形式", "外微分", "拉回",
    "广义 Stokes", "不证明一般流形上的广义 Stokes 定理",
)
```

Run: `python3.12 -m unittest tests.test_part_09_consistency -v`

Expected: FAIL because the appendix is absent.

- [ ] **Step 2: Write the appendix**

Map scalar functions and classical vector-calculus integrands to concrete
forms in Euclidean coordinates. Explain external differentiation and pullback
only through examples already supported by Chapters 37–41. Include a compact
Green/Gauss/Stokes comparison table and the generalized Stokes slogan. Exclude
general manifolds, tangent bundles, cohomology, a complete exterior-algebra
development, and a general proof.

- [ ] **Step 3: Publish, test, and commit the appendix**

Run:

```bash
python3.12 -m unittest tests.test_part_09_consistency tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: all pass; the appendix is visible once and core totals stay 21 units
and 32 hours. Then commit:

```bash
git add content/appendices/part-09-differential-forms.md mkdocs.yml content/course-map.md docs/curriculum/part-09-dependencies.md tests/test_part_09_consistency.py tests/test_mkdocs_site.py
git commit -m "docs: add optional differential forms appendix"
```

## Task 9: Close the Part IX consistency audit

**Files:**
- Create: `docs/reviews/2026-07-31-part-09-consistency-review.md`
- Modify: `tests/test_part_09_consistency.py`
- Modify: `tests/test_mkdocs_site.py`
- Modify: `README.md`
- Modify: `content/course-map.md`
- Modify: `docs/curriculum/part-09-dependencies.md`

- [ ] **Step 1: Strengthen the final consistency contract**

Require exactly 21 Part IX unit pages, five guides, one appendix, 201 anchored
exercises, and 247 collapsed answers. Require the final publication boundary
to be Chapter 41; exact core totals of 24 theory plus 8 application hours;
exactly one textbook call site for each function in `vector_analysis.py`; all
five chapter reviews; and these stable historical milestones:

```python
README_TEXT = (ROOT / "README.md").read_text(encoding="utf-8")
textbook_text = "\n".join(
    path.read_text(encoding="utf-8")
    for path in (ROOT / "content/chapters").rglob("*.md")
)
self.assertIn("第八部已经完整发布", README_TEXT)
self.assertIn("第九部已经完整发布", README_TEXT)
self.assertNotIn("chapters/chapter-42/", NAVIGATION)
self.assertEqual(1, textbook_text.count("composite_midpoint_line_integral"))
self.assertEqual(1, textbook_text.count("composite_midpoint_flux_integral"))
```

- [ ] **Step 2: Run every focused Part IX test**

Run:

```bash
python3.12 -m unittest \
  tests.test_chapter_37 \
  tests.test_chapter_38 \
  tests.test_chapter_39 \
  tests.test_chapter_40 \
  tests.test_chapter_41 \
  tests.test_vector_analysis \
  tests.test_part_09_consistency \
  tests.test_mkdocs_site -v
```

Expected: all pass.

- [ ] **Step 3: Run the complete quality gate**

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

Serve the built site and inspect representative pages from 37.4, 38.2 or 38.4,
39.3, 40.4, 41.2 or 41.3, and the differential-forms comparison table. Record
viewport width, `scrollWidth`, one visible level-one heading, MathJax rendering,
code-block wrapping, folded answers, sidebar behavior, and the absence of
page-level horizontal scrolling. Fix any overflow before continuing.

- [ ] **Step 5: Write the final consistency review**

Record the final unit, hour, exercise, and answer totals; proof and orientation
coverage; numerical non-certificate semantics; appendix exclusion; all command
results; mobile evidence; and the fact that Chapter 42 has not been created.

- [ ] **Step 6: Commit the closed audit**

```bash
git add docs/reviews/2026-07-31-part-09-consistency-review.md tests/test_part_09_consistency.py tests/test_mkdocs_site.py README.md content/course-map.md docs/curriculum/part-09-dependencies.md
git commit -m "docs: close part 09 consistency audit"
```
