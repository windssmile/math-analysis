# Part III Self-Study Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite Part III (Chapters 9–12) as a 20-unit, 40-hour, `content_standard = 2` self-study sequence, add the non-core trigonometric-continuity appendix, and close every curriculum, navigation, render, and proof-boundary contract without starting Part IV.

**Architecture:** Keep the four existing chapter themes and all 13 existing URLs, add seven registered core pages and one unregistered optional bridge page, and make `curriculum/outline.toml` plus `curriculum/units.toml` the machine-readable source of truth. Implement chapter-by-chapter in dependency order; each chapter receives exact registry tests, mathematical boundary tests, v2 manuscript validation, navigation registration, and a green commit before the next chapter begins. Reuse the existing bisection implementation and the Part II Bolzano–Weierstrass/contraction results rather than duplicating them.

**Tech Stack:** Quarto Website, Markdown/QMD, TOML via Python 3.12 `tomllib`, Python 3.12 `unittest`, MathJax, existing `scripts/check_outline.py`, `scripts/check_units.py`, `scripts/render_curriculum_map.py`, and `scripts/check_site.py`.

---

## Execution rules

- The approved design is `docs/superpowers/specs/2026-07-23-part-03-self-study-rewrite-design.md`.
- The main agent writes and reviews the manuscript. Do not treat a subagent report as proof that a chapter is correct.
- Preserve all existing Part I and Part II QMD files unchanged.
- Do not edit or draft Part IV.
- Do not add a second bisection implementation; import or cite `src/mathbook_examples/bisection.py`.
- Keep `_site/`, `site_libs/`, and rendered HTML out of Git.
- Every core page must pass the exact `content_standard = 2` contract: required headings, at least two stable example anchors, at least five stable exercise anchors, at least seven collapsed answers, and `## 常见误区与后续`.
- Each core page must contain at least two explicit immediate checks even though the generic validator does not count them.
- After each chapter, inspect the diff personally for proof gaps, circular dependencies, undefined notation, and accidental use of Part IV tools.

## Task 1: Establish an isolated, verified execution baseline

**Files:**
- Read: `docs/superpowers/specs/2026-07-23-part-03-self-study-rewrite-design.md`
- Read: `curriculum/outline.toml`
- Read: `curriculum/units.toml`
- Read: `_quarto.yml`

- [ ] **Step 1: Confirm the starting branch and working tree**

Run:

```bash
git status --short --branch
git log -3 --oneline
```

Expected: `main` is ahead of `origin/main` by the approved design commit `6997eec`, with no uncommitted files other than this plan if the plan has not yet been committed.

- [ ] **Step 2: Create the implementation branch**

Run:

```bash
git switch -c codex/part-03-self-study-rewrite
```

Expected: Git reports a new branch named `codex/part-03-self-study-rewrite`.

- [ ] **Step 3: Run the pre-change test suite**

Run:

```bash
python3.12 -m unittest discover -s tests -v
python3.12 scripts/check_outline.py
python3.12 scripts/check_units.py
```

Expected: all tests pass; the outline reports `278+92=370`; the unit validator reports 48 registered units.

- [ ] **Step 4: Record the clean baseline**

Run:

```bash
git status --short
```

Expected: no manuscript or generated-site changes.

## Task 2: Change the authoritative hour contract from 370 to 384

**Files:**
- Modify: `tests/test_outline.py`
- Modify: `scripts/check_outline.py`
- Modify: `curriculum/outline.toml`
- Modify: `tests/test_curriculum_map.py`
- Regenerate: `book/curriculum-map.qmd`
- Modify: `curriculum/parts-02-03-dependencies.md`

- [ ] **Step 1: Write failing outline tests for the approved totals**

In `tests/test_outline.py`:

- add `test_part_three_has_closed_forty_hour_contract`, expecting `(32, 8)`;
- rename/update the whole-book hour test to expect `(290, 94, 384)`;
- update the bad-total assertions to expect the new protected totals.

Run:

```bash
python3.12 -m unittest tests.test_outline -v
```

Expected: failures show the current Part III `20+6` and whole-book `278+92=370` values.

- [ ] **Step 2: Update the validator’s immutable curriculum contract**

In `scripts/check_outline.py`:

- change the Part III expected tuple from `20, 6` to `32, 8`;
- change protected whole-book theory/applied totals from `278, 92` to `290, 94`;
- change the success message to `outline valid: 12 parts, 54 chapters, 290+94=384 hours`.

Do not alter chapter titles, order, IDs, or any other part’s hours.

- [ ] **Step 3: Update the source outline**

In `curriculum/outline.toml`:

- set book hours to `theory_hours = 290`, `applied_hours = 94`, `total_hours = 384`;
- set Part III hours to `theory_hours = 32`, `applied_hours = 8`.

- [ ] **Step 4: Make outline tests green**

Run:

```bash
python3.12 -m unittest tests.test_outline -v
python3.12 scripts/check_outline.py
```

Expected: all outline tests pass and the validator prints `290+94=384`.

- [ ] **Step 5: Update the generated-map contract before regeneration**

In `tests/test_curriculum_map.py`, change the expected map total from `278 + 92 = 370` to `290 + 94 = 384`. Leave the current 13-unit Part III count unchanged until all seven new core units have been registered.

Run:

```bash
python3.12 -m unittest tests.test_curriculum_map -v
```

Expected: failure because `book/curriculum-map.qmd` still contains the old total.

- [ ] **Step 6: Regenerate the curriculum map**

Run:

```bash
python3.12 scripts/render_curriculum_map.py
python3.12 -m unittest tests.test_curriculum_map -v
```

Expected: the map test passes and the generated header shows `290 + 94 = 384`.

- [ ] **Step 7: Rewrite the Part II → Part III dependency document**

Update `curriculum/parts-02-03-dependencies.md` to state:

- Part III has 20 core units and `32+8=40` hours;
- Chapter 9 supplies the complete function-limit type system;
- Chapter 10 supplies point, one-sided, set, and elementary-algebraic continuity;
- Chapter 11 uses sequential compactness from Part II Bolzano–Weierstrass;
- Chapter 12 distinguishes existence, interval, and contraction certificates;
- open-cover compactness is optional preview only;
- the optional trigonometric page is outside registered units and core hours;
- Part IV owns derivatives, MVT, Taylor, Newton, and convergence order.

- [ ] **Step 8: Run contract tests and commit**

Run:

```bash
python3.12 -m unittest tests.test_outline tests.test_curriculum_map -v
python3.12 scripts/check_outline.py
git diff --check
git add tests/test_outline.py scripts/check_outline.py curriculum/outline.toml tests/test_curriculum_map.py book/curriculum-map.qmd curriculum/parts-02-03-dependencies.md
git commit -m "feat: expand part three curriculum contract"
```

Expected: tests pass and the commit contains only the hour/dependency baseline.

## Task 3: Rewrite Chapter 9 as the complete function-limit foundation

**Files:**
- Modify: `tests/test_chapter_09.py`
- Modify: `curriculum/units.toml`
- Modify: `_quarto.yml`
- Rewrite: `book/part-03/chapter-09/u-03-09-01-local-neighborhoods.qmd`
- Rewrite: `book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.qmd`
- Create: `book/part-03/chapter-09/u-03-09-05-epsilon-delta-workshop.qmd`
- Create: `book/part-03/chapter-09/u-03-09-06-one-sided-limits.qmd`
- Create: `book/part-03/chapter-09/u-03-09-07-infinite-limits-at-point.qmd`
- Create: `book/part-03/chapter-09/u-03-09-08-limits-at-infinity.qmd`
- Rewrite: `book/part-03/chapter-09/u-03-09-03-function-limit-laws.qmd`
- Rewrite: `book/part-03/chapter-09/u-03-09-04-sequential-function-limits.qmd`

- [ ] **Step 1: Replace the Chapter 9 registry test with the final ordered contract**

Make `tests/test_chapter_09.py` require this exact order, title, hours, and suffix:

| ID | Title | Theory | Applied | Suffix |
|---|---|---:|---:|---|
| `u-03-09-01` | 函数在一点附近意味着什么？ | 1.50 | 0.50 | `local-neighborhoods` |
| `u-03-09-02` | “任意接近”怎样定义函数极限？ | 1.75 | 0.25 | `epsilon-delta-limit` |
| `u-03-09-05` | 极限证明怎样从目标误差反推局部范围？ | 1.50 | 0.50 | `epsilon-delta-workshop` |
| `u-03-09-06` | 左右极限怎样共同决定双侧极限？ | 1.50 | 0.50 | `one-sided-limits` |
| `u-03-09-07` | 函数怎样在有限点附近趋于无穷？ | 1.75 | 0.25 | `infinite-limits-at-point` |
| `u-03-09-08` | 自变量趋于无穷时怎样定义函数极限？ | 1.50 | 0.50 | `limits-at-infinity` |
| `u-03-09-03` | 局部估计怎样传递极限？ | 1.75 | 0.25 | `function-limit-laws` |
| `u-03-09-04` | 用点列靠近能否判别函数极限？ | 1.75 | 0.25 | `sequential-function-limits` |

Also assert:

- exact sums `13.0` theory and `3.0` applied;
- every unit has `content_standard == 2`;
- `_quarto.yml` uses the same eight-page reading order;
- the chapter contains no derivative, MVT, Taylor, L’Hôpital, Newton, or integration dependency.

Run:

```bash
python3.12 -m unittest tests.test_chapter_09 -v
```

Expected: failures for missing units, old hours, old order, and missing v2 flags.

- [ ] **Step 2: Register all eight units with final metadata**

In `curriculum/units.toml`:

- preserve existing IDs and paths;
- insert `09-05` through `09-08` in the approved reading order;
- update all eight hour allocations;
- set `content_standard = 2`;
- supply concrete prerequisite lists, difficulty, capabilities, and learning goals matching the design;
- keep Python prerequisites empty except where a short observational experiment is actually used.

Do not register an empty or unfinished page: complete the manuscript steps below before running `scripts/check_units.py`.

- [ ] **Step 3: Rewrite 9.1 neighborhood language**

In `u-03-09-01-local-neighborhoods.qmd`, cover domain accumulation points, neighborhoods, deleted neighborhoods, left/right neighborhoods, and the difference between `f(a)` and behavior near `a`. Include stable anchors:

- `def-u-03-09-01-accumulation-point`
- `def-u-03-09-01-neighborhood`
- two `ex-u-03-09-01-*` examples
- five `pr-u-03-09-01-*` exercises

Use domain-restricted examples such as a punctured domain and an endpoint.

- [ ] **Step 4: Rewrite 9.2 finite-point finite limits**

In `u-03-09-02-epsilon-delta-limit.qmd`, state the quantifiers in order, require `x` to lie in the function domain, prove uniqueness, and separate the punctured condition from the value at `a`. Preserve `def-u-03-09-02-function-limit`; add a uniqueness theorem anchor, two examples, two immediate checks, five exercises, and seven complete collapsed answers.

- [ ] **Step 5: Write 9.3 epsilon–delta proof workshop**

In `u-03-09-05-epsilon-delta-workshop.qmd`, teach backward design and forward verification for linear, quadratic, radical, and rational estimates. Explicitly show how auxiliary bounds such as `|x-a|<1` control a second factor. Add:

- `def-u-03-09-05-proof-certificate`
- `ex-u-03-09-05-linear`
- `ex-u-03-09-05-quadratic`
- at least five anchored exercises and seven complete answers.

- [ ] **Step 6: Write 9.4 one-sided limits**

In `u-03-09-06-one-sided-limits.qmd`, define both one-sided limits, prove that a two-sided finite limit exists iff both one-sided limits exist and agree, and treat interval endpoints and piecewise functions. Add:

- `def-u-03-09-06-left-limit`
- `def-u-03-09-06-right-limit`
- `thm-u-03-09-06-two-sided-criterion`
- examples showing agreement and disagreement.

- [ ] **Step 7: Write 9.5 infinite limits at a finite point**

In `u-03-09-07-infinite-limits-at-point.qmd`, define `+\infty` and `-\infty` targets with `M`-quantifiers, include one-sided versions, and state exactly what a vertical asymptote claim does and does not mean. Use `1/x` and `1/x^2` to distinguish sides. Add:

- `def-u-03-09-07-positive-infinite-limit`
- `def-u-03-09-07-negative-infinite-limit`
- two anchored examples and the full v2 exercise/answer set.

- [ ] **Step 8: Write 9.6 limits at infinity**

In `u-03-09-08-limits-at-infinity.qmd`, give all four domain-target combinations needed for `x→±∞` and finite/`±∞` values. Treat horizontal behavior and elementary growth comparisons without using L’Hôpital or derivatives. Add:

- `def-u-03-09-08-finite-limit-at-infinity`
- `def-u-03-09-08-infinite-limit-at-infinity`
- examples for rational functions and growth comparison.

- [ ] **Step 9: Rewrite 9.7 limit laws**

In `u-03-09-03-function-limit-laws.qmd`, prove local boundedness, eventual sign preservation, order preservation, squeeze, sum/product/quotient, and composition with all denominator/domain side conditions. Preserve `thm-u-03-09-03-squeeze`; add stable anchors for local boundedness and the quotient law.

- [ ] **Step 10: Rewrite 9.8 Heine’s sequential criterion**

In `u-03-09-04-sequential-function-limits.qmd`, prove both directions of the finite-point criterion. The reverse direction must negate the epsilon–delta definition and choose a bad point within `1/n` for every `n`; preserve `thm-u-03-09-04-sequential-criterion`. Add a sequence-based counterexample and exercises transferring the method to one-sided or infinite limits.

- [ ] **Step 11: Put registry and Website navigation in exact reading order**

Update both `project.render` and the Chapter 9 sidebar block in `_quarto.yml` to:

```text
09-01, 09-02, 09-05, 09-06, 09-07, 09-08, 09-03, 09-04
```

The sidebar labels must be generated manually as `9.1` through `9.8` using the final titles; do not expose ID suffixes as reading numbers.

- [ ] **Step 12: Make Chapter 9 and generic v2 validation green**

Run:

```bash
python3.12 -m unittest tests.test_chapter_09 tests.test_units tests.test_sidebar -v
python3.12 scripts/check_units.py
```

Expected: all pass; the registry reports 52 units at this stage.

- [ ] **Step 13: Review mathematical and source quality**

Run:

```bash
rg -n "导数|中值定理|Taylor|L.?Hôpital|洛必达|Newton|积分" book/part-03/chapter-09
rg -n "TODO|TBD|待补|占位|显然可取|图像可知" book/part-03/chapter-09
git diff --check
```

Expected: no forbidden dependency or placeholder prose. Any occurrence of “中值” must refer only to an intermediate value in ordinary language, not the Mean Value Theorem.

- [ ] **Step 14: Commit the green Chapter 9 slice**

Run:

```bash
git add tests/test_chapter_09.py curriculum/units.toml _quarto.yml book/part-03/chapter-09
git commit -m "feat: rebuild chapter nine function limits"
```

## Task 4: Rewrite Chapter 10 and close the elementary-continuity bridge

**Files:**
- Modify: `tests/test_chapter_10.py`
- Modify: `curriculum/units.toml`
- Modify: `_quarto.yml`
- Rewrite: `book/part-03/chapter-10/u-03-10-01-epsilon-delta-continuity.qmd`
- Rewrite: `book/part-03/chapter-10/u-03-10-02-continuous-operations.qmd`
- Create: `book/part-03/chapter-10/u-03-10-04-one-sided-continuity-extension.qmd`
- Rewrite: `book/part-03/chapter-10/u-03-10-03-discontinuities-elementary-functions.qmd`
- Create: `book/part-03/chapter-10/u-03-10-05-elementary-continuity-bridge.qmd`

- [ ] **Step 1: Write the failing five-unit Chapter 10 contract**

Require this exact order and hours:

| ID | Title | Theory | Applied | Suffix |
|---|---|---:|---:|---|
| `u-03-10-01` | 连续性怎样写成局部控制？ | 1.75 | 0.25 | `epsilon-delta-continuity` |
| `u-03-10-02` | 连续性怎样经过运算和复合传递？ | 1.75 | 0.25 | `continuous-operations` |
| `u-03-10-04` | 单侧连续怎样处理端点与连续延拓？ | 1.50 | 0.50 | `one-sided-continuity-extension` |
| `u-03-10-03` | 函数会以哪些方式失去连续性？ | 1.50 | 0.50 | `discontinuities-elementary-functions` |
| `u-03-10-05` | 初等代数函数的连续性从哪里来？ | 1.50 | 0.50 | `elementary-continuity-bridge` |

Assert exact sums `8.0+2.0`, `content_standard == 2`, exact Quarto order, and absence of Part IV tools.

Run:

```bash
python3.12 -m unittest tests.test_chapter_10 -v
```

Expected: missing-unit, old-hour, and missing-v2 failures.

- [ ] **Step 2: Register the final five units**

Update Chapter 10 entries in `curriculum/units.toml`, add `10-04` and `10-05`, and set final hours, prerequisites, capabilities, learning goals, and `content_standard = 2`.

- [ ] **Step 3: Rewrite 10.1 point and set continuity**

Define continuity by `lim_{x→a} f(x)=f(a)`, then prove the equivalent epsilon–delta and sequential forms. Define continuity on a subset with relative-domain quantification. Preserve `def-u-03-10-01-continuity` and include examples at interior and endpoint points.

- [ ] **Step 4: Rewrite 10.2 continuous operations and composition**

Prove arithmetic and composition closure using Chapter 9 laws. Preserve:

- `thm-u-03-10-02-continuous-operations`
- `thm-u-03-10-02-composition`

Every quotient or composition example must state the denominator and domain condition.

- [ ] **Step 5: Write 10.3 one-sided continuity and extension**

Define left/right continuity and endpoint continuity, then characterize removable discontinuities and continuous extension. Include piecewise parameter examples and anchors:

- `def-u-03-10-04-one-sided-continuity`
- `thm-u-03-10-04-continuous-extension`

- [ ] **Step 6: Rewrite 10.4 discontinuity classification**

Treat removable, jump, infinite, and oscillatory discontinuities. Preserve `ex-u-03-10-03-discontinuity-types`; use sequential witnesses for oscillation and state why classification depends on the relevant one-sided limits.

- [ ] **Step 7: Write 10.5 elementary algebraic continuity**

Prove, rather than merely cite, continuity on the correct domains for constants, identity, polynomials, rational functions, absolute value, roots, and finite compositions. Add:

- `thm-u-03-10-05-polynomial-continuity`
- `thm-u-03-10-05-rational-continuity`
- `thm-u-03-10-05-root-continuity`

State exponent/logarithm continuity as named prerequisite facts, not reconstructed results. Link to the optional trigonometric bridge only after that bridge exists; until Task 7, use forward text without a broken link.

- [ ] **Step 8: Update Quarto order and labels**

Set Chapter 10 navigation order to `10-01, 10-02, 10-04, 10-03, 10-05`, displayed as `10.1` through `10.5`.

- [ ] **Step 9: Validate and review Chapter 10**

Run:

```bash
python3.12 -m unittest tests.test_chapter_10 tests.test_units tests.test_sidebar -v
python3.12 scripts/check_units.py
rg -n "导数|中值定理|Taylor|洛必达|Newton|图像.*连续" book/part-03/chapter-10
rg -n "TODO|TBD|待补|占位" book/part-03/chapter-10
git diff --check
```

Expected: all tests pass; the registry reports 54 units; searches reveal no forbidden proof dependency or placeholder.

- [ ] **Step 10: Commit the green Chapter 10 slice**

Run:

```bash
git add tests/test_chapter_10.py curriculum/units.toml _quarto.yml book/part-03/chapter-10
git commit -m "feat: rebuild chapter ten continuity"
```

## Task 5: Replace Chapter 11’s open-cover route with sequential compactness

**Files:**
- Modify: `tests/test_chapter_11.py`
- Modify: `tests/test_site.py`
- Modify: `scripts/check_site.py`
- Modify: `curriculum/units.toml`
- Rewrite: `book/part-03/chapter-11/u-03-11-01-compact-intervals.qmd`
- Rewrite: `book/part-03/chapter-11/u-03-11-02-extreme-value-theorem.qmd`
- Rewrite: `book/part-03/chapter-11/u-03-11-03-uniform-continuity.qmd`

- [ ] **Step 1: Write failing sequential-compactness tests**

Update the registry expectations to:

| ID | Title | Theory | Applied |
|---|---|---:|---:|
| `u-03-11-01` | 为什么闭区间中的数列总有收敛子列？ | 1.75 | 0.25 |
| `u-03-11-02` | 连续函数为何一定有界并取得最值？ | 1.75 | 0.25 |
| `u-03-11-03` | 局部连续何时升级为全局一致控制？ | 1.50 | 0.50 |

Require:

- exact sums `5.0+1.0`;
- `content_standard == 2`;
- `def-u-03-11-01-sequential-compactness`;
- explicit use of `Bolzano–Weierstrass` and closedness;
- no core definitions `def-u-03-11-01-open-cover` or `def-u-03-11-01-compactness`;
- no `thm-u-03-11-01-heine-borel`;
- the words “开覆盖” may occur only in a clearly labelled optional preview section.

Run:

```bash
python3.12 -m unittest tests.test_chapter_11 -v
```

Expected: failures demonstrate the current open-cover route and old hours.

- [ ] **Step 2: Update rendered-anchor expectations first**

In `scripts/check_site.py`, replace Chapter 11’s old compactness/Heine–Borel anchors with:

- `def-u-03-11-01-sequential-compactness`
- `thm-u-03-11-01-closed-interval-sequentially-compact`

Update the corresponding expectation in `tests/test_site.py`.

Run:

```bash
python3.12 -m unittest tests.test_site -v
```

Expected: the static expectation test passes; the manuscript test remains red until the QMD is rewritten.

- [ ] **Step 3: Update Chapter 11 registry metadata**

Apply the final titles, hours, `content_standard = 2`, and prerequisite links to Chapter 8 Bolzano–Weierstrass and Chapter 10 continuity.

- [ ] **Step 4: Rewrite 11.1 around sequential compactness**

Start with the real-line definition needed in this book: every sequence in the set has a subsequence converging to a point of the set. Prove the closed-interval result by:

1. boundedness of a sequence in `[a,b]`;
2. Part II Bolzano–Weierstrass;
3. closedness retaining the limit.

Distinguish closed, bounded, and sequentially compact with counterexamples. Put open-cover terminology only in `### 选读前瞻：第七部的开覆盖语言`, with no proof or core dependency.

- [ ] **Step 5: Rewrite 11.2 extreme value theorem**

Prove boundedness by contradiction using a sequence `|f(x_n)|>n`, extract a convergent subsequence, and use continuity. Then separately prove the supremum and infimum are attained by selecting approximating sequences and extracting convergent subsequences. Preserve `thm-u-03-11-02-extreme-value`.

- [ ] **Step 6: Rewrite 11.3 Heine–Cantor**

Define uniform continuity with quantifiers in the correct order. Prove the closed-interval theorem by contradiction: construct `x_n,y_n` with `|x_n-y_n|<1/n` but a fixed lower bound on `|f(x_n)-f(y_n)|`, extract a convergent subsequence from one sequence, and control the paired sequence. Preserve `thm-u-03-11-03-uniform-continuity`.

- [ ] **Step 7: Validate proof boundaries**

Run:

```bash
python3.12 -m unittest tests.test_chapter_11 tests.test_site tests.test_units -v
python3.12 scripts/check_units.py
rg -n "def-u-03-11-01-open-cover|thm-u-03-11-01-heine-borel|有限子覆盖|一般度量空间" book/part-03/chapter-11
rg -n "TODO|TBD|待补|占位" book/part-03/chapter-11
git diff --check
```

Expected: tests pass. Any “有限子覆盖” or “一般度量空间” occurrence must be confined to optional preview prose and not used in a proof.

- [ ] **Step 8: Commit the green Chapter 11 slice**

Run:

```bash
git add tests/test_chapter_11.py tests/test_site.py scripts/check_site.py curriculum/units.toml book/part-03/chapter-11
git commit -m "feat: rebuild chapter eleven via sequential compactness"
```

## Task 6: Rewrite Chapter 12 around existence and verifiable certificates

**Files:**
- Modify: `tests/test_chapter_12.py`
- Modify: `curriculum/units.toml`
- Modify: `_quarto.yml`
- Rewrite: `book/part-03/chapter-12/u-03-12-01-intermediate-value-theorem.qmd`
- Rewrite: `book/part-03/chapter-12/u-03-12-03-fixed-points-and-iteration.qmd`
- Rewrite: `book/part-03/chapter-12/u-03-12-02-certified-bisection.qmd`
- Create: `book/part-03/chapter-12/u-03-12-04-certificate-comparison.qmd`
- Read/reuse: `src/mathbook_examples/bisection.py`
- Read/reuse: `tests/test_bisection.py`

- [ ] **Step 1: Write the failing final Chapter 12 contract**

Require exact order:

| ID | Title | Theory | Applied | Suffix |
|---|---|---:|---:|---|
| `u-03-12-01` | 连续函数怎样保证取遍中间值？ | 1.75 | 0.25 | `intermediate-value-theorem` |
| `u-03-12-03` | 有固定点是否意味着简单迭代会收敛？ | 1.50 | 0.50 | `fixed-points-and-iteration` |
| `u-03-12-02` | 怎样把有根证明变成误差可证的算法？ | 1.25 | 0.75 | `certified-bisection` |
| `u-03-12-04` | 不同存在与计算证书各自保证什么？ | 1.50 | 0.50 | `certificate-comparison` |

Assert exact sums `6.0+2.0`, `content_standard == 2`, exact Quarto order, reuse of `mathbook_examples.bisection`, and absence of Newton, derivative, MVT, and convergence-order claims.

Run:

```bash
python3.12 -m unittest tests.test_chapter_12 -v
```

Expected: missing `12-04`, old-hour, old-order, and missing-v2 failures.

- [ ] **Step 2: Register and order the four final units**

Update `curriculum/units.toml` and `_quarto.yml`. Sidebar display order must be `12.1 = 12-01`, `12.2 = 12-03`, `12.3 = 12-02`, `12.4 = 12-04`.

- [ ] **Step 3: Rewrite 12.1 zero and intermediate value theorems**

Prove the zero theorem by nested sign-changing intervals, invoke the Part II nested-interval theorem for the common point, and use continuity to force value zero. Derive the general intermediate value theorem by applying the zero theorem to `f-y`. Preserve:

- `thm-u-03-12-01-zero`
- `thm-u-03-12-01-intermediate-value`

Explicitly state that existence does not imply uniqueness or an algorithm.

- [ ] **Step 4: Rewrite 12.2 fixed-point existence and iteration boundary**

For continuous `g:[a,b]→[a,b]`, apply the zero theorem to `h(x)=g(x)-x` using endpoint signs. Preserve `thm-u-03-12-03-fixed-point`. Use `g(x)=1-x` to separate existence, uniqueness, iteration convergence, and error certification. Cite Part II contraction results without reproving them.

- [ ] **Step 5: Rewrite 12.3 certified bisection**

Follow this exact narrative:

```text
problem → continuity/sign assumptions → interval invariant → pseudocode
→ interval/root error → prior step count/stopping → existing Python API
→ result interpretation → rejected inputs
```

Preserve:

- `alg-u-03-12-02-bisection`
- `thm-u-03-12-02-bisection-error`

Import or show calls to `mathbook_examples.bisection`; do not paste a second implementation. Explain why a small residual is not an unconditional root-error bound.

- [ ] **Step 6: Write 12.4 certificate comparison**

Compare in one explicit table:

- intermediate-value existence certificate;
- bisection sign-changing interval and width certificate;
- Part II contraction self-map, contraction constant, convergence, uniqueness, and geometric error certificate.

Use at least one problem where only existence is known, one where bisection is certified, and one where contraction gives the stronger result. Add `tbl-u-03-12-04-certificates` and `thm-u-03-12-04-certificate-boundary`.

- [ ] **Step 7: Re-run algorithm tests without changing the implementation**

Run:

```bash
python3.12 -m unittest tests.test_bisection -v
git diff -- src/mathbook_examples/bisection.py
```

Expected: bisection tests pass and there is no diff in the implementation.

- [ ] **Step 8: Validate and review Chapter 12**

Run:

```bash
python3.12 -m unittest tests.test_chapter_12 tests.test_bisection tests.test_units tests.test_sidebar -v
python3.12 scripts/check_units.py
rg -n "Newton|导数|中值定理|收敛阶|Taylor|洛必达" book/part-03/chapter-12
rg -n "TODO|TBD|待补|占位" book/part-03/chapter-12
git diff --check
```

Expected: all tests pass; the registry reports the final 55 core units; no forbidden dependencies or placeholders.

- [ ] **Step 9: Commit the green Chapter 12 slice**

Run:

```bash
git add tests/test_chapter_12.py curriculum/units.toml _quarto.yml book/part-03/chapter-12
git commit -m "feat: rebuild chapter twelve certificates"
```

## Task 7: Add the optional trigonometric-continuity bridge

**Files:**
- Create: `book/bridges/math/trigonometric-continuity.qmd`
- Modify: `_quarto.yml`
- Modify: `tests/test_sidebar.py`
- Modify: `book/part-03/chapter-10/u-03-10-05-elementary-continuity-bridge.qmd`

- [ ] **Step 1: Write a failing navigation test for the non-core bridge**

In `tests/test_sidebar.py`, assert:

- `book/bridges/math/trigonometric-continuity.qmd` is in both `project.render` and the `附录` sidebar section;
- it appears exactly once;
- it is not present in `curriculum/units.toml`;
- total rendered QMD paths equal 60 after all seven registered additions and this bridge.

Run:

```bash
python3.12 -m unittest tests.test_sidebar -v
```

Expected: failure because the bridge does not yet exist in Quarto config.

- [ ] **Step 2: Write the complete optional page**

Create a standalone, unnumbered page with stable H1 anchor `bridge-trigonometric-continuity`. Cover:

- the standard inequality needed near zero;
- continuity of sine at zero;
- addition-formula transfer to arbitrary points;
- continuity of cosine;
- domain-aware consequences for tangent where cosine is nonzero;
- at least two worked examples and a complete optional exercise set.

Do not register this page as a core unit and do not add its hours to the outline.

- [ ] **Step 3: Register the bridge only in Website render/sidebar**

Add the page to `project.render` and to the `附录` section in `_quarto.yml` with label `三角函数连续性（选读）`.

- [ ] **Step 4: Link the core elementary-continuity bridge**

Add a relative Quarto link from `u-03-10-05-elementary-continuity-bridge.qmd` to the optional page. Keep the core proof self-contained for algebraic functions.

- [ ] **Step 5: Validate and commit**

Run:

```bash
python3.12 -m unittest tests.test_sidebar tests.test_units -v
python3.12 scripts/check_units.py
git diff --check
git add book/bridges/math/trigonometric-continuity.qmd book/part-03/chapter-10/u-03-10-05-elementary-continuity-bridge.qmd _quarto.yml tests/test_sidebar.py
git commit -m "feat: add trigonometric continuity bridge"
```

Expected: tests pass; core registry remains 55.

## Task 8: Close global registry, map, site-marker, and source-quality contracts

**Files:**
- Modify: `tests/test_curriculum_map.py`
- Modify: `tests/test_units.py`
- Modify: `tests/test_site.py`
- Modify: `scripts/check_site.py`
- Regenerate: `book/curriculum-map.qmd`

- [ ] **Step 1: Write final global registry assertions**

In `tests/test_units.py`, add a test that:

- the registry contains exactly 55 unique unit IDs and paths;
- Part III contains exactly 20 units;
- every Part III unit has `content_standard = 2`;
- Part III sums to `32.0` theory and `8.0` applied.

Run:

```bash
python3.12 -m unittest tests.test_units -v
```

Expected: pass if all chapter tasks are complete; otherwise fix registry metadata, not the expected totals.

- [ ] **Step 2: Update the curriculum-map contract to the final Part III set**

In `tests/test_curriculum_map.py`:

- change the Part III link count from 13 to 20;
- assert the first, one middle new unit, and final certificate-comparison link;
- retain 12 parts, 54 chapters, and `290+94=384`.

Run:

```bash
python3.12 -m unittest tests.test_curriculum_map -v
```

Expected: failure because the generated map is stale.

- [ ] **Step 3: Regenerate the map and make it deterministic**

Run:

```bash
python3.12 scripts/render_curriculum_map.py
python3.12 -m unittest tests.test_curriculum_map -v
python3.12 scripts/render_curriculum_map.py
git diff --exit-code -- book/curriculum-map.qmd
```

Expected: tests pass and the second generation creates no diff.

- [ ] **Step 4: Expand rendered-site anchor coverage**

In `scripts/check_site.py`, require representative anchors for:

- Chapter 9 finite, one-sided, infinite-at-point, infinity-domain, law, and Heine pages;
- Chapter 10 continuity, extension, discontinuity, and elementary bridge;
- Chapter 11 sequential compactness, EVT, and uniform continuity;
- Chapter 12 IVT, fixed point, bisection, and certificate comparison;
- optional trigonometric bridge.

In `tests/test_site.py`, assert the exact anchor lists for at least one representative page per chapter and for the optional bridge.

- [ ] **Step 5: Strengthen Part III navigation markers**

Update `REQUIRED_NAVIGATION_MARKERS` and the Part III marker loop so a Chapter 12 page contains:

- the Third Part title;
- Chapter 12 title;
- labels `12.1` through `12.4`;
- hierarchical sidebar marker.

Also add a marker check for the optional trigonometric page under `附录`.

- [ ] **Step 6: Run source-level global checks**

Run:

```bash
python3.12 -m unittest tests.test_units tests.test_curriculum_map tests.test_sidebar tests.test_site -v
python3.12 scripts/check_outline.py
python3.12 scripts/check_units.py
git diff --check
```

Expected: all pass; reports are `290+94=384` and 55 units.

- [ ] **Step 7: Review all Part III prose for placeholders and forbidden scope**

Run:

```bash
rg -n "TODO|TBD|待补|占位|稍后补充|此处省略" book/part-03 book/bridges/math/trigonometric-continuity.qmd
rg -n "Newton|洛必达|L.?Hôpital|Taylor|Riemann|一般度量空间" book/part-03
rg -n "显然|容易看出|不难证明" book/part-03
```

Expected:

- first search: no matches;
- second search: matches only in explicit “本部不使用” boundary statements, if any;
- third search: every match is manually checked and expanded wherever it hides a real proof step.

- [ ] **Step 8: Commit global contracts**

Run:

```bash
git add tests/test_curriculum_map.py tests/test_units.py tests/test_site.py scripts/check_site.py book/curriculum-map.qmd
git commit -m "test: close part three global contracts"
```

## Task 9: Run full verification and browser review

**Files:**
- Inspect: `_site/`
- Inspect: `book/part-03/**/*.qmd`
- Do not commit: `_site/`

- [ ] **Step 1: Run all Python tests**

Run:

```bash
python3.12 -m unittest discover -s tests -v
```

Expected: all tests pass with no import outside the Python 3.12 standard-library dependencies already used by the project.

- [ ] **Step 2: Run the authoritative full verification**

Run:

```bash
DENO_DIR=/private/tmp/mathbook-part3-quarto-cache make verify
```

Expected:

- unit tests pass;
- outline reports 12 parts, 54 chapters, `290+94=384`;
- unit registry reports 55 units;
- Quarto renders all 60 configured pages;
- site validation reports valid internal links, titles, navigation, anchors, and no automatic chapter/heading numbering.

- [ ] **Step 3: Verify no generated artifacts entered the source tree**

Run:

```bash
git status --short
find book -type f \( -name '*.html' -o -name '*.ipynb' \) -print
```

Expected: no source-tree HTML/notebook artifacts. `_site/` may exist locally but remains ignored.

- [ ] **Step 4: Start a local preview for visual QA**

Run:

```bash
quarto preview --no-browser
```

Expected: a local URL is printed. Keep the preview process running only for the following browser checks.

- [ ] **Step 5: Inspect one representative page from each chapter**

Using the browser-control skill, inspect:

- Chapter 9: `u-03-09-08-limits-at-infinity`;
- Chapter 10: `u-03-10-05-elementary-continuity-bridge`;
- Chapter 11: `u-03-11-01-compact-intervals`;
- Chapter 12: `u-03-12-04-certificate-comparison`;
- Appendix: `trigonometric-continuity`.

For each page verify:

- MathJax expressions render without raw commands;
- sidebar labels match the intended reading order;
- no `chapter-number` or `header-section-number` spans appear;
- collapsed answers open;
- tables and callouts fit a narrow viewport;
- previous/next navigation follows the configured sequence.

- [ ] **Step 6: Fix any visual defects and repeat proportional checks**

If a QMD or style fix is needed, rerun its chapter test, `tests.test_site`, and `DENO_DIR=/private/tmp/mathbook-part3-quarto-cache make verify`. Do not weaken tests to accept a rendering defect.

- [ ] **Step 7: Perform final diff review**

Run:

```bash
git diff origin/main --stat
git diff origin/main -- curriculum/outline.toml curriculum/units.toml _quarto.yml
git diff --check origin/main
git status --short --branch
```

Confirm:

- only the approved Part III, bridge, curriculum, test, and design/plan files changed;
- Part I and Part II QMD files are untouched;
- no Part IV file changed;
- all 13 old Part III paths remain;
- exactly seven core QMDs and one optional bridge QMD were added.

- [ ] **Step 8: Commit any final QA corrections**

If QA produced changes:

```bash
git status --short
git add book/part-03 book/bridges/math/trigonometric-continuity.qmd curriculum _quarto.yml tests scripts/check_site.py
git commit -m "fix: polish part three rendered manuscript"
```

If QA produced no changes, do not create an empty commit.

## Task 10: Final completion gate and stop boundary

- [ ] **Step 1: Invoke verification-before-completion**

Run the `superpowers:verification-before-completion` skill and use the fresh Task 9 output as evidence. If any required command is stale or failed, rerun it before claiming completion.

- [ ] **Step 2: Confirm final branch state**

Run:

```bash
git status --short --branch
git log --oneline origin/main..HEAD
```

Expected: clean `codex/part-03-self-study-rewrite` branch with the approved design, plan, chapter commits, global-contract commit, and any justified QA correction.

- [ ] **Step 3: Report completion and stop**

Report:

- 20 core Part III units, `32+8=40` hours;
- whole-book baseline `290+94=384`;
- 55 registered core units;
- 60 rendered pages including the optional bridge;
- full verification result;
- branch/commit state.

Stop after Part III. Do not begin Chapter 13 or any Part IV work.
