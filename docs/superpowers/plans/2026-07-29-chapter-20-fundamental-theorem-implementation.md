# Chapter 20 Fundamental Theorem Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Chapter 20 as five rigorous self-study units that connect Riemann accumulation to differentiation and antiderivatives, derive legal definite-integration rules, and add an independent mixed-practice unit.

**Architecture:** Add one chapter guide and five `content_standard: 2` units under `content/chapters/chapter-20/`. Lock mathematical, training, publication, and rendered-anchor contracts in failing tests before writing content; implement one dependency-closed unit per green commit; publish only after all five content contracts pass. Keep geometry models, improper integrals, numerical quadrature, and parameter differentiation outside the chapter core.

**Tech Stack:** Markdown + YAML front matter, Python 3.12 `unittest`, Zensical strict build, existing content and rendered-site validators, Git worktree workflow.

---

## File map

**Create**

- `content/chapters/chapter-20/index.md` — chapter guide, proof ladder, dependencies, and Chapter 21 boundary.
- `content/chapters/chapter-20/u-05-20-01-accumulation-continuity.md` — variable-upper-limit accumulation and Lipschitz continuity.
- `content/chapters/chapter-20/u-05-20-02-fundamental-theorem-part-one.md` — local averages and pointwise FTC Part I.
- `content/chapters/chapter-20/u-05-20-03-newton-leibniz.md` — primitive existence and two Newton–Leibniz proof levels.
- `content/chapters/chapter-20/u-05-20-04-definite-substitution-parts.md` — definite substitution and integration by parts.
- `content/chapters/chapter-20/u-05-20-05-definite-integral-practice.md` — endpoint, symmetry, mixed-method, and diagnosis practice.
- `tests/test_chapter_20.py` — chapter metadata, mathematics, counts, boundaries, dependencies, and publication contract.
- `docs/reviews/2026-07-29-chapter-20-consistency-review.md` — final mathematical and publication audit.

**Modify**

- `docs/curriculum/part-05-dependencies.md` — add Unit 20.5, change 22 units to 23, and advance the current boundary to Chapter 20.
- `mkdocs.yml` — add the Chapter 20 guide and five units after Chapter 19.
- `content/course-map.md` — add Chapter 20 hours and links; update release count to 87.
- `README.md` — update release scope to Chapter 20 and 87 units.
- `scripts/check_site.py` — require representative Chapter 20 anchors and navigation.
- `tests/test_mkdocs_site.py` — lock Chapter 20 rendered-anchor dictionaries.
- `tests/test_chapter_15.py`, `tests/test_chapter_16.py`, `tests/test_chapter_17.py`, `tests/test_chapter_18.py`, `tests/test_chapter_19.py`, `tests/test_part_04_consistency.py`, `tests/test_zensical_structure.py` — update only global release assertions; preserve chapter-local contracts.

## Locked unit contract

| Unit | Title | Theory | Applied | Minimum exercises | Minimum answers |
|---|---|---:|---:|---:|---:|
| `u-05-20-01` | 变上限累积函数为什么连续？ | 1.25 | 0.25 | 6 | 8 |
| `u-05-20-02` | 局部平均怎样恢复被积函数？ | 1.50 | 0.25 | 6 | 8 |
| `u-05-20-03` | 原函数怎样把分割极限化为端点差？ | 1.25 | 0.50 | 6 | 8 |
| `u-05-20-04` | 定积分的换元与分部积分怎样合法使用？ | 1.00 | 1.00 | 8 | 10 |
| `u-05-20-05` | 定积分综合计算怎样处理端点、对称与错误诊断？ | 0.25 | 0.75 | 12 | 14 |

Chapter total: theory 5.25, applied 2.75, total 8; at least 38 anchored exercises and 48 collapsed answers.

### Task 1: Lock Chapter 20 contracts in failing tests

**Files:**

- Create: `tests/test_chapter_20.py`
- Modify: `tests/test_mkdocs_site.py`

- [ ] **Step 1: Create the chapter contract test**

Create `tests/test_chapter_20.py` with:

```python
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-20"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-05-dependencies.md"

EXPECTED_UNITS = [
    (
        "u-05-20-01",
        "变上限累积函数为什么连续？",
        1.25,
        0.25,
        "accumulation-continuity",
        6,
        8,
    ),
    (
        "u-05-20-02",
        "局部平均怎样恢复被积函数？",
        1.50,
        0.25,
        "fundamental-theorem-part-one",
        6,
        8,
    ),
    (
        "u-05-20-03",
        "原函数怎样把分割极限化为端点差？",
        1.25,
        0.50,
        "newton-leibniz",
        6,
        8,
    ),
    (
        "u-05-20-04",
        "定积分的换元与分部积分怎样合法使用？",
        1.00,
        1.00,
        "definite-substitution-parts",
        8,
        10,
    ),
    (
        "u-05-20-05",
        "定积分综合计算怎样处理端点、对称与错误诊断？",
        0.25,
        0.75,
        "definite-integral-practice",
        12,
        14,
    ),
]

REQUIRED_ANCHORS = {
    "u-05-20-01": (
        "def-u-05-20-01-accumulation-function",
        "thm-u-05-20-01-lipschitz-continuity",
        "cor-u-05-20-01-basepoint-shift",
        "ex-u-05-20-01-step-accumulation",
    ),
    "u-05-20-02": (
        "lem-u-05-20-02-local-average-control",
        "thm-u-05-20-02-ftc-part-one-pointwise",
        "cor-u-05-20-02-continuous-integrand",
        "ex-u-05-20-02-jump-boundary",
        "ex-u-05-20-02-single-point-redefinition",
    ),
    "u-05-20-03": (
        "thm-u-05-20-03-continuous-primitive-existence",
        "thm-u-05-20-03-newton-leibniz-continuous",
        "thm-u-05-20-03-newton-leibniz-integrable-derivative",
        "tbl-u-05-20-03-existence-representation-computation",
        "ex-u-05-20-03-gaussian-boundary",
    ),
    "u-05-20-04": (
        "thm-u-05-20-04-definite-substitution",
        "tbl-u-05-20-04-forward-vs-inverse-substitution",
        "ex-u-05-20-04-decreasing-substitution",
        "thm-u-05-20-04-definite-integration-by-parts",
        "cor-u-05-20-04-piecewise-rules",
    ),
    "u-05-20-05": (
        "tbl-u-05-20-05-method-selection",
        "thm-u-05-20-05-reflection-symmetry",
        "cor-u-05-20-05-even-odd",
        "cor-u-05-20-05-period-shift",
        "ex-u-05-20-05-cyclic-parts",
        "ex-u-05-20-05-illegal-substitution",
    ),
}

MINIMUM_EXAMPLES = {
    "u-05-20-01": 2,
    "u-05-20-02": 2,
    "u-05-20-03": 2,
    "u-05-20-04": 3,
    "u-05-20-05": 4,
}

MINIMUM_CHECKS = {
    "u-05-20-01": 2,
    "u-05-20-02": 2,
    "u-05-20-03": 2,
    "u-05-20-04": 2,
    "u-05-20-05": 4,
}

FORBIDDEN_CORE_TERMS = (
    "反常积分",
    "主值积分",
    "数值求积",
    "Simpson",
    "积分号下求导",
    "Lebesgue",
    "旋转体",
    "弧长公式",
)


def unit_path(
    unit: tuple[str, str, float, float, str, int, int],
) -> Path:
    unit_id, _title, _theory, _applied, suffix, _exercises, _answers = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterTwentyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_final_metadata_hours_anchors_and_training(self) -> None:
        theory = 0.0
        applied = 0.0
        total_exercises = 0
        total_answers = 0
        for unit in EXPECTED_UNITS:
            (
                unit_id,
                title,
                theory_hours,
                applied_hours,
                _suffix,
                exercises,
                answers,
            ) = unit
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
                self.assertGreaterEqual(
                    text.count("### 例 "),
                    MINIMUM_EXAMPLES[unit_id],
                )
                self.assertGreaterEqual(
                    text.count("### 即时检验 "),
                    MINIMUM_CHECKS[unit_id],
                )
                actual_exercises = text.count(f"{{#pr-{unit_id}-")
                actual_answers = text.count('??? note "答案"')
                self.assertGreaterEqual(actual_exercises, exercises)
                self.assertGreaterEqual(actual_answers, answers)
                total_exercises += actual_exercises
                total_answers += actual_answers
                theory += float(metadata["hours"]["theory"])
                applied += float(metadata["hours"]["applied"])
        self.assertEqual(5.25, theory)
        self.assertEqual(2.75, applied)
        self.assertGreaterEqual(total_exercises, 38)
        self.assertGreaterEqual(total_answers, 48)

    def test_chapter_guide_lists_units_hours_route_and_boundaries(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共5个核心单元，8学时（理论5.25，应用2.75）。", guide)
        for marker in (
            "Riemann 分割极限",
            "变上限累积函数",
            "局部变化率",
            "原函数端点差",
            "第 18 章",
            "第 19 章",
            "第 21 章",
        ):
            self.assertIn(marker, guide)
        for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_unit_one_proves_continuity_from_integral_bounds(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in (
            "Riemann 可积",
            "有界",
            "区间可加",
            "Lipschitz",
            "一致连续",
            "不同基点",
            r"|A_c(y)-A_c(x)|",
            r"M|y-x|",
        ):
            self.assertIn(marker, text)

    def test_unit_two_recovers_only_continuity_points(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in (
            "局部平均",
            "连续点",
            "右导数",
            "左导数",
            "阶跃",
            "单点改值",
            "充分条件",
            "不是必要条件",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"A'(x_0)=f(x_0)", text)

    def test_unit_three_separates_two_newton_leibniz_levels(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in (
            "连续函数",
            "原函数存在",
            "相差常数",
            "已有原函数",
            "Lagrange 中值定理",
            "Riemann 和",
            "初等原函数",
            r"e^{-x^2}",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"G(b)-G(a)", text)

    def test_unit_four_derives_rules_with_conditions(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in (
            "链式法则",
            "乘积法则",
            "不要求",
            "单调",
            "反解变量",
            "递减",
            "边界项",
            "分段",
            "全局连续",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"\phi\in C^1", text)
        self.assertIn(r"[u(x)v(x)]_a^b", text)

    def test_unit_five_has_mixed_training_and_diagnosis_density(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[4]))
        self.assertGreaterEqual(text.count("{#pr-u-05-20-05-mixed-"), 4)
        self.assertGreaterEqual(text.count("{#pr-u-05-20-05-diagnosis-"), 3)
        self.assertGreaterEqual(text.count("{#pr-u-05-20-05-boundary-"), 2)
        for marker in (
            "区间与定义域",
            "结构识别",
            "路线选择",
            "中点反射",
            "奇函数",
            "偶函数",
            "周期",
            "循环分部积分",
            "首个非法步骤",
            "数值点检只能",
        ):
            self.assertIn(marker, text)

    def test_core_does_not_use_later_integral_theory(self) -> None:
        for unit in EXPECTED_UNITS:
            path = unit_path(unit)
            if not path.is_file():
                continue
            core = path.read_text(encoding="utf-8").split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)

    def test_dependency_map_and_publication_scope(self) -> None:
        deps = self.required_text(DEPENDENCIES)
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("23 个核心单元", deps)
        self.assertIn("当前发布边界：第 20 章", deps)
        self.assertIn(
            "| `u-05-20-05` | `u-05-20-04`、`u-05-19-04` |",
            deps,
        )
        self.assertIn("第 20 章：微积分基本定理", config)
        self.assertIn("本章学时：8 小时（理论 5.25，应用 2.75）。", course_map)
        self.assertIn("第五部第 20 章，共 87 个学习单元", readme)
        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
            path = f"chapters/chapter-20/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            navigation_positions.append(config.index(path))
            map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Add rendered-site contract tests**

Append these methods to `ZensicalSiteValidationTests` in `tests/test_mkdocs_site.py`:

```python
def test_checks_chapter_twenty_ftc_page(self) -> None:
    page = "chapters/chapter-20/u-05-20-02-fundamental-theorem-part-one/index.html"
    self.assertEqual(
        [
            "lem-u-05-20-02-local-average-control",
            "thm-u-05-20-02-ftc-part-one-pointwise",
        ],
        REQUIRED_RENDERED_ANCHORS[page],
    )
    self.assertEqual(
        [
            "md-sidebar",
            "第五部：积分、累积与数值求积",
            "第 20 章：微积分基本定理",
        ],
        REQUIRED_NAVIGATION_MARKERS[page],
    )

def test_checks_chapter_twenty_newton_leibniz_page(self) -> None:
    page = "chapters/chapter-20/u-05-20-03-newton-leibniz/index.html"
    self.assertEqual(
        [
            "thm-u-05-20-03-newton-leibniz-continuous",
            "thm-u-05-20-03-newton-leibniz-integrable-derivative",
        ],
        REQUIRED_RENDERED_ANCHORS[page],
    )
    self.assertEqual(
        [
            "md-sidebar",
            "第五部：积分、累积与数值求积",
            "第 20 章：微积分基本定理",
        ],
        REQUIRED_NAVIGATION_MARKERS[page],
    )

def test_checks_chapter_twenty_practice_page(self) -> None:
    page = "chapters/chapter-20/u-05-20-05-definite-integral-practice/index.html"
    self.assertEqual(
        [
            "tbl-u-05-20-05-method-selection",
            "thm-u-05-20-05-reflection-symmetry",
        ],
        REQUIRED_RENDERED_ANCHORS[page],
    )
    self.assertEqual(
        [
            "md-sidebar",
            "第五部：积分、累积与数值求积",
            "第 20 章：微积分基本定理",
        ],
        REQUIRED_NAVIGATION_MARKERS[page],
    )
```

- [ ] **Step 3: Run tests and verify RED**

Run:

```bash
python3.12 -m unittest tests.test_chapter_20 tests.test_mkdocs_site -v
```

Expected: Chapter 20 tests fail because `content/chapters/chapter-20/` and publication entries do not exist; the three new site tests fail because Chapter 20 dictionaries are not yet present.

- [ ] **Step 4: Commit the failing contract**

```bash
git add tests/test_chapter_20.py tests/test_mkdocs_site.py
git commit -m "test: lock chapter 20 fundamental theorem contract"
```

### Task 2: Establish the chapter guide

**Files:**

- Create: `content/chapters/chapter-20/index.md`

- [ ] **Step 1: Write the chapter guide**

Use:

```markdown
---
title: 第 20 章：微积分基本定理
---

# 第 20 章：微积分基本定理 {#chapter-20}

本章共5个核心单元，8学时（理论5.25，应用2.75）。
```

List the five exact unit links and hours from the locked unit table. Include the proof ladder:

```text
Riemann 分割极限
→ 变上限累积函数
→ 局部变化率
→ 原函数端点差
→ 定积分计算规则
```

State that Chapter 18 supplies primitive methods, Chapter 19 independently defines and studies the integral, and Chapter 20 now proves when the two can be connected. State that Chapter 21 owns geometry and physical models.

- [ ] **Step 2: Run the guide test**

```bash
python3.12 -m unittest \
  tests.test_chapter_20.ChapterTwentyTests.test_chapter_guide_lists_units_hours_route_and_boundaries -v
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add content/chapters/chapter-20/index.md
git commit -m "docs: establish chapter 20 proof route"
```

### Task 3: Write Unit 20.1 accumulation continuity

**Files:**

- Create: `content/chapters/chapter-20/u-05-20-01-accumulation-continuity.md`

- [ ] **Step 1: Add complete front matter**

```yaml
---
title: 变上限累积函数为什么连续？
unit_id: u-05-20-01
hours: {theory: 1.25, applied: 0.25}
difficulty: 3
prerequisites:
  book: [u-05-19-03, u-05-19-04]
  higher_algebra: [绝对值不等式, 常数界, 函数差]
  analytic_geometry: [闭区间, 区间长度, Lipschitz 条件]
  python: [函数定义, 数值抽样, 差值比较]
capabilities: [accumulation_function, lipschitz_bound, basepoint_change, endpoint_orientation]
learning_goals: [定义变上限累积函数, 证明Lipschitz连续, 比较不同基点, 处理反向端点]
content_standard: 2
---
```

- [ ] **Step 2: Write the definition and Lipschitz proof**

Include every v2 heading. For a Riemann integrable `f` on `[a,b]`, fixed `c∈[a,b]`, and `|f|≤M`, define:

```latex
A_c(x)=\int_c^x f(t)\,dt.
```

Use interval additivity and endpoint orientation to derive:

```latex
A_c(y)-A_c(x)=\int_x^y f(t)\,dt,
\qquad
|A_c(y)-A_c(x)|\le M|y-x|.
```

Conclude Lipschitz continuity and uniform continuity without assuming `f` continuous. For basepoints `c,d`, derive exactly:

```latex
A_c(x)-A_d(x)=\int_c^d f(t)\,dt.
```

Do not call `M` a maximum unless the example actually attains it.

- [ ] **Step 3: Add examples and six exercises**

Required examples:

1. A step function whose accumulation is continuous and piecewise linear, anchored by `ex-u-05-20-01-step-accumulation`.
2. A bounded oscillatory integrable function where the Lipschitz estimate gives continuity without evaluating the integral.

Six anchored exercises must cover endpoint orientation, a constant integrand, different basepoints, a step function, a supplied uniform bound, and diagnosis of the false claim “the integrand must be continuous.” Add at least eight answer blocks.

Add two immediate checks: one asks for a Lipschitz constant from a supplied bound, and one asks students to compare two basepoints without evaluating either accumulation function.

- [ ] **Step 4: Run focused checks**

```bash
python3.12 -m unittest \
  tests.test_chapter_20.ChapterTwentyTests.test_unit_one_proves_continuity_from_integral_bounds \
  tests.test_chapter_20.ChapterTwentyTests.test_core_does_not_use_later_integral_theory -v
python3.12 scripts/check_content.py
```

Expected: implemented-unit tests and the content checker pass; the aggregate metadata test still fails because Units 20.2–20.5 are missing.

- [ ] **Step 5: Commit**

```bash
git add content/chapters/chapter-20/u-05-20-01-accumulation-continuity.md
git commit -m "docs: prove accumulation function continuity"
```

### Task 4: Write Unit 20.2 pointwise FTC Part I

**Files:**

- Create: `content/chapters/chapter-20/u-05-20-02-fundamental-theorem-part-one.md`

- [ ] **Step 1: Add complete front matter**

```yaml
---
title: 局部平均怎样恢复被积函数？
unit_id: u-05-20-02
hours: {theory: 1.50, applied: 0.25}
difficulty: 4
prerequisites:
  book: [u-03-10-01, u-04-13-02, u-05-20-01]
  higher_algebra: [绝对值不等式, 平均值, 差商]
  analytic_geometry: [单侧邻域, 闭区间端点, 分段函数]
  python: [函数定义, 单侧抽样, 差商比较]
capabilities: [local_average, pointwise_ftc, endpoint_derivatives, discontinuity_diagnosis]
learning_goals: [把差商改写为局部平均, 在连续点恢复被积函数, 处理端点单侧导数, 诊断间断点边界]
content_standard: 2
---
```

- [ ] **Step 2: Prove the local-average control lemma**

For interior `x_0` and signed `h` with the interval inside `[a,b]`, derive:

```latex
\frac{A(x_0+h)-A(x_0)}{h}
=\frac1h\int_{x_0}^{x_0+h}f(t)\,dt
```

and:

```latex
\left|
\frac1h\int_{x_0}^{x_0+h}f(t)\,dt-f(x_0)
\right|
\le
\sup_{t\in I_h}|f(t)-f(x_0)|.
```

Define `I_h` using the two endpoints so the same argument is valid for positive and negative `h`.

- [ ] **Step 3: State and prove the pointwise theorem**

If `f` is Riemann integrable on `[a,b]` and continuous at interior `x_0`, prove:

```latex
A'(x_0)=f(x_0).
```

State separate right-derivative and left-derivative conclusions at `a` and `b`. Then state the whole-interval continuous corollary. Do not replace pointwise continuity by uniform continuity.

- [ ] **Step 4: Add the two required boundary examples**

1. A jump function where left and right local averages differ, so accumulation is not differentiable at the jump.
2. A function changed at one point only: its accumulation is unchanged and differentiable there, but the derivative need not equal the reassigned point value.

Say explicitly that continuity is a sufficient condition for recovery, not a necessary condition for the existence of the derivative.

Add six exercises and eight answers covering signed `h`, endpoint derivatives, a continuous example, a jump, a single-point redefinition, and an overstrong-conclusion diagnosis.

Add two immediate checks: one rewrites a negative-`h` difference quotient as a local average, and one identifies the correct one-sided derivative at an endpoint.

- [ ] **Step 5: Run focused checks and commit**

```bash
python3.12 -m unittest \
  tests.test_chapter_20.ChapterTwentyTests.test_unit_two_recovers_only_continuity_points \
  tests.test_chapter_20.ChapterTwentyTests.test_core_does_not_use_later_integral_theory -v
python3.12 scripts/check_content.py
git add content/chapters/chapter-20/u-05-20-02-fundamental-theorem-part-one.md
git commit -m "docs: prove pointwise fundamental theorem"
```

### Task 5: Write Unit 20.3 Newton–Leibniz

**Files:**

- Create: `content/chapters/chapter-20/u-05-20-03-newton-leibniz.md`

- [ ] **Step 1: Add complete front matter**

```yaml
---
title: 原函数怎样把分割极限化为端点差？
unit_id: u-05-20-03
hours: {theory: 1.25, applied: 0.50}
difficulty: 4
prerequisites:
  book: [u-04-15-01, u-05-18-01, u-05-19-02, u-05-20-02]
  higher_algebra: [有限求和, 望远镜求和, 恒等变形]
  analytic_geometry: [闭区间, 工作区间, 端点方向]
  python: [符号点检, 数值抽样, 误差比较]
capabilities: [primitive_existence, newton_leibniz, riemann_sum_telescoping, condition_separation]
learning_goals: [证明连续函数存在原函数, 使用端点差公式, 证明已有原函数加强版, 区分存在表示与计算]
content_standard: 2
---
```

- [ ] **Step 2: Prove the continuous version without circularity**

From Unit 20.2, use:

```latex
A(x)=\int_a^x f(t)\,dt,\qquad A'=f
```

for continuous `f`. This proves primitive existence. If `G'=f`, use the Chapter 18 constant-difference theorem to obtain:

```latex
\int_a^b f(x)\,dx=G(b)-G(a).
```

Handle `a=b` and `a>b` through the established endpoint convention.

- [ ] **Step 3: Prove the existing-primitive strengthened version**

Assume only that `f` is Riemann integrable on `[a,b]` and `G'=f`. For each partition interval, apply the Lagrange mean value theorem to choose `ξ_i` with:

```latex
G(x_i)-G(x_{i-1})
=f(\xi_i)(x_i-x_{i-1}).
```

Sum to get an exact tagged Riemann sum equal to `G(b)-G(a)`, then invoke the Riemann-sum definition. Explicitly verify continuity of `G` on each closed subinterval and differentiability inside it.

- [ ] **Step 4: Separate existence, representation, and computation**

Add the required table with three independent questions:

```text
Is f Riemann integrable?
Does f have a primitive?
Can a primitive be written in the current elementary toolbox?
```

Use `e^{-x^2}` on a finite interval to show that continuity gives a primitive and a definite integral even when no elementary closed form is supplied. Do not claim or prove the non-elementarity theorem.

Include two complete examples: one direct endpoint-difference computation with a verified primitive, and the Gaussian existence/representation boundary. Add two immediate checks that distinguish assumptions in the continuous and existing-primitive versions.

Add six exercises and eight answers covering primitive verification, reversed endpoints, the MVT–Riemann-sum proof, a piecewise working interval, a false existence inference, and the Gaussian boundary example.

- [ ] **Step 5: Run focused checks and commit**

```bash
python3.12 -m unittest \
  tests.test_chapter_20.ChapterTwentyTests.test_unit_three_separates_two_newton_leibniz_levels \
  tests.test_chapter_20.ChapterTwentyTests.test_core_does_not_use_later_integral_theory -v
python3.12 scripts/check_content.py
git add content/chapters/chapter-20/u-05-20-03-newton-leibniz.md
git commit -m "docs: prove Newton Leibniz formula"
```

### Task 6: Write Unit 20.4 definite substitution and parts

**Files:**

- Create: `content/chapters/chapter-20/u-05-20-04-definite-substitution-parts.md`

- [ ] **Step 1: Add complete front matter**

```yaml
---
title: 定积分的换元与分部积分怎样合法使用？
unit_id: u-05-20-04
hours: {theory: 1.00, applied: 1.00}
difficulty: 4
prerequisites:
  book: [u-04-14-01, u-04-14-02, u-05-18-02, u-05-18-03, u-05-20-03]
  higher_algebra: [恒等变形, 复合函数, 乘积展开]
  analytic_geometry: [像区间, 方向, 逆函数分支, 分段]
  python: [符号回验, 端点代入, 数值点检]
capabilities: [definite_substitution, endpoint_transform, definite_parts, piecewise_rules]
learning_goals: [从链式法则推出定积分换元, 同步变换端点方向, 从乘积法则推出分部积分, 检查分段条件]
content_standard: 2
---
```

- [ ] **Step 2: Derive definite substitution**

Under the sufficient conditions:

```latex
\phi\in C^1[\alpha,\beta],
\qquad
f\text{ continuous on an interval containing }\phi([\alpha,\beta]),
```

choose `F'=f`, apply the chain rule to `F∘φ`, and derive:

```latex
\int_\alpha^\beta f(\phi(t))\phi'(t)\,dt
=
\int_{\phi(\alpha)}^{\phi(\beta)}f(u)\,du.
```

State explicitly that this forward formula does not require `φ` to be monotone. In the required forward-versus-inverse table, distinguish it from solving `u=φ(t)` for `t`, which may require injectivity, an inverse branch, and domain checks.

- [ ] **Step 3: Handle direction and piecewise conditions**

Include a decreasing-substitution example where the transformed limits reverse automatically. For piecewise `C^1` extensions, require global continuity and `C^1` regularity on each finite piece; use interval additivity and show internal boundary terms cancel. Do not hide a jump at a splice point.

- [ ] **Step 4: Derive definite integration by parts**

For `u,v∈C^1[a,b]`, integrate the product rule to obtain:

```latex
\int_a^b u(x)v'(x)\,dx
=[u(x)v(x)]_a^b-\int_a^b u'(x)v(x)\,dx.
```

Explain that the bracket is one complete boundary term evaluated at both endpoints. Include one polynomial–exponential example and one finite-piece example.

Together with the decreasing-substitution example, these give three complete examples. Add two immediate checks: one transforms bounds for a decreasing map, and one expands a boundary bracket correctly.

Add eight exercises and ten answers covering condition checks, increasing and decreasing substitutions, a nonmonotone forward parameterization, illegal inverse use, one-step parts, boundary-term diagnosis, and finite-piece splicing.

- [ ] **Step 5: Run focused checks and commit**

```bash
python3.12 -m unittest \
  tests.test_chapter_20.ChapterTwentyTests.test_unit_four_derives_rules_with_conditions \
  tests.test_chapter_20.ChapterTwentyTests.test_core_does_not_use_later_integral_theory -v
python3.12 scripts/check_content.py
git add content/chapters/chapter-20/u-05-20-04-definite-substitution-parts.md
git commit -m "docs: derive definite integration rules"
```

### Task 7: Write Unit 20.5 mixed definite-integral practice

**Files:**

- Create: `content/chapters/chapter-20/u-05-20-05-definite-integral-practice.md`

- [ ] **Step 1: Add complete front matter**

```yaml
---
title: 定积分综合计算怎样处理端点、对称与错误诊断？
unit_id: u-05-20-05
hours: {theory: 0.25, applied: 0.75}
difficulty: 4
prerequisites:
  book: [u-05-18-05, u-05-19-04, u-05-20-04]
  higher_algebra: [恒等变形, 奇偶性, 参数分类]
  analytic_geometry: [对称区间, 中点反射, 分段与定义域]
  python: [符号回验, 数值抽样, 误差报警]
capabilities: [definite_method_selection, reflection_symmetry, mixed_routes, error_diagnosis]
learning_goals: [无标签选择定积分方法, 使用反射奇偶与周期结构, 组合换元和分部, 定位首个非法步骤]
content_standard: 2
---
```

- [ ] **Step 2: Add the method-selection table**

Use the exact workflow:

```text
区间与定义域
→ 结构识别
→ 路线选择
→ 端点或边界项
→ 完整计算
→ 符号与估计回验
```

The table must give entry conditions and exit signals for splitting, substitution, integration by parts, reflection, and periodicity. State that a longer route is not automatically illegal, while an undefined inverse branch or missing boundary term is illegal.

- [ ] **Step 3: Prove symmetry and periodicity tools**

From `x=a+b-t`, prove:

```latex
\int_a^b f(x)\,dx
=\int_a^b f(a+b-x)\,dx.
```

Derive even/odd formulas on `[-a,a]`. For a continuous `T`-periodic function, prove shift-invariance of one-period integrals using interval additivity and a translation substitution; do not use geometric area language.

- [ ] **Step 4: Add four complete examples**

Required examples:

1. A midpoint-reflection simplification.
2. A piecewise or absolute-value integral that must be split before applying a rule.
3. A cyclic integration-by-parts example such as `∫ e^x sin x dx` on fixed finite bounds.
4. An illegal substitution diagnosis with a lost branch, missing limit transformation, or unsupported inverse.

- [ ] **Step 5: Add four immediate checks**

The checks must ask for: the reflection partner of an integrand, the sign of an odd-function integral, the legal split point for an absolute value, and the first boundary-term error in a short derivation.

- [ ] **Step 6: Add the locked mixed exercise bank**

Create at least twelve exercises and fourteen answers. Use invisible stable-anchor classifications:

```text
pr-u-05-20-05-mixed-01 ... mixed-04
pr-u-05-20-05-diagnosis-01 ... diagnosis-03
pr-u-05-20-05-boundary-01 ... boundary-02
pr-u-05-20-05-core-01 ... core-03
```

Mix their visible order so the anchors do not become displayed method labels. Every answer must include conditions, key transformation, result, and a symbolic or estimate-based check. Include the sentence “数值点检只能作为报警器，不能证明积分恒等式。”

- [ ] **Step 7: Run all content contracts**

```bash
python3.12 -m unittest tests.test_chapter_20 -v
python3.12 scripts/check_content.py
```

Expected: only publication-scope assertions fail before Task 8; all metadata, anchors, mathematical markers, exercise counts, answer counts, and boundary tests pass.

- [ ] **Step 8: Commit**

```bash
git add content/chapters/chapter-20/u-05-20-05-definite-integral-practice.md
git commit -m "docs: add definite integral mixed practice"
```

### Task 8: Publish Chapter 20

**Files:**

- Modify: `mkdocs.yml`
- Modify: `content/course-map.md`
- Modify: `README.md`
- Modify: `docs/curriculum/part-05-dependencies.md`
- Modify: `scripts/check_site.py`
- Modify: global release assertions under `tests/`

- [ ] **Step 1: Add navigation**

After Chapter 19 in `mkdocs.yml`, add exactly one entry for each page:

```yaml
      - 第 20 章：微积分基本定理:
          - 本章导学: chapters/chapter-20/index.md
          - 20.1 变上限累积函数为什么连续？: chapters/chapter-20/u-05-20-01-accumulation-continuity.md
          - 20.2 局部平均怎样恢复被积函数？: chapters/chapter-20/u-05-20-02-fundamental-theorem-part-one.md
          - 20.3 原函数怎样把分割极限化为端点差？: chapters/chapter-20/u-05-20-03-newton-leibniz.md
          - 20.4 定积分的换元与分部积分怎样合法使用？: chapters/chapter-20/u-05-20-04-definite-substitution-parts.md
          - 20.5 定积分综合计算怎样处理端点、对称与错误诊断？: chapters/chapter-20/u-05-20-05-definite-integral-practice.md
```

- [ ] **Step 2: Update dependency and release surfaces**

In `docs/curriculum/part-05-dependencies.md`:

```text
范围：第 18–22 章，23 个核心单元
当前发布边界：第 20 章
```

Change the blueprint sentence to Chapters 21–22, insert:

```markdown
| `u-05-20-05` | `u-05-20-04`、`u-05-19-04` | 定积分综合选法、对称变换、错误诊断与回验 |
```

and extend the Chapter 20 responsibility statement to include the independent practice unit.

Update README to:

```text
第五部第 20 章，共 87 个学习单元
```

Add the Chapter 20 heading, `8 小时（理论 5.25，应用 2.75）`, and five links to `content/course-map.md`. Change the later-route sentence to Chapter 21.

- [ ] **Step 3: Update stale global assertions only**

Run:

```bash
rg -n "第五部第 19 章|82 个学习单元|当前发布边界：第 19 章|22 个核心单元" \
  README.md content docs/curriculum tests
```

Update global release assertions in the seven listed existing test files. In `tests/test_chapter_18.py`, rename the dependency-map test to `test_dependency_map_covers_all_twenty_three_units`, change Chapter 20's expected count from 4 to 5, and expect the Chapter 20 boundary. Preserve Chapter 18/19 historical teaching statements and local page links.

- [ ] **Step 4: Add rendered-site requirements**

Add to both `REQUIRED_RENDERED_ANCHORS` and `REQUIRED_NAVIGATION_MARKERS` in `scripts/check_site.py`:

```python
"chapters/chapter-20/u-05-20-02-fundamental-theorem-part-one/index.html": [
    "lem-u-05-20-02-local-average-control",
    "thm-u-05-20-02-ftc-part-one-pointwise",
],
"chapters/chapter-20/u-05-20-03-newton-leibniz/index.html": [
    "thm-u-05-20-03-newton-leibniz-continuous",
    "thm-u-05-20-03-newton-leibniz-integrable-derivative",
],
"chapters/chapter-20/u-05-20-05-definite-integral-practice/index.html": [
    "tbl-u-05-20-05-method-selection",
    "thm-u-05-20-05-reflection-symmetry",
],
```

Each navigation value must be:

```python
[
    "md-sidebar",
    "第五部：积分、累积与数值求积",
    "第 20 章：微积分基本定理",
]
```

- [ ] **Step 5: Run publication and strict-build gates**

```bash
python3.12 -m unittest \
  tests.test_chapter_15 \
  tests.test_chapter_16 \
  tests.test_chapter_17 \
  tests.test_chapter_18 \
  tests.test_chapter_19 \
  tests.test_chapter_20 \
  tests.test_part_04_consistency \
  tests.test_zensical_structure \
  tests.test_mkdocs_site -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: all commands exit 0 and Zensical reports `No issues found`.

- [ ] **Step 6: Commit**

```bash
git add README.md content/course-map.md docs/curriculum/part-05-dependencies.md \
  mkdocs.yml scripts/check_site.py tests
git commit -m "docs: publish chapter 20 fundamental theorem"
```

### Task 9: Audit and run the full quality gate

**Files:**

- Create: `docs/reviews/2026-07-29-chapter-20-consistency-review.md`

- [ ] **Step 1: Count and inspect the delivered contracts**

Run:

```bash
rg -c '\{#pr-u-05-20-' content/chapters/chapter-20/u-05-20-*.md
rg -F -c '??? note "答案"' content/chapters/chapter-20/u-05-20-*.md
rg -n 'id="(thm-u-05-20-02-ftc-part-one-pointwise|thm-u-05-20-03-newton-leibniz-continuous|thm-u-05-20-05-reflection-symmetry)"' \
  site/chapters/chapter-20
```

Expected minimum exercise counts: `6, 6, 6, 8, 12`; minimum answer counts: `8, 8, 8, 10, 14`; all three rendered anchors are present.

- [ ] **Step 2: Write the consistency review**

Record:

- accumulation continuity comes only from boundedness, additivity, and the integral estimate;
- FTC Part I uses pointwise continuity and treats endpoint one-sided derivatives;
- jump and single-point examples do not claim continuity is necessary;
- the two Newton–Leibniz proof levels and their different assumptions;
- substitution does not incorrectly require monotonicity, while inverse use checks branches;
- finite-piece rules preserve global continuity;
- Unit 20.5 has 12 mixed exercises, 14 answers, and the required diagnosis density;
- 5 units, `5.25+2.75=8` hours, at least 38 exercises and 48 answers;
- 87 published units, 23-unit Part V plan, and Chapter 20 release boundary;
- Chapter 21 has not started;
- exact final test and build evidence.

If the audit finds any high- or medium-priority issue, fix it and rerun the affected focused gates before
recording the review as passed.

- [ ] **Step 3: Run fresh full verification before the review commit**

```bash
make verify
git diff --check
git status --short
```

Expected: all tests pass, content/site validators pass, strict build has no issues, and only the review file is uncommitted.

- [ ] **Step 4: Commit the review and verify again**

```bash
git add docs/reviews/2026-07-29-chapter-20-consistency-review.md
git commit -m "docs: verify chapter 20 consistency"
make verify
git diff --check
git status --short
```

Expected: the feature worktree is clean and all quality gates pass.

- [ ] **Step 5: Hand off the verified branch**

Report the final commit, test count, content/build/site gate results, unit/hour/exercise totals, and the Chapter 21 stop point. Then use `superpowers:finishing-a-development-branch` to let the user choose local merge, pull request, preservation, or discard; do not merge or push without the selected authorization.
