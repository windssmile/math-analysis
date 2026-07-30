# Chapter 21 Geometric and Physical Models Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Chapter 21 as five rigorous self-study units that derive one-variable geometric and physical integral models from local contributions and Riemann sums, then train mixed model selection in an independent capstone unit.

**Architecture:** Add one chapter guide and five `content_standard: 2` units under `content/chapters/chapter-21/`. Lock metadata, proof conditions, training density, publication statistics, and rendered anchors in failing tests first; implement the guide and each dependency-closed unit in separate green commits; publish only after all content contracts pass. Keep improper integration, numerical quadrature, parametric curves, surface area, fluid pressure, and multivariable calculus outside the chapter core.

**Tech Stack:** Markdown with YAML front matter, Python 3.12 `unittest`, Zensical strict build, existing content/site validators, Git worktree workflow.

---

## File map

**Create**

- `content/chapters/chapter-21/index.md` — chapter guide, model-building route, dependencies, and Chapter 22 boundary.
- `content/chapters/chapter-21/u-05-21-01-area-models.md` — Riemann area, signed/geometric area, and area between curves.
- `content/chapters/chapter-21/u-05-21-02-volume-models.md` — cross sections, disks/washers, and rigorous shell remainder control.
- `content/chapters/chapter-21/u-05-21-03-arc-length.md` — polygonal length, refinement monotonicity, and the \(C^1\) graph arc-length theorem.
- `content/chapters/chapter-21/u-05-21-04-work-mass-average.md` — variable work, line-density mass, average value, and units.
- `content/chapters/chapter-21/u-05-21-05-modeling-practice.md` — mixed model selection, piecewise setup, diagnosis, and verification.
- `tests/test_chapter_21.py` — all chapter content, boundary, count, dependency, and publication contracts.
- `docs/reviews/2026-07-30-chapter-21-consistency-review.md` — final proof and publication audit.

**Modify**

- `docs/curriculum/part-05-dependencies.md` — add Unit 21.5, change 23 units to 24, preserve 40.5 hours, and advance the boundary.
- `mkdocs.yml` — add the Chapter 21 guide and five units after Chapter 20.
- `content/course-map.md` — add Chapter 21 hours and links; update release count to 92.
- `README.md` — update release scope to Chapter 21 and 92 units.
- `scripts/check_site.py` — require representative Chapter 21 anchors and navigation.
- `tests/test_mkdocs_site.py` — lock the Chapter 21 rendered-site dictionaries.
- `tests/test_chapter_15.py`, `tests/test_chapter_16.py`, `tests/test_chapter_17.py`, `tests/test_chapter_18.py`, `tests/test_chapter_19.py`, `tests/test_chapter_20.py`, `tests/test_part_04_consistency.py`, `tests/test_zensical_structure.py` — update only stale global release assertions.

## Locked unit contract

| Unit | Title | Theory | Applied | Exercises | Answers |
|---|---|---:|---:|---:|---:|
| `u-05-21-01` | 面积怎样从局部条带与有向积分产生？ | 1.00 | 0.25 | 6 | 8 |
| `u-05-21-02` | 截面怎样重建立体体积？ | 1.00 | 0.50 | 8 | 10 |
| `u-05-21-03` | 折线长度怎样逼近光滑图像的弧长？ | 1.00 | 0.25 | 6 | 8 |
| `u-05-21-04` | 功、质量与平均值怎样选择局部贡献？ | 0.75 | 0.50 | 6 | 8 |
| `u-05-21-05` | 几何与物理综合建模怎样选变量并回验？ | 0.25 | 1.50 | 12 | 16 |

Chapter total: theory 4, applied 3, total 7; 38 anchored exercises and 50 collapsed answers.

### Task 1: Lock Chapter 21 contracts in failing tests

**Files:**

- Create: `tests/test_chapter_21.py`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Write the chapter contract test**

Create a complete `unittest` module with this locked data:

```python
EXPECTED_UNITS = [
    ("u-05-21-01", "面积怎样从局部条带与有向积分产生？",
     1.00, 0.25, "area-models", 6, 8),
    ("u-05-21-02", "截面怎样重建立体体积？",
     1.00, 0.50, "volume-models", 8, 10),
    ("u-05-21-03", "折线长度怎样逼近光滑图像的弧长？",
     1.00, 0.25, "arc-length", 6, 8),
    ("u-05-21-04", "功、质量与平均值怎样选择局部贡献？",
     0.75, 0.50, "work-mass-average", 6, 8),
    ("u-05-21-05", "几何与物理综合建模怎样选变量并回验？",
     0.25, 1.50, "modeling-practice", 12, 16),
]

REQUIRED_ANCHORS = {
    "u-05-21-01": (
        "def-u-05-21-01-riemann-area",
        "thm-u-05-21-01-area-between-curves",
        "ex-u-05-21-01-signed-vs-geometric",
    ),
    "u-05-21-02": (
        "thm-u-05-21-02-cross-section-volume",
        "thm-u-05-21-02-washer-volume",
        "lem-u-05-21-02-shell-remainder",
        "thm-u-05-21-02-shell-volume",
    ),
    "u-05-21-03": (
        "def-u-05-21-03-polygonal-length",
        "def-u-05-21-03-graph-arc-length",
        "lem-u-05-21-03-refinement-monotonicity",
        "thm-u-05-21-03-c1-graph-arc-length",
    ),
    "u-05-21-04": (
        "thm-u-05-21-04-variable-force-work",
        "thm-u-05-21-04-linear-density-mass",
        "def-u-05-21-04-average-value",
        "tbl-u-05-21-04-unit-check",
    ),
    "u-05-21-05": (
        "alg-u-05-21-05-modeling-workflow",
        "tbl-u-05-21-05-model-selection",
        "ex-u-05-21-05-cross-model",
        "ex-u-05-21-05-error-diagnosis",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "反常积分",
    "数值求积",
    "Simpson",
    "参数曲线",
    "曲面面积",
    "流体压力",
    "多重积分",
    "Lebesgue",
)
```

Implement tests that:

```python
self.assertEqual(4.0, theory)
self.assertEqual(3.0, applied)
self.assertEqual(38, total_exercises)
self.assertEqual(50, total_answers)
self.assertIn("本章共5个核心单元，7学时（理论4，应用3）。", guide)
self.assertGreaterEqual(unit_five.count("{#pr-u-05-21-05-mixed-"), 4)
self.assertGreaterEqual(unit_five.count("{#pr-u-05-21-05-diagnosis-"), 3)
self.assertGreaterEqual(unit_five.count("{#pr-u-05-21-05-boundary-"), 2)
self.assertIn("24 个核心单元", dependencies)
self.assertIn("当前发布边界：第 21 章", dependencies)
self.assertIn("第五部第 21 章，共 92 个学习单元", readme)
```

Also require the mathematical markers from the design:

```python
AREA_MARKERS = ("Riemann 面积", "有向积分", "几何面积", "上减下",
                "右减左", "换号点")
VOLUME_MARKERS = ("截面面积", "圆盘", "垫片", "柱壳", "一致连续",
                  "二次余项", "网格")
ARC_MARKERS = ("内接折线", "上确界", "分割加细", "Lagrange 中值定理",
               "一致连续", "公共加细")
PHYSICS_MARKERS = ("局部功", "有向功", "线密度", "非负",
                   "平均值", "单位")
```

- [ ] **Step 2: Add rendered-site test expectations**

Extend `tests/test_mkdocs_site.py` with:

```python
def test_checks_chapter_twenty_one_volume_page(self) -> None:
    self.assertEqual(
        [
            "lem-u-05-21-02-shell-remainder",
            "thm-u-05-21-02-shell-volume",
        ],
        check_site.REQUIRED_RENDERED_ANCHORS[
            "chapters/chapter-21/u-05-21-02-volume-models/index.html"
        ],
    )

def test_checks_chapter_twenty_one_arc_length_page(self) -> None:
    self.assertEqual(
        [
            "def-u-05-21-03-graph-arc-length",
            "thm-u-05-21-03-c1-graph-arc-length",
        ],
        check_site.REQUIRED_RENDERED_ANCHORS[
            "chapters/chapter-21/u-05-21-03-arc-length/index.html"
        ],
    )

def test_checks_chapter_twenty_one_practice_page(self) -> None:
    self.assertEqual(
        [
            "alg-u-05-21-05-modeling-workflow",
            "tbl-u-05-21-05-model-selection",
        ],
        check_site.REQUIRED_RENDERED_ANCHORS[
            "chapters/chapter-21/u-05-21-05-modeling-practice/index.html"
        ],
    )
```

- [ ] **Step 3: Verify RED**

Run:

```bash
python3.12 -m unittest tests.test_chapter_21 tests.test_mkdocs_site -v
```

Expected: Chapter 21 content tests fail because the guide/pages do not exist; rendered-site tests error because the dictionaries do not contain Chapter 21 paths.

- [ ] **Step 4: Commit the failing contract**

```bash
git add tests/test_chapter_21.py tests/test_mkdocs_site.py
git commit -m "test: lock chapter 21 modeling contract"
```

### Task 2: Establish the chapter guide

**Files:**

- Create: `content/chapters/chapter-21/index.md`

- [ ] **Step 1: Write the guide**

Use:

```yaml
---
title: 第 21 章：积分的几何与物理模型
---
```

The body must contain exactly one link to each unit, the 4+3=7 hour budget, the model-building chain, Chapter 19/20 inputs, explicit distinctions among signed quantity/geometric quantity/formula computation, and the Chapter 22 stop boundary.

- [ ] **Step 2: Run the guide contract**

```bash
python3.12 -m unittest \
  tests.test_chapter_21.ChapterTwentyOneTests.test_chapter_guide_lists_units_hours_route_and_boundaries -v
python3.12 scripts/check_content.py
```

Expected: both pass; other Chapter 21 tests remain red because unit pages are absent.

- [ ] **Step 3: Commit**

```bash
git add content/chapters/chapter-21/index.md
git commit -m "docs: establish chapter 21 modeling route"
```

### Task 3: Write Unit 21.1 area models

**Files:**

- Create: `content/chapters/chapter-21/u-05-21-01-area-models.md`

- [ ] **Step 1: Add front matter**

```yaml
---
title: 面积怎样从局部条带与有向积分产生？
unit_id: u-05-21-01
part: 5
chapter: 21
section: 1
prerequisites:
  - u-05-19-02
  - u-05-19-04
  - u-05-20-03
hours:
  theory: 1.0
  applied: 0.25
difficulty: core
content_standard: 2
---
```

- [ ] **Step 2: Write the proof core**

Include the three stable anchors and these exact formulas:

```latex
S(f;P,\xi)=\sum_{i=1}^{n}f(\xi_i)\Delta x_i
A_{\mathrm{geom}}=\int_a^b |f(x)|\,dx
A=\int_a^b(f(x)-g(x))\,dx
```

Prove the Riemann-area origin for nonnegative continuous functions, then separate signed integral from geometric area and require splitting at sign/order changes.

- [ ] **Step 3: Add self-study material**

Add at least two complete examples, two immediate checks, six anchored exercises, and eight collapsed answers. Include one vertical-versus-horizontal setup and one error diagnosis, but leave extended selection practice for Unit 21.5.

- [ ] **Step 4: Verify and commit**

```bash
python3.12 -m unittest tests.test_chapter_21 -v
python3.12 scripts/check_content.py
git diff --check
git add content/chapters/chapter-21/u-05-21-01-area-models.md
git commit -m "docs: derive area models from local strips"
```

Expected: Unit 21.1 and content validation pass; tests for Units 21.2–21.5 and publication remain red.

### Task 4: Write Unit 21.2 volume models

**Files:**

- Create: `content/chapters/chapter-21/u-05-21-02-volume-models.md`

- [ ] **Step 1: Add front matter**

```yaml
---
title: 截面怎样重建立体体积？
unit_id: u-05-21-02
part: 5
chapter: 21
section: 2
prerequisites:
  - u-05-21-01
  - u-05-19-04
hours:
  theory: 1.0
  applied: 0.5
difficulty: core
content_standard: 2
---
```

- [ ] **Step 2: Derive cross sections, disks, and washers**

Use:

```latex
V=\lim_{\lVert P\rVert\to0}\sum_i A(\xi_i)\Delta x_i
 =\int_a^b A(x)\,dx
A(x)=\pi R(x)^2
A(x)=\pi\bigl(R(x)^2-r(x)^2\bigr)
```

State continuity/integrability and radius-order conditions.

- [ ] **Step 3: Prove the shell remainder**

For continuous height \(h\ge0\), compare upper/lower heights on each radial subinterval and expand:

```latex
\pi\bigl((r_i+\Delta r_i)^2-r_i^2\bigr)h_i
=2\pi r_i h_i\Delta r_i+\pi h_i(\Delta r_i)^2.
```

Bound the height-oscillation contribution with the modulus of continuity and the quadratic remainder by:

```latex
\sum_i \pi M(\Delta r_i)^2
\le \pi M\lVert P\rVert(b-a)\to0.
```

Then obtain:

```latex
V=2\pi\int_a^b r\,h(r)\,dr.
```

- [ ] **Step 4: Add training, verify, and commit**

Add at least three complete examples, two immediate checks, eight anchored exercises, and ten collapsed answers, including one washer/shell comparison and one axis/radius diagnosis.

```bash
python3.12 -m unittest tests.test_chapter_21 -v
python3.12 scripts/check_content.py
git diff --check
git add content/chapters/chapter-21/u-05-21-02-volume-models.md
git commit -m "docs: derive cross section and shell volume"
```

### Task 5: Write Unit 21.3 arc length

**Files:**

- Create: `content/chapters/chapter-21/u-05-21-03-arc-length.md`

- [ ] **Step 1: Add front matter**

```yaml
---
title: 折线长度怎样逼近光滑图像的弧长？
unit_id: u-05-21-03
part: 5
chapter: 21
section: 3
prerequisites:
  - u-04-14-02
  - u-04-15-01
  - u-05-19-03
  - u-05-20-03
hours:
  theory: 1.0
  applied: 0.25
difficulty: advanced
content_standard: 2
---
```

- [ ] **Step 2: Define polygonal and graph length**

Use the stable anchors and:

```latex
L(f,P)=\sum_{i=1}^{n}
\sqrt{(x_i-x_{i-1})^2+(f(x_i)-f(x_{i-1}))^2}
```

Define graph length as the supremum of these quantities and prove refinement monotonicity by the triangle inequality.

- [ ] **Step 3: Prove the \(C^1\) theorem**

For each interval, use Lagrange MVT:

```latex
\frac{f(x_i)-f(x_{i-1})}{x_i-x_{i-1}}=f'(\xi_i).
```

Show fine polygonal lengths are tagged Riemann sums for
\(g(x)=\sqrt{1+[f'(x)]^2}\). For an arbitrary fixed partition \(Q\), take fine common refinements \(P_n\supset Q\); use
\(L(f,Q)\le L(f,P_n)\to\int g\) and a fine sequence with lengths converging to the same integral to prove:

```latex
L=\int_a^b\sqrt{1+[f'(x)]^2}\,dx.
```

- [ ] **Step 4: Add training, verify, and commit**

Add two complete examples, two immediate checks, six anchored exercises, and eight collapsed answers. Include \(L\ge b-a\), a line check, a non-\(C^1\) boundary discussion, and an explicit warning that the vector mean-value theorem was not used.

```bash
python3.12 -m unittest tests.test_chapter_21 -v
python3.12 scripts/check_content.py
git diff --check
git add content/chapters/chapter-21/u-05-21-03-arc-length.md
git commit -m "docs: prove the c1 graph arc length formula"
```

### Task 6: Write Unit 21.4 work, mass, and average value

**Files:**

- Create: `content/chapters/chapter-21/u-05-21-04-work-mass-average.md`

- [ ] **Step 1: Add front matter**

```yaml
---
title: 功、质量与平均值怎样选择局部贡献？
unit_id: u-05-21-04
part: 5
chapter: 21
section: 4
prerequisites:
  - u-05-19-04
  - u-05-20-03
hours:
  theory: 0.75
  applied: 0.5
difficulty: core
content_standard: 2
---
```

- [ ] **Step 2: Derive all three models**

Use:

```latex
W=\int_a^b F(x)\,dx
m=\int_a^b\rho(x)\,dx,\qquad \rho(x)\ge0
f_{\mathrm{avg}}=\frac{1}{b-a}\int_a^b f(x)\,dx
```

Start each formula from its Riemann sum and define the unit contract: force times displacement, mass-per-length times length, and accumulated quantity divided by length. Preserve signed work.

- [ ] **Step 3: Add training, verify, and commit**

Add three complete examples, two immediate checks, six anchored exercises, and eight collapsed answers. Include a spring, a finite-interval pumping-work setup, a piecewise density, a unit diagnosis, and a counterexample to endpoint averaging.

```bash
python3.12 -m unittest tests.test_chapter_21 -v
python3.12 scripts/check_content.py
git diff --check
git add content/chapters/chapter-21/u-05-21-04-work-mass-average.md
git commit -m "docs: derive work mass and average models"
```

### Task 7: Write Unit 21.5 mixed modeling practice

**Files:**

- Create: `content/chapters/chapter-21/u-05-21-05-modeling-practice.md`

- [ ] **Step 1: Add front matter**

```yaml
---
title: 几何与物理综合建模怎样选变量并回验？
unit_id: u-05-21-05
part: 5
chapter: 21
section: 5
prerequisites:
  - u-05-21-01
  - u-05-21-02
  - u-05-21-03
  - u-05-21-04
  - u-05-20-05
hours:
  theory: 0.25
  applied: 1.5
difficulty: advanced
content_standard: 2
---
```

- [ ] **Step 2: Add the workflow and selection table**

Anchor this workflow:

```text
识别所求量 → 选择积分变量 → 写局部贡献 → 确定区间与分段
→ 计算 → 单位、符号、界与数量级回验
```

The selection table must compare local contribution, variable, interval, required splitting, and fastest independent check without presenting a formula-only lookup sheet.

- [ ] **Step 3: Add examples and locked exercise bank**

Add at least four complete cross-model examples and four immediate checks. Add exactly twelve anchored exercises:

```text
mixed-01 ... mixed-04
diagnosis-01 ... diagnosis-03
boundary-01 ... boundary-02
verification-01 ... verification-03
```

Add sixteen collapsed answers. Cover vertical/horizontal area, washer/shell volume, piecewise setup, variable force/density, arc-length lower bound, sign/unit checks, and integral-bound verification. Do not group the exercises by model.

- [ ] **Step 4: Verify all content contracts and commit**

```bash
python3.12 -m unittest tests.test_chapter_21 -v
python3.12 scripts/check_content.py
git diff --check
git add content/chapters/chapter-21/u-05-21-05-modeling-practice.md
git commit -m "docs: add chapter 21 mixed modeling practice"
```

Expected: all content-only Chapter 21 tests pass; only publication assertions remain red.

### Task 8: Publish Chapter 21

**Files:**

- Modify: `README.md`
- Modify: `content/course-map.md`
- Modify: `docs/curriculum/part-05-dependencies.md`
- Modify: `mkdocs.yml`
- Modify: `scripts/check_site.py`
- Modify: `tests/test_chapter_15.py`
- Modify: `tests/test_chapter_16.py`
- Modify: `tests/test_chapter_17.py`
- Modify: `tests/test_chapter_18.py`
- Modify: `tests/test_chapter_19.py`
- Modify: `tests/test_chapter_20.py`
- Modify: `tests/test_part_04_consistency.py`
- Modify: `tests/test_zensical_structure.py`

- [ ] **Step 1: Add navigation and course-map entries**

Add the guide and five units under:

```yaml
- 第 21 章：积分的几何与物理模型:
    - 导学: chapters/chapter-21/index.md
    - 面积怎样从局部条带与有向积分产生？: chapters/chapter-21/u-05-21-01-area-models.md
    - 截面怎样重建立体体积？: chapters/chapter-21/u-05-21-02-volume-models.md
    - 折线长度怎样逼近光滑图像的弧长？: chapters/chapter-21/u-05-21-03-arc-length.md
    - 功、质量与平均值怎样选择局部贡献？: chapters/chapter-21/u-05-21-04-work-mass-average.md
    - 几何与物理综合建模怎样选变量并回验？: chapters/chapter-21/u-05-21-05-modeling-practice.md
```

Add the same reading order and `本章学时：7 小时（理论 4，应用 3）。` to `content/course-map.md`.

- [ ] **Step 2: Update release and dependency surfaces**

Apply these exact contracts:

```text
README: 第五部第 21 章，共 92 个学习单元
course map: 当前已发布第一至第四部及第五部第 21 章，共 92 个学习单元
dependencies: 范围：第 18–22 章，24 个核心单元
dependencies: 当前发布边界：第 21 章
```

Replace the four old Chapter 21 rows with the five dependency rows in the design. Preserve `40.5 学时` wherever the fifth-part total appears.

- [ ] **Step 3: Update rendered-site dictionaries**

Add to `scripts/check_site.py`:

```python
"chapters/chapter-21/u-05-21-02-volume-models/index.html": [
    "lem-u-05-21-02-shell-remainder",
    "thm-u-05-21-02-shell-volume",
],
"chapters/chapter-21/u-05-21-03-arc-length/index.html": [
    "def-u-05-21-03-graph-arc-length",
    "thm-u-05-21-03-c1-graph-arc-length",
],
"chapters/chapter-21/u-05-21-05-modeling-practice/index.html": [
    "alg-u-05-21-05-modeling-workflow",
    "tbl-u-05-21-05-model-selection",
],
```

Each path gets navigation markers:

```python
["md-sidebar", "第五部：积分、累积与数值求积", "第 21 章：积分的几何与物理模型"]
```

- [ ] **Step 4: Update stale global assertions**

Search:

```bash
rg -n "第五部第 20 章|87 个学习单元|当前发布边界：第 20 章|23 个核心单元" \
  README.md content docs/curriculum tests
```

Update current release assertions only. Do not rewrite historical specs, plans, or reviews.

- [ ] **Step 5: Run publication gates**

```bash
python3.12 -m unittest \
  tests.test_chapter_15 tests.test_chapter_16 tests.test_chapter_17 \
  tests.test_chapter_18 tests.test_chapter_19 tests.test_chapter_20 \
  tests.test_chapter_21 tests.test_part_04_consistency \
  tests.test_zensical_structure tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: every command exits 0.

- [ ] **Step 6: Commit**

```bash
git add README.md content/course-map.md docs/curriculum/part-05-dependencies.md \
  mkdocs.yml scripts/check_site.py tests
git commit -m "docs: publish chapter 21 modeling applications"
```

### Task 9: Audit and run the full quality gate

**Files:**

- Create: `docs/reviews/2026-07-30-chapter-21-consistency-review.md`

- [ ] **Step 1: Count the delivered training contracts**

```bash
rg -c '\{#pr-u-05-21-' content/chapters/chapter-21/u-05-21-*.md
rg -F -c '??? note "答案"' content/chapters/chapter-21/u-05-21-*.md
rg -n 'id="(thm-u-05-21-02-shell-volume|thm-u-05-21-03-c1-graph-arc-length|alg-u-05-21-05-modeling-workflow)"' \
  site/chapters/chapter-21
```

Expected exercise counts: `6, 8, 6, 6, 12`; answer counts: `8, 10, 8, 8, 16`.

- [ ] **Step 2: Write the consistency review**

Record:

```text
area: signed/geometric distinction and order-change splitting
volume: cross-section source, washer conditions, shell oscillation and quadratic remainder
arc length: polygonal supremum, refinement monotonicity, fine common refinements
physics: signed work, nonnegative density, average-value and unit contracts
practice: 12 exercises, 16 answers, mixed/diagnosis/boundary density
hours: 4+3=7
counts: 38 exercises, 50 answers
publication: Chapter 21, 92 units; Part V 24 units and 40.5 hours
boundary: Chapter 22 not started
findings: no high or medium priority findings
```

- [ ] **Step 3: Run fresh full verification**

```bash
make verify
git diff --check
git status --short
```

Expected: 0 failures, strict build and site checks pass, and only the new review is untracked.

- [ ] **Step 4: Commit the review and verify again**

```bash
git add docs/reviews/2026-07-30-chapter-21-consistency-review.md
git commit -m "docs: verify chapter 21 consistency"
make verify
git status --short
```

Expected: all gates pass and status is clean.

- [ ] **Step 5: Hand off the branch**

Use `superpowers:finishing-a-development-branch` and present exactly the four local merge / PR / keep / discard options. Do not merge or push without the user's selection.
