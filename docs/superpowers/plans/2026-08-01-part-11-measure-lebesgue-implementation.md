# Part XI Measure and Lebesgue Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Part XI as 25 rigorous self-study units that construct Lebesgue measure from interval length, build measurable functions and the Lebesgue integral, prove MCT, Fatou, and DCT, and explain the exact boundary of Riemann integration.

**Architecture:** Implement one dependency-closed chapter at a time, beginning with a locked curriculum registry and the shared rational-enumeration motivation. Keep the proof chain one-way: outer measure → measurable sets → measurable functions → integral → convergence theorems. Put the two finite, explicitly non-certifying computations in one `src/mathbook_examples/lebesgue_approximation.py` source.

**Tech Stack:** Python 3.12 standard library, frozen dataclasses, `unittest`, Markdown with Zensical/MkDocs, MathJax, PyYAML-backed metadata tests, `scripts/check_content.py`, `scripts/check_site.py`, and `make verify`.

---

## Locked curriculum registry

```python
PART_11_UNITS = [
    ("u-11-46-01", "区间长度应满足哪些基本性质？", 1.25, 0.00, "interval-length-axioms"),
    ("u-11-46-02", "可数区间覆盖怎样定义 Lebesgue 外测度？", 1.25, 0.25, "outer-measure-definition"),
    ("u-11-46-03", "外测度为何单调并满足可数次可加性？", 1.25, 0.25, "outer-measure-properties"),
    ("u-11-46-04", "区间的外测度为何恰好等于区间长度？", 1.25, 0.50, "interval-outer-measure"),
    ("u-11-46-05", "可数集为何是零测集，Jordan 理论的边界在哪里？", 1.00, 0.50, "null-countable-sets"),
    ("u-11-47-01", "为什么集合运算必须对可数过程封闭？", 1.25, 0.25, "sigma-algebras"),
    ("u-11-47-02", "Carathéodory 判据怎样定义可测集合？", 1.50, 0.25, "caratheodory-criterion"),
    ("u-11-47-03", "可测集合为何构成 σ-代数？", 1.50, 0.25, "measurable-sigma-algebra"),
    ("u-11-47-04", "外测度在可测集上为何成为可数可加的测度？", 1.25, 0.25, "countable-additivity"),
    ("u-11-47-05", "Borel 集、零测集及其子集怎样进入 Lebesgue 可测世界？", 1.00, 0.50, "borel-lebesgue-completion"),
    ("u-11-48-01", "可测函数为何可由水平集的可测性刻画？", 1.25, 0.25, "measurable-functions"),
    ("u-11-48-02", "运算、上确界与逐点极限怎样保持可测性？", 1.25, 0.25, "measurable-operations-limits"),
    ("u-11-48-03", "非负可测函数怎样由递增简单函数逼近？", 1.50, 0.50, "simple-function-approximation"),
    ("u-11-48-04", "逐点、一致与几乎处处收敛怎样区分？", 1.00, 0.25, "pointwise-uniform-ae"),
    ("u-11-48-05", "依测度收敛与其他收敛方式有什么关系？", 1.00, 0.25, "convergence-in-measure"),
    ("u-11-49-01", "简单函数的积分怎样由水平集测度定义？", 1.25, 0.50, "simple-function-integral"),
    ("u-11-49-02", "非负可测函数的积分怎样由下逼近定义？", 1.50, 0.25, "nonnegative-integral"),
    ("u-11-49-03", "积分的单调性、齐次性与可加性怎样证明？", 1.50, 0.25, "integral-properties"),
    ("u-11-49-04", "正部、负部怎样定义一般函数的积分？", 1.25, 0.25, "signed-integral"),
    ("u-11-49-05", "绝对可积、零测集修改与积分估计怎样统一？", 1.00, 0.25, "absolute-integrability"),
    ("u-11-50-01", "单调收敛定理怎样闭合递增逼近？", 1.25, 0.25, "monotone-convergence"),
    ("u-11-50-02", "Fatou 引理怎样给出下极限不等式？", 1.25, 0.00, "fatou-lemma"),
    ("u-11-50-03", "控制收敛定理为何需要可积控制函数？", 1.50, 0.25, "dominated-convergence"),
    ("u-11-50-04", "Riemann 可积函数与 Lebesgue 积分怎样兼容？", 1.25, 0.25, "riemann-lebesgue-comparison"),
    ("u-11-50-05", "序章失败序列怎样被新理论完整解释？", 0.75, 0.25, "motivation-closure"),
]
```

Locked totals: 25 units, 31 theory hours, 7 application hours, and 38 hours. The completed book totals become 234 core units and 405 core hours. Every unit contains exactly 10 anchored formal exercises and at least 12 collapsed answers, including immediate checks. No Part XII page or navigation entry is created.

## File map

### Create

- `docs/curriculum/part-11-dependencies.md` — all unit prerequisites, unique outputs, proof order, hours, scope, and release state.
- `content/chapters/chapter-46/` through `content/chapters/chapter-50/` — five guides and 25 unit pages.
- `tests/test_chapter_46.py` through `tests/test_chapter_50.py` — metadata, proof, counterexample, exercise, answer, and scope contracts.
- `src/mathbook_examples/lebesgue_approximation.py` — the sole finite simple-integral and cover-upper-bound implementation.
- `tests/test_lebesgue_approximation.py` — exact values, interval merging, frozen result, overflow, and invalid-input tests.
- `tests/test_part_11_consistency.py` — totals, dependencies, motivation recovery, publication, scope, and unique-source contracts.
- `docs/reviews/2026-08-01-chapter-46-consistency-review.md` through `docs/reviews/2026-08-01-chapter-50-consistency-review.md`.
- `docs/reviews/2026-08-01-part-11-consistency-review.md`.

### Modify

- `content/course-map.md` — record the locked blueprint, then advance chapter status after each gate.
- `mkdocs.yml` — publish only the chapter reached at the current checkpoint.
- `README.md` — advance the release boundary and totals only after a chapter gate passes.
- `tests/test_mkdocs_site.py`, `tests/test_zensical_structure.py`, and `scripts/check_site.py` — add representative Part XI rendered anchors and final navigation.
- `docs/curriculum/part-05-dependencies.md`, `part-06-dependencies.md`, `part-08-dependencies.md`, and `part-10-dependencies.md` — replace future handoffs with precise published interfaces at final closure.
- `tests/test_part_10_consistency.py` — replace the historical “Part XI absent” assertion with a Part X snapshot assertion that permits the newly published neighbor.

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

Every core proof uses `### 障碍`, `### 证明路线`, `### 逐步证明`, `### 假设用在何处`, and `### 失败边界`. Computational material additionally uses the existing seven algorithm headings. Python outputs must say `finite_cover_only` or otherwise state that finite computation is not a measure-theoretic certificate.

## Task 1: Lock the Part XI blueprint

**Files:**
- Create: `tests/test_part_11_consistency.py`
- Create: `docs/curriculum/part-11-dependencies.md`
- Modify: `content/course-map.md`
- Modify: `tests/test_part_10_consistency.py`

- [ ] **Step 1: Write the failing Part XI registry test**

Create `tests/test_part_11_consistency.py` with `PART_11_UNITS` above and this exact structural core:

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs/curriculum/part-11-dependencies.md"
COURSE_MAP = ROOT / "content/course-map.md"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

class PartElevenConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_locked_part_totals(self):
        theory = sum(row[2] for row in PART_11_UNITS)
        applied = sum(row[3] for row in PART_11_UNITS)
        self.assertEqual((25, 31.0, 7.0, 38.0),
                         (len(PART_11_UNITS), theory, applied, theory + applied))

    def test_blueprint_starts_after_part_ten(self):
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 45 章", text)
        self.assertIn("25 个核心单元、38 学时", text)
        self.assertNotIn("chapters/chapter-46/", NAVIGATION)

    def test_part_twelve_is_not_created(self):
        self.assertFalse((ROOT / "content/chapters/chapter-51").exists())
        self.assertNotIn("chapters/chapter-51/", NAVIGATION)
```

- [ ] **Step 2: Run red**

Run: `python3.12 -m unittest tests.test_part_11_consistency -v`

Expected: FAIL because `docs/curriculum/part-11-dependencies.md` is absent.

- [ ] **Step 3: Add the dependency registry and planned map**

Create all 25 rows with exact direct prerequisites and unique outputs. Record the rational-enumeration sequence, outer-measure-to-DCT proof chain, 38-hour cap, the two finite-computation contracts, and Part XII exclusion. Add Chapters 46–50 to `content/course-map.md` as planned; do not create pages or navigation.

- [ ] **Step 4: Remove only the stale neighbor lock from Part X**

Replace `test_part_eleven_is_not_created` in `tests/test_part_10_consistency.py` with assertions that Chapter 45 still has exactly five Part X pages and remains before any Part XI navigation. Do not change Part X historical totals.

- [ ] **Step 5: Run green and commit**

```bash
python3.12 -m unittest tests.test_part_10_consistency tests.test_part_11_consistency -v
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
git add tests/test_part_10_consistency.py tests/test_part_11_consistency.py docs/curriculum/part-11-dependencies.md content/course-map.md
git commit -m "docs: lock part 11 curriculum blueprint"
```

Expected: all checks pass; the published site still stops at Chapter 45.

## Task 2: Implement the finite computation source and publish Chapter 46

**Files:**
- Create: `tests/test_lebesgue_approximation.py`
- Create: `src/mathbook_examples/lebesgue_approximation.py`
- Create: `tests/test_chapter_46.py`
- Create: `content/chapters/chapter-46/index.md`
- Create: five Chapter 46 unit files named from the registry slugs
- Create: `docs/reviews/2026-08-01-chapter-46-consistency-review.md`
- Modify: `docs/curriculum/part-11-dependencies.md`, `content/course-map.md`, `mkdocs.yml`, `README.md`, `tests/test_zensical_structure.py`

- [ ] **Step 1: Write failing computation tests**

Cover these exact cases:

```python
self.assertEqual(simple_integral([2, -1], [0.5, 3]), -2.0)
result = finite_cover_upper_bound([(0, 1), (0.5, 2), (3, 4)])
self.assertEqual(result.upper_bound, 3.0)
self.assertEqual(result.merged_intervals, ((0.0, 2.0), (3.0, 4.0)))
self.assertEqual(result.status, "finite_cover_only")
```

Reject booleans, strings, empty sequences, unequal lengths, negative measures, reversed intervals, nonfinite inputs, nonfinite products, and overflowing sums. Assert the result dataclass is frozen.

- [ ] **Step 2: Run red**

Run: `python3.12 -m unittest tests.test_lebesgue_approximation -v`

Expected: ERROR because the module does not exist.

- [ ] **Step 3: Implement the minimal finite source**

Use `math.fsum`, `math.isfinite`, a frozen `FiniteCoverResult`, sorted interval merging, and stage-specific `ValueError` messages. The module docstring and result status must state that it does not compute or certify outer measure.

- [ ] **Step 4: Write the failing Chapter 46 content contract**

Lock exact metadata from the registry, the nine shared headings, 50 exercises, at least 60 answers, and these proof markers:

```python
MARKERS = {
    "u-11-46-01": ("平移不变", "有限可加", "区间长度"),
    "u-11-46-02": ("可数开区间覆盖", "下确界", "外测度"),
    "u-11-46-03": ("单调性", "可数次可加性", "epsilon/2^n"),
    "u-11-46-04": ("有限子覆盖", "紧致性", "区间长度"),
    "u-11-46-05": ("可数集", "零测集", "Jordan"),
}
```

Also assert the Part XI introduction contains `f_n`, `q_n`, `Riemann`, and the four motivating questions, but does not use MCT as an already-proved result.

- [ ] **Step 5: Write and publish Chapter 46**

Prove both interval outer-measure inequalities. In the lower bound, enlarge a countable cover slightly, extract a finite subcover of the compact interval, and prove finite-cover length domination rather than citing it. Use the finite-cover source only in the application unit and label its output as an upper bound.

Advance totals to 214 units and 374.5 hours. Publish only Chapter 46.

- [ ] **Step 6: Verify, review, and commit**

```bash
python3.12 -m unittest tests.test_lebesgue_approximation tests.test_chapter_46 tests.test_part_11_consistency -v
make verify
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
git add src/mathbook_examples/lebesgue_approximation.py tests/test_lebesgue_approximation.py tests/test_chapter_46.py content/chapters/chapter-46 docs/reviews/2026-08-01-chapter-46-consistency-review.md docs/curriculum/part-11-dependencies.md content/course-map.md mkdocs.yml README.md tests/test_zensical_structure.py
git commit -m "docs: publish chapter 46 outer measure"
```

## Task 3: Publish Chapter 47

**Files:** Create Chapter 47 guide, five units, `tests/test_chapter_47.py`, and its review; modify the shared publication surfaces.

- [ ] **Step 1: Write the failing Chapter 47 contract**

Lock 50 exercises, at least 60 answers, exact metadata, and markers for `σ-代数`, arbitrary-test-set Carathéodory splitting, complement and countable-union closure, finite-to-countable additivity, interval/open-set measurability, Borel versus Lebesgue σ-algebras, and completeness. Forbid general extension-theorem claims.

- [ ] **Step 2: Run red**

Run: `python3.12 -m unittest tests.test_chapter_47 -v`

Expected: FAIL because Chapter 47 is absent.

- [ ] **Step 3: Write the guide and units**

Prove the Carathéodory class is a σ-algebra with all limiting steps explicit. Prove countable additivity by finite splitting followed by continuity from below derived in place. Prove intervals and open sets measurable before naming the Borel σ-algebra. Prove every subset of a null set is measurable.

- [ ] **Step 4: Publish, verify, review, and commit**

Advance totals to 219 units and 382.5 hours. Publish only through Chapter 47. Run the focused chapter tests and full five gates, then commit with `docs: publish chapter 47 measurable sets`.

## Task 4: Publish Chapter 48

**Files:** Create Chapter 48 guide, five units, `tests/test_chapter_48.py`, and its review; modify the shared publication surfaces.

- [ ] **Step 1: Write the failing Chapter 48 contract**

Lock exact metadata, 50 exercises, at least 60 answers, equivalent level-set tests, closure under arithmetic and countable suprema, and the explicit approximation

```text
phi_n(x) = 2^(-n) floor(2^n f(x)) for f(x) < n,
phi_n(x) = n for f(x) >= n.
```

Require proofs of measurability, monotonicity, and pointwise convergence after resolving boundary conventions. Lock pointwise/uniform/a.e./in-measure definitions, the finite-measure hypothesis for a.e. ⇒ in measure, and stable counterexamples to invalid converses.

- [ ] **Step 2: Run red, write the five units, and keep dependencies one-way**

Do not use Lebesgue integration, MCT, Fatou, DCT, Egorov, Riesz subsequence theorems, or `L^p` language in the proof core.

- [ ] **Step 3: Publish, verify, review, and commit**

Advance totals to 224 units and 390 hours. Publish only through Chapter 48. Run focused and full gates, then commit with `docs: publish chapter 48 measurable functions`.

## Task 5: Publish Chapter 49

**Files:** Create Chapter 49 guide, five units, `tests/test_chapter_49.py`, and its review; modify the shared publication surfaces.

- [ ] **Step 1: Write the failing Chapter 49 contract**

Lock exact metadata, 50 exercises, at least 60 answers, representation independence for simple integrals, the supremum definition for nonnegative integrals, extended-real cases, positive/negative parts, absolute integrability, null-set modification, and `|∫f| ≤ ∫|f|`. Require the imported `simple_integral` source exactly once and forbid copied implementations.

- [ ] **Step 2: Lock the anti-circular proof contract**

The test must require the phrase `递增简单函数引理` in Unit 49-03 and forbid references to `u-11-50-01` or “由单调收敛定理” in its proof core. The chapter may prove the restricted lemma for simple approximants, but may not assume the general MCT it prepares.

- [ ] **Step 3: Run red and write the five units**

Show simple-integral representation independence by common refinement. Define the nonnegative integral as a supremum. Prove additivity from the restricted increasing-simple lemma, then define signed integrals only when at least one of the positive/negative parts is finite. Reject every appearance of an `∞-∞` value.

- [ ] **Step 4: Publish, verify, review, and commit**

Advance totals to 229 units and 398 hours. Publish only through Chapter 49. Run focused and full gates, then commit with `docs: publish chapter 49 lebesgue integral`.

## Task 6: Publish Chapter 50

**Files:** Create Chapter 50 guide, five units, `tests/test_chapter_50.py`, and its review; modify the shared publication surfaces and rendered-site checks.

- [ ] **Step 1: Write the failing Chapter 50 contract**

Lock exact metadata, 50 exercises, at least 60 answers, and these theorem contracts:

```python
THEOREMS = {
    "u-11-50-01": ("非负可测", "递增", "逐点", "积分极限"),
    "u-11-50-02": ("非负可测", "下极限", "不等式", "Fatou"),
    "u-11-50-03": ("几乎处处收敛", "可积控制函数", "绝对值", "控制收敛"),
    "u-11-50-04": ("Riemann 可积", "不连续点集", "零测集", "积分相同"),
    "u-11-50-05": ("有理数枚举", "单调收敛", "积分为 0", "Riemann 失效"),
}
```

Require a named failure example for every missing hypothesis. Forbid product measure, Tonelli, Lebesgue Fubini, `L^p`, and Fourier results in proof cores.

- [ ] **Step 2: Run red and write MCT, Fatou, and DCT without circularity**

Prove MCT from the nonnegative integral definition and simple lower tests. Derive Fatou by applying MCT to tail infima. Derive DCT by applying Fatou to `g+f_n` and `g-f_n`, with all integrability checks explicit.

- [ ] **Step 3: Prove the one-dimensional Riemann comparison**

Prove equality of integrals through Darboux step functions. Prove the bounded Riemann-integrability Lebesgue criterion using oscillation sets and interval covers only; do not invoke product measure or Fubini–Tonelli.

- [ ] **Step 4: Close the introduction and publish**

Return to `f_n = 1_{q_1,...,q_n}` and identify exactly where Chapters 46–50 answer the four opening questions. Advance totals to 234 units and 405 hours. Add representative Part XI page and anchor checks to `tests/test_mkdocs_site.py`, `tests/test_zensical_structure.py`, and `scripts/check_site.py`. Keep Chapter 51 absent.

- [ ] **Step 5: Verify, review, and commit**

Run focused Chapter 50 and Part XI tests, then all five gates. Commit with `docs: publish chapter 50 convergence theorems`.

## Task 7: Close Part XI cross-chapter and cross-part consistency

**Files:**
- Create: `docs/reviews/2026-08-01-part-11-consistency-review.md`
- Modify: `tests/test_part_11_consistency.py`
- Modify: `docs/curriculum/part-05-dependencies.md`, `part-06-dependencies.md`, `part-08-dependencies.md`, `part-10-dependencies.md`, `part-11-dependencies.md`
- Modify: `README.md`, `content/course-map.md`, `mkdocs.yml`, `tests/test_mkdocs_site.py`, `tests/test_zensical_structure.py`, `scripts/check_site.py`

- [ ] **Step 1: Expand the final consistency test**

Assert 25 unique pages, 234 units, 405 hours, exact dependency rows, exact navigation order, exactly one implementation of each public computation, no Chapter 51, five chapter reviews, and one final review. Assert that the opening sequence is mentioned in the Part XI introduction and every chapter, with no premature theorem use.

- [ ] **Step 2: Audit all critical proofs line by line**

Record checks for interval outer-measure equality; Carathéodory σ-algebra closure; countable additivity; simple approximation; representation independence; the restricted simple lemma; MCT/Fatou/DCT; the one-dimensional Riemann criterion; and every counterexample calculation. A machine marker is not proof of correctness.

- [ ] **Step 3: Update cross-part handoffs**

Record the exact units consuming Riemann integrability, uniform convergence, Jordan limitations, and parameter-integral boundaries. Keep Part XII as a future consumer, not a prerequisite or published surface.

- [ ] **Step 4: Run the complete release audit**

```bash
make verify
python3.12 scripts/check_content.py
zensical build --strict
python3.12 scripts/check_site.py
git diff --check
git status --short
```

Expected: 0 failures; 25 Part XI pages; final totals 234 units and 405 hours; release boundary Chapter 50; only known pre-existing ignored build artifacts may remain; Chapter 51 does not exist.

- [ ] **Step 5: Commit closure**

```bash
git add README.md content/course-map.md mkdocs.yml scripts/check_site.py tests docs/curriculum docs/reviews/2026-08-01-part-11-consistency-review.md
git commit -m "docs: close part 11 consistency audit"
```

## Plan self-review

- Every design requirement maps to a task: construction (Tasks 2–3), functions and convergence modes (Task 4), integral (Task 5), convergence theorems and Riemann comparison (Task 6), and publication closure (Task 7).
- The Chapter 49 restricted-simple lemma prevents circular dependence on Chapter 50 MCT.
- The Riemann criterion is explicitly one-dimensional and cannot borrow product measure.
- Both numerical interfaces are finite and non-certifying by name, result status, tests, and page language.
- Historical Part X totals remain frozen while its stale future-neighbor assertion is scoped away.
- No placeholder steps, future Part XII pages, or out-of-scope theorem implementations remain.
