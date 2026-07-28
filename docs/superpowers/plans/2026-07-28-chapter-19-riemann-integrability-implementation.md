# Chapter 19 Riemann Integrability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Chapter 19 as four rigorous self-study units that motivate with tagged Riemann sums, use Darboux sums for proofs, prove the two definitions equivalent, establish core integrable classes and integral properties, then merge and push the verified result.

**Architecture:** Add one chapter guide and four `content_standard: 2` units under `content/chapters/chapter-19/`. Lock mathematical, curricular, publication, and rendered-anchor contracts in `tests/test_chapter_19.py` before writing content; implement one unit per green commit; publish only after all content contracts pass. Preserve the Chapter 20 boundary by forbidding later calculus machinery in each unit core.

**Tech Stack:** Markdown + YAML front matter, Python 3.12 `unittest`, Zensical strict build, existing content and site validators, Git worktree workflow.

---

## File map

**Create**

- `content/chapters/chapter-19/index.md` — chapter guide, learning path, dependencies, proof boundary.
- `content/chapters/chapter-19/u-05-19-01-partitions-darboux-sums.md` — partitions, tags, mesh, Darboux sums, refinement.
- `content/chapters/chapter-19/u-05-19-02-riemann-darboux-equivalence.md` — two definitions, criterion, common-refinement bridge, equivalence.
- `content/chapters/chapter-19/u-05-19-03-integrable-classes.md` — continuous, monotone, finitely piecewise-continuous classes and counterexamples.
- `content/chapters/chapter-19/u-05-19-04-integral-properties.md` — algebra, order, estimates, restrictions, interval additivity.
- `tests/test_chapter_19.py` — chapter-specific content, boundary, counts, and publication contract.
- `docs/reviews/2026-07-28-chapter-19-consistency-review.md` — final mathematical and publication audit.

**Modify**

- `docs/curriculum/part-05-dependencies.md` — advance current publication boundary to Chapter 19 only.
- `mkdocs.yml` — add Chapter 19 guide and four units after Chapter 18.
- `content/course-map.md` — add Chapter 19 hours and links; update release count to 82.
- `README.md` — update release scope to Chapter 19 and 82 units.
- `scripts/check_site.py` — require representative Chapter 19 anchors and navigation.
- `tests/test_mkdocs_site.py` — lock the new rendered-anchor dictionaries.
- Existing tests containing the old 78-unit release assertion — update to 82 without changing their chapter-local contracts.

## Locked unit contract

| Unit | Title | Theory | Applied | Minimum exercises |
|---|---|---:|---:|---:|
| `u-05-19-01` | 怎样用分割和上下和夹住未知总量？ | 1.50 | 0.25 | 6 |
| `u-05-19-02` | Riemann 和何时拥有与取样无关的极限？ | 1.50 | 0.25 | 6 |
| `u-05-19-03` | 哪些函数可积，证明障碍在哪里？ | 1.75 | 0.25 | 8 |
| `u-05-19-04` | 可积函数的代数、序与区间结构怎样传递？ | 1.25 | 0.75 | 8 |

Chapter total: theory 6, applied 1.5, total 7.5; at least 28 anchored exercises.

### Task 1: Lock Chapter 19 contracts in failing tests

**Files:**

- Create: `tests/test_chapter_19.py`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Create the chapter contract test**

Create `tests/test_chapter_19.py` with:

```python
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-19"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-05-dependencies.md"

EXPECTED_UNITS = [
    ("u-05-19-01", "怎样用分割和上下和夹住未知总量？", 1.50, 0.25, "partitions-darboux-sums", 6),
    ("u-05-19-02", "Riemann 和何时拥有与取样无关的极限？", 1.50, 0.25, "riemann-darboux-equivalence", 6),
    ("u-05-19-03", "哪些函数可积，证明障碍在哪里？", 1.75, 0.25, "integrable-classes", 8),
    ("u-05-19-04", "可积函数的代数、序与区间结构怎样传递？", 1.25, 0.75, "integral-properties", 8),
]

REQUIRED_ANCHORS = {
    "u-05-19-01": (
        "def-u-05-19-01-partition-mesh",
        "def-u-05-19-01-darboux-sums",
        "thm-u-05-19-01-refinement-monotonicity",
        "ex-u-05-19-01-linear-uniform-partition",
    ),
    "u-05-19-02": (
        "def-u-05-19-02-darboux-integrable",
        "def-u-05-19-02-riemann-integrable",
        "thm-u-05-19-02-darboux-criterion",
        "lem-u-05-19-02-common-refinement-control",
        "thm-u-05-19-02-riemann-darboux-equivalence",
    ),
    "u-05-19-03": (
        "thm-u-05-19-03-continuous-integrable",
        "thm-u-05-19-03-monotone-integrable",
        "cor-u-05-19-03-piecewise-continuous-integrable",
        "ex-u-05-19-03-dirichlet-obstruction",
    ),
    "u-05-19-04": (
        "thm-u-05-19-04-algebra-closure",
        "thm-u-05-19-04-order-bounds",
        "thm-u-05-19-04-interval-additivity",
        "tbl-u-05-19-04-property-conditions",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "Newton–Leibniz",
    "微积分基本定理",
    "积分上限函数",
    "反常积分",
    "Lebesgue",
)


def unit_path(unit):
    unit_id, _title, _theory, _applied, suffix, _exercises = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path):
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterNineteenTests(unittest.TestCase):
    def required_text(self, path):
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_final_metadata_hours_anchors_and_training(self):
        theory = applied = 0.0
        total_exercises = 0
        for unit in EXPECTED_UNITS:
            unit_id, title, theory_hours, applied_hours, _suffix, exercises = unit
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
                actual = text.count(f"{{#pr-{unit_id}-")
                self.assertGreaterEqual(actual, exercises)
                self.assertGreaterEqual(text.count('??? note "答案"'), exercises + 2)
                total_exercises += actual
                theory += float(metadata["hours"]["theory"])
                applied += float(metadata["hours"]["applied"])
        self.assertEqual(6.0, theory)
        self.assertEqual(1.5, applied)
        self.assertGreaterEqual(total_exercises, 28)

    def test_chapter_guide_lists_units_hours_route_and_boundaries(self):
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共4个核心单元，7.5学时（理论6，应用1.5）。", guide)
        self.assertIn("Riemann 取样和建立直觉", guide)
        self.assertIn("Darboux 上下和承担证明", guide)
        self.assertIn("第 18 章", guide)
        self.assertIn("第 20 章", guide)
        for unit_id, title, _theory, _applied, suffix, _exercises in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_unit_one_builds_partition_and_refinement_language(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in ("标记分割", "网格", "上和", "下和", "加细", "公共加细", r"L(f,P)\le", r"S(f;P,\xi)", r"U(f,P)"):
            self.assertIn(marker, text)

    def test_unit_two_proves_definitions_equivalent_without_refinement_shortcut(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in ("所有分割", "所有取样点", "不一定加细", "公共加细", "逼近上确界", "逼近下确界", "等价"):
            self.assertIn(marker, text)
        self.assertIn(r"\|Q\|", text)

    def test_unit_three_proves_classes_with_explicit_controls(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in ("一致连续", "振幅", r"\frac{b-a}{n}", "有限分段连续", "总长度", "Dirichlet", "单点尖峰", "无界"):
            self.assertIn(marker, text)

    def test_unit_four_proves_properties_without_antiderivative_calculation(self):
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in ("线性", "乘积", "绝对值", "最大值", "最小值", "一致远离零", "保序", "区间可加"):
            self.assertIn(marker, text)
        self.assertIn(r"\left|\int_a^b f", text)

    def test_core_does_not_use_later_integral_theory(self):
        for unit in EXPECTED_UNITS:
            path = unit_path(unit)
            if not path.is_file():
                continue
            core = path.read_text(encoding="utf-8").split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)

    def test_dependency_map_and_publication_scope(self):
        deps = self.required_text(DEPENDENCIES)
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("当前发布边界：第 19 章", deps)
        self.assertIn("第 19 章：Riemann 积分与可积性", config)
        self.assertIn("本章学时：7.5 小时（理论 6，应用 1.5）。", course_map)
        self.assertIn("第五部第 19 章，共 82 个学习单元", readme)
        for _unit_id, title, _theory, _applied, suffix, _exercises in EXPECTED_UNITS:
            path = f"chapters/chapter-19/{_unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Extend rendered-site contract tests**

Add exact expectations to `tests/test_mkdocs_site.py` for:

```python
def test_checks_chapter_nineteen_equivalence_page(self) -> None:
    page = "chapters/chapter-19/u-05-19-02-riemann-darboux-equivalence/index.html"
    self.assertEqual(
        [
            "thm-u-05-19-02-darboux-criterion",
            "lem-u-05-19-02-common-refinement-control",
            "thm-u-05-19-02-riemann-darboux-equivalence",
        ],
        REQUIRED_RENDERED_ANCHORS[page],
    )
    self.assertEqual(
        [
            "md-sidebar",
            "第五部：积分、累积与数值求积",
            "第 19 章：Riemann 积分与可积性",
        ],
        REQUIRED_NAVIGATION_MARKERS[page],
    )
```

and an analogous test for:

```python
page = "chapters/chapter-19/u-05-19-04-integral-properties/index.html"
anchors = [
    "thm-u-05-19-04-algebra-closure",
    "thm-u-05-19-04-order-bounds",
    "thm-u-05-19-04-interval-additivity",
]
```

- [ ] **Step 3: Run tests and verify RED**

Run:

```bash
python3.12 -m unittest tests.test_chapter_19 tests.test_mkdocs_site -v
```

Expected: Chapter 19 tests fail because `content/chapters/chapter-19/` and publication entries do not yet exist; existing site tests remain green.

- [ ] **Step 4: Commit the failing contract**

```bash
git add tests/test_chapter_19.py tests/test_mkdocs_site.py
git commit -m "test: lock chapter 19 Riemann integrability contract"
```

### Task 2: Establish the chapter guide

**Files:**

- Create: `content/chapters/chapter-19/index.md`

- [ ] **Step 1: Write the chapter guide**

Use front matter:

```yaml
---
title: 第 19 章：Riemann 积分与可积性
---
```

The guide must include:

```markdown
# 第 19 章：Riemann 积分与可积性 {#chapter-19}

本章共4个核心单元，7.5学时（理论6，应用1.5）。

Riemann 取样和建立直觉，Darboux 上下和承担证明；随后证明两种定义等价。
```

List the four exact links and hours from the locked unit table. State that Chapter 18 only supplies symbolic antiderivative language, while Chapter 19 defines accumulation independently; Chapter 20 is the first place that connects the two.

- [ ] **Step 2: Run the guide test**

```bash
python3.12 -m unittest tests.test_chapter_19.ChapterNineteenTests.test_chapter_guide_lists_units_hours_route_and_boundaries -v
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add content/chapters/chapter-19/index.md
git commit -m "docs: establish chapter 19 learning route"
```

### Task 3: Write Unit 19.1 partitions and Darboux sums

**Files:**

- Create: `content/chapters/chapter-19/u-05-19-01-partitions-darboux-sums.md`

- [ ] **Step 1: Add complete front matter**

```yaml
---
title: 怎样用分割和上下和夹住未知总量？
unit_id: u-05-19-01
hours: {theory: 1.50, applied: 0.25}
difficulty: 3
prerequisites:
  book: [u-01-03-02, u-02-05-02, u-02-06-02]
  higher_algebra: [有限求和, 不等式, 上确界与下确界]
  analytic_geometry: [闭区间, 区间长度, 函数图像]
  python: [列表, 循环, 有限求和]
capabilities: [tagged_partitions, darboux_sums, refinement, finite_sum_bounds]
learning_goals: [定义分割标记与网格, 构造上下和, 证明加细单调性, 用上下和夹住所有取样和]
content_standard: 2
---
```

- [ ] **Step 2: Write definitions and proofs**

Include all v2 headings. Establish, in order:

```text
bounded function on [a,b]
partition P and Δx_i
tag ξ_i and mesh ||P||
tagged sum S(f;P,ξ)
M_i=sup f and m_i=inf f on each closed subinterval
L(f,P), U(f,P)
L ≤ S ≤ U
refinement monotonicity
common refinement P∪Q
L(f,P) ≤ U(f,Q)
lower and upper integrals
```

Prove refinement monotonicity by first inserting one point, then iterating. Prove cross-partition comparison through the common refinement, not by assuming one partition refines the other.

- [ ] **Step 3: Add examples and six exercises**

Required examples:

1. `f(x)=x` on `[0,1]` with uniform partition:
   \[
   L=(n-1)/(2n),\quad U=(n+1)/(2n),\quad U-L=1/n.
   \]
2. Single-point spike, with the exceptional point trapped in intervals of arbitrarily small total length.

Six exercises must cover: mesh calculation, tagged sums, upper/lower sums for monotone functions, one-point insertion, common refinement, and proof diagnosis. Add at least eight answer blocks.

- [ ] **Step 4: Run focused tests**

```bash
python3.12 -m unittest \
  tests.test_chapter_19.ChapterNineteenTests.test_unit_one_builds_partition_and_refinement_language \
  tests.test_chapter_19.ChapterNineteenTests.test_units_have_final_metadata_hours_anchors_and_training -v
python3.12 scripts/check_content.py
```

Expected: the unit-one test and content checker pass; aggregate metadata test still fails because Units 19.2–19.4 are missing.

- [ ] **Step 5: Commit**

```bash
git add content/chapters/chapter-19/u-05-19-01-partitions-darboux-sums.md
git commit -m "docs: build partitions and Darboux sums"
```

### Task 4: Write Unit 19.2 and prove equivalence

**Files:**

- Create: `content/chapters/chapter-19/u-05-19-02-riemann-darboux-equivalence.md`

- [ ] **Step 1: Add complete front matter**

```yaml
---
title: Riemann 和何时拥有与取样无关的极限？
unit_id: u-05-19-02
hours: {theory: 1.50, applied: 0.25}
difficulty: 4
prerequisites:
  book: [u-02-05-02, u-02-06-02, u-05-19-01]
  higher_algebra: [有限求和, 三角不等式, 上确界逼近]
  analytic_geometry: [闭区间, 区间长度, 分割]
  python: [有限和, 数值比较]
capabilities: [darboux_integrability, riemann_integrability, epsilon_reasoning, equivalence_proof]
learning_goals: [使用Darboux判据, 正确书写Riemann量词, 控制公共加细误差, 证明两种定义等价]
content_standard: 2
---
```

- [ ] **Step 2: Prove the Darboux criterion**

Define lower and upper integrals, then prove:

\[
\underline{\int_a^b}f=\overline{\int_a^b}f
\iff
\forall\varepsilon>0\ \exists P:\ U(f,P)-L(f,P)<\varepsilon.
\]

Use supremum and infimum approximation explicitly in the reverse direction.

- [ ] **Step 3: State the full tagged-partition definition**

Require one value `I` such that:

```text
for every ε>0 there exists δ>0 such that
for every tagged partition (Q,ξ) with ||Q||<δ,
|S(f;Q,ξ)-I|<ε.
```

Contrast it with one regular left-endpoint sequence.

- [ ] **Step 4: Prove the common-refinement control lemma**

For a fixed partition `P={x_0,...,x_n}`, arbitrary `Q`, and `|f|≤M`, construct `P∪Q`. Bound the total lengths of `Q`-intervals that contain the `n-1` internal points of `P` by at most `(n-1)||Q||`, and use a safe bound proportional to `2M(n-1)||Q||` for each upper/lower comparison. State constants conservatively and choose `δ` from the final inequality.

- [ ] **Step 5: Prove both directions of equivalence**

For Riemann implies Darboux, choose near-supremum and near-infimum tags separately on one sufficiently fine partition. Allocate a finite error budget across subintervals; do not assume extrema are attained.

Add at least two complete examples, six exercises, and eight answers. One example must use the Dirichlet function to show dependence on tags; another must diagnose the false “small mesh means refinement” argument.

- [ ] **Step 6: Run focused tests**

```bash
python3.12 -m unittest \
  tests.test_chapter_19.ChapterNineteenTests.test_unit_two_proves_definitions_equivalent_without_refinement_shortcut \
  tests.test_chapter_19.ChapterNineteenTests.test_core_does_not_use_later_integral_theory -v
python3.12 scripts/check_content.py
```

Expected: PASS for the implemented units.

- [ ] **Step 7: Commit**

```bash
git add content/chapters/chapter-19/u-05-19-02-riemann-darboux-equivalence.md
git commit -m "docs: prove Riemann and Darboux equivalence"
```

### Task 5: Write Unit 19.3 integrable classes

**Files:**

- Create: `content/chapters/chapter-19/u-05-19-03-integrable-classes.md`

- [ ] **Step 1: Add complete front matter**

```yaml
---
title: 哪些函数可积，证明障碍在哪里？
unit_id: u-05-19-03
hours: {theory: 1.75, applied: 0.25}
difficulty: 4
prerequisites:
  book: [u-03-11-03, u-05-19-02]
  higher_algebra: [有限求和, 不等式, 单调性]
  analytic_geometry: [闭区间, 分段函数, 单调图像]
  python: [有限取样, 函数定义]
capabilities: [continuous_integrability, monotone_integrability, piecewise_integrability, counterexample_analysis]
learning_goals: [用一致连续证明可积, 给出单调函数显式控制, 直接处理有限断点, 识别不可积障碍]
content_standard: 2
---
```

- [ ] **Step 2: Prove continuous and monotone cases**

Continuous case: choose oscillation below `ε/(b-a)` using uniform continuity, then sum.

Monotone increasing case: use an equal partition and derive exactly:

\[
U-L=\frac{b-a}{n}[f(b)-f(a)].
\]

Handle the decreasing case separately or by applying the argument to `-f`; do not assume monotone functions are continuous.

- [ ] **Step 3: Prove finite piecewise continuity directly**

Around finitely many breaks choose neighborhoods with total length below an explicit error budget. Use boundedness there and uniform continuity on the remaining finite closed pieces. Do not invoke interval additivity from Unit 19.4.

- [ ] **Step 4: Add counterexamples and eight exercises**

Core contrasts:

- Dirichlet function: every nondegenerate interval has oscillation one.
- Single-point and finite-point spikes: integrable by small exceptional intervals.
- Step functions: finitely many jumps yet integrable.
- Unbounded functions: outside the bounded-function contract, not silently handled as improper integrals.

Eight exercises must include proof reconstruction, explicit `n` choice, finite spike construction, step functions, Dirichlet, and two diagnosis questions. Add at least ten answers.

- [ ] **Step 5: Run focused tests and commit**

```bash
python3.12 -m unittest \
  tests.test_chapter_19.ChapterNineteenTests.test_unit_three_proves_classes_with_explicit_controls \
  tests.test_chapter_19.ChapterNineteenTests.test_core_does_not_use_later_integral_theory -v
python3.12 scripts/check_content.py
git add content/chapters/chapter-19/u-05-19-03-integrable-classes.md
git commit -m "docs: prove core Riemann integrable classes"
```

### Task 6: Write Unit 19.4 integral properties

**Files:**

- Create: `content/chapters/chapter-19/u-05-19-04-integral-properties.md`

- [ ] **Step 1: Add complete front matter**

```yaml
---
title: 可积函数的代数、序与区间结构怎样传递？
unit_id: u-05-19-04
hours: {theory: 1.25, applied: 0.75}
difficulty: 4
prerequisites:
  book: [u-05-19-02, u-05-19-03]
  higher_algebra: [绝对值不等式, 恒等变形, 有界性]
  analytic_geometry: [区间拼接, 函数界, 最大值与最小值]
  python: [有限和, 数值点检]
capabilities: [integral_algebra, order_bounds, interval_additivity, condition_checks]
learning_goals: [证明代数封闭性, 使用保序与绝对值估计, 检查商的条件, 拆分与反向区间]
content_standard: 2
---
```

- [ ] **Step 2: Prove algebraic closure**

Use the Darboux oscillation criterion. Include scalar multiples, sums, products, absolute value, max/min via:

\[
\max(f,g)=\frac{f+g+|f-g|}{2},\qquad
\min(f,g)=\frac{f+g-|f-g|}{2}.
\]

For reciprocals, require `|g(x)|≥m>0` and use:

\[
\left|\frac1{g(x)}-\frac1{g(y)}\right|
\le \frac{|g(x)-g(y)|}{m^2}.
\]

- [ ] **Step 3: Prove order and interval structure**

Prove order preservation, constant bounds, absolute-value estimates, restriction to subintervals, interval additivity by adjoining the split point, and endpoint conventions. Include the exact property-condition table anchor.

- [ ] **Step 4: Add examples and eight exercises**

At least two examples and eight exercises must train:

- estimating an integral without evaluating it;
- checking denominator-away-from-zero before quotient closure;
- applying max/min identities;
- splitting an interval at a sign or formula change;
- detecting an invalid cancellation or reversed inequality.

Add at least ten answer blocks. Do not evaluate any definite integral by an antiderivative.

- [ ] **Step 5: Run all content contracts**

```bash
python3.12 -m unittest tests.test_chapter_19 -v
python3.12 scripts/check_content.py
```

Expected: only publication-scope assertions fail before Task 7; all unit metadata, anchors, mathematical markers, counts, and boundary tests pass.

- [ ] **Step 6: Commit**

```bash
git add content/chapters/chapter-19/u-05-19-04-integral-properties.md
git commit -m "docs: establish Riemann integral properties"
```

### Task 7: Publish Chapter 19

**Files:**

- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `README.md`
- Modify: `docs/curriculum/part-05-dependencies.md`
- Modify: `scripts/check_site.py`
- Modify: release-count assertions found under `tests/`

- [ ] **Step 1: Add navigation**

After Chapter 18 in `mkdocs.yml`, add:

```yaml
      - 第 19 章：Riemann 积分与可积性:
          - 本章导学: chapters/chapter-19/index.md
          - 19.1 怎样用分割和上下和夹住未知总量？: chapters/chapter-19/u-05-19-01-partitions-darboux-sums.md
          - 19.2 Riemann 和何时拥有与取样无关的极限？: chapters/chapter-19/u-05-19-02-riemann-darboux-equivalence.md
          - 19.3 哪些函数可积，证明障碍在哪里？: chapters/chapter-19/u-05-19-03-integrable-classes.md
          - 19.4 可积函数的代数、序与区间结构怎样传递？: chapters/chapter-19/u-05-19-04-integral-properties.md
```

- [ ] **Step 2: Update release surfaces**

Update README to contain:

```text
第五部第 19 章，共 82 个学习单元
```

Add the Chapter 19 guide, hours, and four links to `content/course-map.md`. Advance the later-route sentence to Chapter 20. In `docs/curriculum/part-05-dependencies.md`, change only:

```text
当前发布边界：第 19 章
```

and keep Chapters 20–22 as blueprint-only.

- [ ] **Step 3: Update stale release-count tests**

Run:

```bash
rg -n "78 个|第五部第 18 章|第 18 章，共" README.md content tests
```

Update only assertions that describe the current global release. Preserve chapter-local references explaining dependencies or historical boundaries.

- [ ] **Step 4: Add rendered-site requirements**

In `scripts/check_site.py`, add:

```python
"chapters/chapter-19/u-05-19-02-riemann-darboux-equivalence/index.html": [
    "thm-u-05-19-02-darboux-criterion",
    "lem-u-05-19-02-common-refinement-control",
    "thm-u-05-19-02-riemann-darboux-equivalence",
],
"chapters/chapter-19/u-05-19-04-integral-properties/index.html": [
    "thm-u-05-19-04-algebra-closure",
    "thm-u-05-19-04-order-bounds",
    "thm-u-05-19-04-interval-additivity",
],
```

Add matching navigation markers for Part V and Chapter 19.

- [ ] **Step 5: Run publication and strict-build gates**

```bash
python3.12 -m unittest tests.test_chapter_19 tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: all commands exit 0; Zensical reports `No issues found`.

- [ ] **Step 6: Commit**

```bash
git add README.md content/course-map.md docs/curriculum/part-05-dependencies.md \
  mkdocs.yml scripts/check_site.py tests
git commit -m "docs: publish chapter 19 Riemann integrability"
```

### Task 8: Audit, verify, merge, and push

**Files:**

- Create: `docs/reviews/2026-07-28-chapter-19-consistency-review.md`

- [ ] **Step 1: Write the consistency review**

Record:

- the hybrid teaching route;
- the common-refinement proof safeguard;
- no circular use of interval additivity in Unit 19.3;
- explicit continuous and monotone controls;
- 4 units, `6+1.5=7.5` hours, at least 28 exercises;
- 82 published units and Chapter 19 release boundary;
- Chapter 20 not started;
- exact final test/build evidence.

- [ ] **Step 2: Run fresh full verification on the feature branch**

```bash
make verify
git diff --check
git status --short
```

Expected: all tests pass, content/site validators pass, strict build has no issues, and only the uncommitted review exists before its commit.

- [ ] **Step 3: Commit the review and verify again**

```bash
git add docs/reviews/2026-07-28-chapter-19-consistency-review.md
git commit -m "docs: verify chapter 19 consistency"
make verify
git status --short
```

Expected: clean worktree and all gates pass.

- [ ] **Step 4: Fast-forward merge to main**

From the main worktree:

```bash
git pull --ff-only
git merge --ff-only codex/chapter-19-riemann-integrability
make verify
```

Expected: pull succeeds, merge is fast-forward, and merged `main` passes all gates.

- [ ] **Step 5: Push GitHub and confirm**

```bash
git push origin main
git status -sb
git rev-parse HEAD
git rev-parse origin/main
```

Expected: push succeeds; local `main` and `origin/main` resolve to the same commit.

- [ ] **Step 6: Clean up**

Remove the clean worktree and delete the merged local feature branch:

```bash
git worktree remove .worktrees/chapter-19-riemann-integrability
git branch -d codex/chapter-19-riemann-integrability
```
