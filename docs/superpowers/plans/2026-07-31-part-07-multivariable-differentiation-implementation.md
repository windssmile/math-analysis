# Part VII Multivariable Differentiation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Part VII as 25 self-study units covering finite-dimensional Euclid spaces, Fréchet differentiation, multivariable Taylor theory, inverse and implicit functions, and equality-constrained optimization, with three tested computational units.

**Architecture:** Implement one chapter at a time behind a locked chapter contract. Each chapter adds its content pages, navigation, publication metadata, dependency map entries, tests, and consistency review before the next chapter begins. Computational examples live in three focused modules under `src/mathbook_examples/`; chapter pages import those modules instead of copying algorithms.

**Tech Stack:** Python 3.12 standard library, `unittest`, PyYAML, Markdown with Zensical/MkDocs, MathJax, existing `scripts/check_content.py`, `scripts/check_site.py`, and `make verify`.

---

## Locked curriculum registry

```python
PART_07_UNITS = [
    ("u-07-28-01", "向量、内积、范数和距离怎样描述多维几何？", 1.25, 0.50, "euclidean-geometry", 8, 10),
    ("u-07-28-02", "邻域、开集、闭集、内部与边界怎样组织局部和整体？", 1.50, 0.25, "open-closed-sets", 8, 10),
    ("u-07-28-03", "向量序列怎样收敛，有限维空间为什么完备？", 1.50, 0.25, "sequences-completeness", 9, 11),
    ("u-07-28-04", "紧致性为什么等价于闭且有界？", 1.50, 0.25, "compactness", 9, 11),
    ("u-07-28-05", "多元极限、连续与连通性怎样给出存在性结论？", 1.50, 0.50, "limits-continuity", 10, 12),
    ("u-07-29-01", "偏导数和方向导数能否保证函数可微？", 1.25, 0.25, "partial-directional", 8, 10),
    ("u-07-29-02", "Fréchet 微分怎样刻画最佳线性近似？", 1.50, 0.25, "frechet-derivative", 9, 11),
    ("u-07-29-03", "连续偏导为什么足以推出可微？", 1.50, 0.25, "continuous-partials", 9, 11),
    ("u-07-29-04", "导数映射怎样满足代数规则和链式法则？", 1.50, 0.25, "chain-rule", 9, 11),
    ("u-07-29-05", "Jacobian、梯度与条件数怎样描述敏感性？", 1.25, 0.50, "jacobian-conditioning", 10, 12),
    ("u-07-29-06", "怎样计算并可靠核验多元线性化？", 0.75, 0.75, "linearization-check", 12, 15),
    ("u-07-30-01", "二阶微分和 Hessian 为什么是双线性对象？", 1.50, 0.25, "second-derivative", 9, 11),
    ("u-07-30-02", "高阶微分和多重指标怎样组织混合偏导？", 1.25, 0.25, "higher-derivatives", 8, 10),
    ("u-07-30-03", "多元 Taylor 公式怎样给出可证明的余项？", 1.50, 0.25, "multivariable-taylor", 10, 12),
    ("u-07-30-04", "二次模型怎样支持误差界和敏感性分析？", 1.25, 0.75, "quadratic-models", 11, 14),
    ("u-07-31-01", "Jacobian 可逆怎样产生局部反函数？", 1.50, 0.25, "inverse-function", 9, 11),
    ("u-07-31-02", "隐式方程什么时候能局部解出变量？", 1.50, 0.25, "implicit-function", 10, 12),
    ("u-07-31-03", "局部参数化怎样给出灵敏度并区分分支？", 1.25, 0.50, "local-parameterization", 9, 11),
    ("u-07-31-04", "Newton 法怎样可靠求解非线性方程组？", 1.00, 0.75, "newton-systems", 12, 15),
    ("u-07-32-01", "多元极值什么时候存在，模型定义域怎样影响答案？", 1.25, 0.25, "extrema-existence", 8, 10),
    ("u-07-32-02", "无约束极值为什么满足一阶必要条件？", 1.50, 0.25, "first-order-extrema", 9, 11),
    ("u-07-32-03", "Hessian 怎样给出二阶必要与充分条件？", 1.50, 0.25, "second-order-tests", 10, 12),
    ("u-07-32-04", "Lagrange 乘子怎样处理正则等式约束？", 1.50, 0.50, "lagrange-multipliers", 10, 12),
    ("u-07-32-05", "多个约束、几何解释和异常点怎样处理？", 1.25, 0.50, "multiple-constraints", 10, 12),
    ("u-07-32-06", "梯度法、Newton 法和约束候选怎样可靠核验？", 1.00, 1.25, "optimization-check", 13, 16),
]
```

Locked totals: 25 units, 33.75 theory hours, 10.25 application hours, 44 hours,
239 anchored exercises, and 293 collapsed answers.

## File map

### Create

- `docs/curriculum/part-07-dependencies.md` — direct prerequisites, unique outputs, hours, and release boundary.
- `content/chapters/chapter-28/` through `content/chapters/chapter-32/` — five guides and 25 unit pages.
- `tests/test_chapter_28.py` through `tests/test_chapter_32.py` — locked metadata, proof, boundary, training, and publication contracts.
- `src/mathbook_examples/multivariate.py` and `tests/test_multivariate.py` — Jacobian and linearization diagnostics.
- `src/mathbook_examples/nonlinear.py` and `tests/test_nonlinear.py` — Newton iteration for nonlinear systems.
- `src/mathbook_examples/optimization.py` and `tests/test_optimization.py` — gradient/Newton optimization and equality-constraint candidate checks.
- `tests/test_part_07_consistency.py` — final dependency, totals, scope, navigation, and algorithm-source contracts.
- `docs/reviews/2026-07-31-chapter-28-consistency-review.md` through `docs/reviews/2026-07-31-chapter-32-consistency-review.md`.
- `docs/reviews/2026-07-31-part-07-consistency-review.md`.

### Modify

- `mkdocs.yml` — append only published Part VII chapters; never add Chapter 33.
- `content/course-map.md` — add the locked blueprint, then mark chapters published one checkpoint at a time.
- `README.md` — advance the visible boundary and unit count after each completed chapter.
- `src/mathbook_examples/__init__.py` — retain the package marker; do not re-export APIs.

## Shared content contract

Every Part VII unit uses `content_standard: 2`, includes its stable unit anchor, at least two anchored
examples, at least two immediate checks, the exact exercise and answer counts in the registry, and
these headings in order:

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

Each computational unit additionally uses:

```markdown
### 问题来源
### 数学转化
### 算法思想
### 误差与适用条件
### 伪代码
### Python
### 结果解释
```

## Task 1: Lock the Part VII blueprint

**Files:**
- Create: `docs/curriculum/part-07-dependencies.md`
- Create: `tests/test_part_07_consistency.py`
- Modify: `content/course-map.md`

- [ ] **Step 1: Write the failing blueprint test**

Create `tests/test_part_07_consistency.py` with a `PART_07_UNITS` copy of the locked registry and
assert:

```python
def test_locked_part_totals(self):
    theory = sum(unit[2] for unit in PART_07_UNITS)
    applied = sum(unit[3] for unit in PART_07_UNITS)
    self.assertEqual((25, 33.75, 10.25, 44.0), (
        len(PART_07_UNITS), theory, applied, theory + applied
    ))

def test_blueprint_stops_before_part_eight(self):
    text = DEPENDENCIES.read_text(encoding="utf-8")
    self.assertIn("当前发布边界：第 27 章", text)
    self.assertIn("25 个核心单元、44 学时", text)
    self.assertNotIn("chapter-33", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
```

- [ ] **Step 2: Run the test and verify the missing dependency map fails**

Run: `python3.12 -m unittest tests.test_part_07_consistency -v`

Expected: FAIL because `docs/curriculum/part-07-dependencies.md` does not exist.

- [ ] **Step 3: Write the dependency map and course blueprint**

Create the dependency map with all 25 IDs, direct prerequisites, unique outputs, the five chapter
totals, and the explicit boundary “当前发布边界：第 27 章”. Add a Part VII blueprint to
`content/course-map.md`; label all five chapters “规划中” and do not create navigation or unit pages.

- [ ] **Step 4: Run the focused and baseline gates**

Run:

```bash
python3.12 -m unittest tests.test_part_07_consistency -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: all commands exit 0; the published site still stops at Chapter 27.

- [ ] **Step 5: Commit the blueprint**

```bash
git add docs/curriculum/part-07-dependencies.md content/course-map.md tests/test_part_07_consistency.py
git commit -m "docs: lock part 07 curriculum blueprint"
```

## Task 2: Publish Chapter 28

**Files:**
- Create: `content/chapters/chapter-28/index.md`
- Create: `content/chapters/chapter-28/u-07-28-01-euclidean-geometry.md`
- Create: `content/chapters/chapter-28/u-07-28-02-open-closed-sets.md`
- Create: `content/chapters/chapter-28/u-07-28-03-sequences-completeness.md`
- Create: `content/chapters/chapter-28/u-07-28-04-compactness.md`
- Create: `content/chapters/chapter-28/u-07-28-05-limits-continuity.md`
- Create: `tests/test_chapter_28.py`
- Create: `docs/reviews/2026-07-31-chapter-28-consistency-review.md`
- Modify: `docs/curriculum/part-07-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`

- [ ] **Step 1: Write the failing chapter contract**

In `tests/test_chapter_28.py`, copy the five Chapter 28 registry rows and assert exact metadata,
training counts, one occurrence of every unit link in the guide, and these anchors:

```python
REQUIRED_ANCHORS = {
    "u-07-28-01": ("thm-u-07-28-01-cauchy-schwarz", "thm-u-07-28-01-norm-equivalence"),
    "u-07-28-02": ("def-u-07-28-02-open-closed", "thm-u-07-28-02-sequential-closed"),
    "u-07-28-03": ("thm-u-07-28-03-coordinate-convergence", "thm-u-07-28-03-completeness"),
    "u-07-28-04": ("thm-u-07-28-04-bolzano-weierstrass", "thm-u-07-28-04-heine-borel"),
    "u-07-28-05": ("def-u-07-28-05-multivariable-limit", "thm-u-07-28-05-continuous-image-connected"),
}
```

Also assert that 28.5 contains “有限条路径不能证明极限存在”, and 28.4 contains
“有限维” and “不能无条件推广到无限维”.

- [ ] **Step 2: Run the contract and verify it fails**

Run: `python3.12 -m unittest tests.test_chapter_28 -v`

Expected: FAIL because `content/chapters/chapter-28/` is absent.

- [ ] **Step 3: Write the guide and five units**

Follow the shared content contract and the exact registry. Prove Cauchy–Schwarz, finite-dimensional
norm equivalence, sequential closedness, coordinate completeness, Bolzano–Weierstrass,
Heine–Borel, compact-image consequences, and connected-image preservation. Include counterexamples
for path-dependent limits and for the insufficiency of finitely many successful paths.

- [ ] **Step 4: Publish only Chapter 28**

Add Part VII and Chapter 28 to `mkdocs.yml`; update the release boundary to Chapter 28, 127 total
units, and 238 total published hours where displayed. Mark Chapter 28 published in the course map
and leave Chapters 29–32 as planned.

- [ ] **Step 5: Run all chapter gates**

Run:

```bash
python3.12 -m unittest tests.test_chapter_28 tests.test_part_07_consistency -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
```

Expected: all commands exit 0; rendered navigation stops at Chapter 28.

- [ ] **Step 6: Write the review and commit**

Record proof coverage, counterexample coverage, hours, navigation, and the Chapter 29 boundary in
the review. Then run `git diff --check` and commit:

```bash
git add content/chapters/chapter-28 docs/curriculum/part-07-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_chapter_28.py tests/test_part_07_consistency.py docs/reviews/2026-07-31-chapter-28-consistency-review.md
git commit -m "docs: publish chapter 28 euclidean spaces"
```

## Task 3: Publish Chapter 29 and the Jacobian checker

**Files:**
- Create: `content/chapters/chapter-29/index.md`
- Create: six Chapter 29 unit files using the locked slugs
- Create: `tests/test_chapter_29.py`
- Create: `src/mathbook_examples/multivariate.py`
- Create: `tests/test_multivariate.py`
- Create: `docs/reviews/2026-07-31-chapter-29-consistency-review.md`
- Modify: `docs/curriculum/part-07-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`

- [ ] **Step 1: Write failing numerical API tests**

Define the intended immutable result in the test:

```python
@dataclass(frozen=True)
class JacobianCheck:
    analytic: tuple[tuple[float, ...], ...]
    finite_difference: tuple[tuple[float, ...], ...]
    max_abs_difference: float
    step: float
    condition_estimate: float | None
    status: str
    assumptions: tuple[str, ...]
```

Test `check_jacobian(function, jacobian, point, *, step=1e-6)` on
\(F(x,y)=(x^2+y,xy)\), requiring the expected \(2\times2\) Jacobian within `1e-5`. Test nonfinite
points, nonpositive steps, output-dimension drift, malformed matrices, nonfinite values, and singular
matrices. Required statuses are `checked`, `singular`, and `ill_conditioned`; invalid arguments raise
`ValueError` with a stable field-specific message.

- [ ] **Step 2: Run and verify the missing module fails**

Run: `python3.12 -m unittest tests.test_multivariate -v`

Expected: ERROR with `ModuleNotFoundError: mathbook_examples.multivariate`.

- [ ] **Step 3: Implement the minimal Jacobian checker**

Implement central finite differences, tuple normalization, finite-value validation, infinity matrix
norm, and a pivoted Gaussian-elimination inverse used only for a finite-dimensional condition
estimate. Return `condition_estimate=None` for singular matrices. Do not add NumPy or an automatic
differentiation dependency.

- [ ] **Step 4: Run the numerical tests**

Run: `python3.12 -m unittest tests.test_multivariate -v`

Expected: all tests PASS.

- [ ] **Step 5: Write the failing Chapter 29 contract**

Assert the six locked units and proof markers for:

- partial derivatives and all directional derivatives without continuity;
- the Fréchet remainder quotient;
- continuous partials as a sufficient, not necessary, condition;
- chain rule with compatible domain/codomain dimensions;
- Jacobian/gradient orientation and condition-number semantics;
- the exact seven-step computational sequence in 29.6.

Assert 29.6 imports `mathbook_examples.multivariate` and does not contain
`def check_jacobian(`.

- [ ] **Step 6: Write and publish Chapter 29**

Create the guide and six complete units. Update publication surfaces to Chapter 29, 133 total units,
and 248 total published hours. Keep Chapter 30 absent from navigation.

- [ ] **Step 7: Verify, review, and commit**

Run:

```bash
python3.12 -m unittest tests.test_multivariate tests.test_chapter_29 tests.test_part_07_consistency -v
make verify
git diff --check
```

Expected: all tests and gates exit 0. Write the Chapter 29 review, repeat the focused tests after the
review update, then commit:

```bash
git add src/mathbook_examples/multivariate.py tests/test_multivariate.py tests/test_chapter_29.py content/chapters/chapter-29 docs/curriculum/part-07-dependencies.md content/course-map.md mkdocs.yml README.md docs/reviews/2026-07-31-chapter-29-consistency-review.md
git commit -m "docs: publish chapter 29 multivariable differentiation"
```

## Task 4: Publish Chapter 30

**Files:**
- Create: `content/chapters/chapter-30/index.md`
- Create: four Chapter 30 unit files using the locked slugs
- Create: `tests/test_chapter_30.py`
- Create: `docs/reviews/2026-07-31-chapter-30-consistency-review.md`
- Modify: publication and dependency surfaces

- [ ] **Step 1: Write the failing Chapter 30 contract**

Lock the four units, training counts, and these markers:

```python
REQUIRED_MARKERS = {
    "u-07-30-01": ("双线性映射", "Hessian", "混合偏导", "连续"),
    "u-07-30-02": ("多重指标", "高阶微分", "对称多线性"),
    "u-07-30-03": ("线段完全位于定义域", "一元 Taylor", "余项"),
    "u-07-30-04": ("二次模型", "理论误差界", "敏感性", "不作极值判定"),
}
```

Forbid “Hessian 正定所以是极小值” from the Chapter 30 core sections.

- [ ] **Step 2: Run and verify absence failure**

Run: `python3.12 -m unittest tests.test_chapter_30 -v`

Expected: FAIL because Chapter 30 files are missing.

- [ ] **Step 3: Write the four units and guide**

Prove Hessian symmetry under stated continuity assumptions, introduce multi-index notation only as
needed, derive Taylor along a contained line segment, and separate a finite quadratic model from an
unproved global approximation.

- [ ] **Step 4: Publish, verify, review, and commit**

Advance publication to Chapter 30, 137 units, and 255 published hours. Run:

```bash
python3.12 -m unittest tests.test_chapter_30 tests.test_part_07_consistency -v
make verify
git diff --check
```

Expected: all gates exit 0. Write the review and commit with message
`docs: publish chapter 30 multivariable Taylor theory`.

## Task 5: Publish Chapter 31 and Newton systems

**Files:**
- Create: `content/chapters/chapter-31/index.md`
- Create: four Chapter 31 unit files using the locked slugs
- Create: `tests/test_chapter_31.py`
- Create: `src/mathbook_examples/nonlinear.py`
- Create: `tests/test_nonlinear.py`
- Create: `docs/reviews/2026-07-31-chapter-31-consistency-review.md`
- Modify: publication and dependency surfaces

- [ ] **Step 1: Write failing Newton-system tests**

Lock this immutable API:

```python
@dataclass(frozen=True)
class SystemNewtonResult:
    point: tuple[float, ...]
    converged: bool
    iterations: int
    reason: str
    residual_norm: float
    last_step_norm: float | None
    jacobian_condition: float | None
    trace: tuple[tuple[float, ...], ...]
```

Test `newton_system(function, jacobian, initial, *, residual_tolerance=1e-10,
step_tolerance=1e-10, condition_limit=1e12, max_iterations=50)` on
\(F(x,y)=(x^2+y^2-1,x-y)\). Require explicit `residual`, `step`, `singular_jacobian`,
`ill_conditioned_jacobian`, `nonfinite_value`, and `max_iterations` reasons. Validate dimensions,
finite inputs, positive finite tolerances, and a positive integer iteration budget.

- [ ] **Step 2: Verify missing-module failure**

Run: `python3.12 -m unittest tests.test_nonlinear -v`

Expected: ERROR with `ModuleNotFoundError: mathbook_examples.nonlinear`.

- [ ] **Step 3: Implement Newton systems**

Reuse focused private matrix validation and pivoted linear solving inside `nonlinear.py`; do not
import private names from `multivariate.py`. Preserve the last finite point on failure, record every
accepted iterate, and treat residual/step stops as convergence signals rather than root-error
certificates.

- [ ] **Step 4: Run numerical tests**

Run: `python3.12 -m unittest tests.test_nonlinear -v`

Expected: all tests PASS.

- [ ] **Step 5: Write the chapter contract and content**

Lock inverse-function, implicit-function, branch, sensitivity, and Newton markers. Require 31.4 to
import `mathbook_examples.nonlinear`, include the seven-step computational sequence, and avoid a
local `def newton_system(`. Prove the inverse function theorem before deriving the implicit function
theorem; distinguish local and global invertibility in both examples and exercises.

- [ ] **Step 6: Publish, verify, review, and commit**

Advance publication to Chapter 31, 141 units, and 262 published hours. Run:

```bash
python3.12 -m unittest tests.test_nonlinear tests.test_chapter_31 tests.test_part_07_consistency -v
make verify
git diff --check
```

Expected: all gates exit 0. Write the review and commit with message
`docs: publish chapter 31 implicit function theory`.

## Task 6: Publish Chapter 32 and optimization

**Files:**
- Create: `content/chapters/chapter-32/index.md`
- Create: six Chapter 32 unit files using the locked slugs
- Create: `tests/test_chapter_32.py`
- Create: `src/mathbook_examples/optimization.py`
- Create: `tests/test_optimization.py`
- Create: `docs/reviews/2026-07-31-chapter-32-consistency-review.md`
- Modify: publication and dependency surfaces

- [ ] **Step 1: Write failing optimization tests**

Lock this immutable result:

```python
@dataclass(frozen=True)
class OptimizationResult:
    point: tuple[float, ...]
    converged: bool
    iterations: int
    reason: str
    objective: float
    gradient_norm: float
    last_step_norm: float | None
    hessian_status: str | None
    trace: tuple[tuple[float, ...], ...]
```

Test `gradient_descent` and `newton_optimize` on a positive-definite quadratic. Require explicit
reasons `gradient`, `step`, `non_descent_direction`, `singular_hessian`, `indefinite_hessian`,
`nonfinite_value`, and `max_iterations`. Add
`check_equality_candidate(gradient, constraint_jacobian, point, multipliers)` returning stationarity
and constraint residuals without declaring the candidate optimal.

- [ ] **Step 2: Verify missing-module failure**

Run: `python3.12 -m unittest tests.test_optimization -v`

Expected: ERROR with `ModuleNotFoundError: mathbook_examples.optimization`.

- [ ] **Step 3: Implement minimal optimization APIs**

Use tuple vectors, Euclidean norms, backtracking for gradient descent, and a pivoted Newton step.
Reject nonfinite inputs and dimension drift. Never return an “optimal” status; `converged` means only
that a documented stopping signal fired.

- [ ] **Step 4: Run numerical tests**

Run: `python3.12 -m unittest tests.test_optimization -v`

Expected: all tests PASS.

- [ ] **Step 5: Write the Chapter 32 contract and six units**

Require:

- compact-domain existence before stationary conditions;
- first-order conditions before Hessian classification;
- semidefinite inconclusiveness examples;
- regularity checks before Lagrange multipliers;
- direct treatment of abnormal points;
- explicit exclusion of inequality constraints and general KKT theory;
- the exact computational sequence and reuse of `mathbook_examples.optimization` in 32.6.

- [ ] **Step 6: Publish, verify, review, and commit**

Advance publication to Chapter 32, 147 units, and 273 total published hours. Mark Part VII complete
at 25 units and 44 hours; do not add Chapter 33. Run:

```bash
python3.12 -m unittest tests.test_optimization tests.test_chapter_32 tests.test_part_07_consistency -v
make verify
git diff --check
```

Expected: all gates exit 0. Write the review and commit with message
`docs: publish chapter 32 multivariable optimization`.

## Task 7: Audit and close Part VII

**Files:**
- Modify: `tests/test_part_07_consistency.py`
- Create: `docs/reviews/2026-07-31-part-07-consistency-review.md`
- Modify only if the audit finds a contract violation: Part VII files listed above

- [ ] **Step 1: Extend the failing final consistency contract**

Assert all of the following:

```python
self.assertEqual(25, len(list((ROOT / "content/chapters").glob("chapter-2[89]/u-07-*.md")))
    + len(list((ROOT / "content/chapters").glob("chapter-3[0-2]/u-07-*.md"))))
self.assertNotIn("chapter-33", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
self.assertIn("第七部（第 28–32 章）已经完整发布", README)
self.assertIn("147 个学习单元", README)
```

Also assert exact 33.75/10.25/44 totals from page metadata, every algorithm page imports its unique
source, forbidden scope terms do not appear in core sections, and navigation contains each Part VII
unit exactly once.

- [ ] **Step 2: Run the final contract**

Run: `python3.12 -m unittest tests.test_part_07_consistency -v`

Expected before the audit report and final metadata update: at least one assertion FAILS.

- [ ] **Step 3: Perform the source audit**

Read all 25 units and record evidence for:

- dependency order and no forward proof use;
- all theorem hypotheses;
- counterexample boundaries;
- dimensions and map directions;
- computational source uniqueness;
- error/status semantics;
- exercise and answer coverage;
- Chapter 33 absence.

Fix each observed contract violation in its owning file and rerun its chapter test immediately.

- [ ] **Step 4: Perform the rendered audit**

Run:

```bash
zensical build --strict
python3.12 scripts/check_site.py
```

Inspect the generated pages for one proof-heavy unit and each of 29.6, 31.4, and 32.6. Verify
equations render, tables do not overflow at a narrow viewport, code imports are visible, anchors
resolve, and the sidebar stops at Chapter 32. Record the inspected paths and outcomes in the report.

- [ ] **Step 5: Run the complete verification gate**

Run:

```bash
python3.12 -m unittest discover -s tests -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
```

Expected: every command exits 0 with no failing tests or content/site errors.

- [ ] **Step 6: Commit the final audit**

```bash
git add tests/test_part_07_consistency.py docs/reviews/2026-07-31-part-07-consistency-review.md
git add content/chapters/chapter-28 content/chapters/chapter-29 content/chapters/chapter-30 content/chapters/chapter-31 content/chapters/chapter-32
git add src/mathbook_examples/multivariate.py src/mathbook_examples/nonlinear.py src/mathbook_examples/optimization.py
git add tests/test_multivariate.py tests/test_nonlinear.py tests/test_optimization.py
git add docs/curriculum/part-07-dependencies.md content/course-map.md mkdocs.yml README.md
git commit -m "docs: audit complete part 07"
```

## Execution checkpoints

Stop for review after Tasks 1–7 individually. A later task may begin only when the prior task's
focused tests, content check, strict build, site check, consistency review, and commit have all
completed. Do not push, merge, create Chapter 33, or start Part VIII without a separate user request.
