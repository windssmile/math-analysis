# Part III Continuity and Existence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the 13 registered, renderable Part III learning units that establish an \(\varepsilon\)-\(\delta\)-first theory of function limits, continuity, compactness, and existence, with certified numerical applications.

**Architecture:** Keep the existing file-per-learning-unit Quarto structure. Register every unit in `curriculum/units.toml`, expose each page in `_quarto.yml` and the generated curriculum map, and use chapter-specific regression tests to lock titles, hours, paths, theorem anchors, prerequisites, and dependency boundaries. Existing bisection and contraction example modules stay unchanged; Part III consumes them only as static, tested demonstrations.

**Tech Stack:** Quarto/QMD, TOML, Python 3.12 standard-library `unittest`, existing `scripts/check_outline.py`, `scripts/check_units.py`, `scripts/render_curriculum_map.py`, and `scripts/check_site.py`.

---

## File map

| File | Responsibility |
|---|---|
| `curriculum/outline.toml` | Set `part-03.show_units = true` without changing approved titles, questions, or hours. |
| `curriculum/units.toml` | Replace the pilot registry entry with the 13 Part III unit contracts. |
| `_quarto.yml` | Replace the sole pilot navigation entry with the thirteen pages, in Chapter 9 → 12 order. |
| `book/part-03/chapter-09/*.qmd` | Four \(\varepsilon\)-\(\delta\)-first function-limit units. |
| `book/part-03/chapter-10/*.qmd` | Three continuity units, with sequence language only as established equivalence. |
| `book/part-03/chapter-11/*.qmd` | Three compactness, extreme-value, and uniform-continuity units. |
| `book/part-03/chapter-12/*.qmd` | Three existence and algorithm units replacing the old pilot. |
| `tests/test_chapter_09.py` through `tests/test_chapter_12.py` | Regression contracts for each new chapter's registry and mathematical scope. |
| `tests/test_curriculum_map.py` | Assert that the Part III directory exposes its 13 registered links. |
| `scripts/check_site.py`, `tests/test_site.py` | Require rendered Part III theorem/algorithm anchors and replace the old pilot-only check. |

## Canonical unit registry

Use these exact IDs, titles, hours, and page suffixes. All thirteen entries require the existing TOML list fields: `book_prerequisites`, `higher_algebra_prerequisites`, `analytic_geometry_prerequisites`, `python_prerequisites`, `knowledge_bridges`, `capabilities`, and `learning_goals`.

| ID | Chapter | Title | Theory+application | Suffix |
|---|---|---|---:|---|
| `u-03-09-01` | `chapter-09` | 函数在一点附近意味着什么？ | 1.60+0.40 | `local-neighborhoods` |
| `u-03-09-02` | `chapter-09` | “任意接近”怎样定义函数极限？ | 1.60+0.40 | `epsilon-delta-limit` |
| `u-03-09-03` | `chapter-09` | 局部估计怎样传递极限？ | 1.50+0.50 | `function-limit-laws` |
| `u-03-09-04` | `chapter-09` | 用点列靠近能否判别函数极限？ | 1.50+0.50 | `sequential-function-limits` |
| `u-03-10-01` | `chapter-10` | 连续性怎样写成局部控制？ | 1.60+0.40 | `epsilon-delta-continuity` |
| `u-03-10-02` | `chapter-10` | 连续性怎样经过运算和复合传递？ | 1.50+0.50 | `continuous-operations` |
| `u-03-10-03` | `chapter-10` | 函数会以哪些方式失去连续性？ | 1.50+0.50 | `discontinuities-elementary-functions` |
| `u-03-11-01` | `chapter-11` | 为什么闭区间能把无限局部信息压缩为有限控制？ | 1.60+0.40 | `compact-intervals` |
| `u-03-11-02` | `chapter-11` | 连续函数为何一定有界并取得最值？ | 1.50+0.50 | `extreme-value-theorem` |
| `u-03-11-03` | `chapter-11` | 局部连续何时升级为全局一致控制？ | 1.50+0.50 | `uniform-continuity` |
| `u-03-12-01` | `chapter-12` | 连续函数怎样保证取遍中间值？ | 1.60+0.40 | `intermediate-value-theorem` |
| `u-03-12-02` | `chapter-12` | 怎样把有根证明变成误差可证的算法？ | 1.50+0.50 | `certified-bisection` |
| `u-03-12-03` | `chapter-12` | 有固定点是否意味着简单迭代会收敛？ | 1.50+0.50 | `fixed-points-and-iteration` |

Every QMD page must begin with `# <title> {#<unit-id>}`, contain the eight headings required by `scripts/check_units.py`, include 3--6 answered exercises, and contain the stable anchors listed in the chapter tasks below.

### Task 1: Register the Part III surface and navigation

**Files:**
- Modify: `curriculum/outline.toml`
- Modify: `curriculum/units.toml`
- Modify: `_quarto.yml`
- Modify: `tests/test_curriculum_map.py`
- Create: `tests/test_chapter_09.py`
- Create: `tests/test_chapter_10.py`
- Create: `tests/test_chapter_11.py`
- Create: `tests/test_chapter_12.py`
- Delete: `book/part-03/chapter-12/u-03-12-01-ivt-bisection.qmd`

- [ ] **Step 1: Write the failing registry and navigation tests.**

  Create the four chapter tests with a `test_registry_closes_chapter_hours_and_paths` method. Each must load `curriculum/units.toml`, make a dictionary by `id`, and assert the exact rows from the canonical table. In `tests/test_curriculum_map.py`, replace the negative Part III assertion with:

  ```python
  self.assertIn(
      "   - [函数在一点附近意味着什么？](part-03/chapter-09/u-03-09-01-local-neighborhoods.qmd#u-03-09-01)",
      rendered,
  )
  self.assertIn(
      "   - [有固定点是否意味着简单迭代会收敛？](part-03/chapter-12/u-03-12-03-fixed-points-and-iteration.qmd#u-03-12-03)",
      rendered,
  )
  self.assertEqual(13, rendered.count("part-03/chapter-"))
  ```

- [ ] **Step 2: Run the registry tests and confirm the expected RED failure.**

  Run: `python3.12 -m unittest tests.test_chapter_09 tests.test_chapter_10 tests.test_chapter_11 tests.test_chapter_12 tests.test_curriculum_map -v`

  Expected: failures because Part III has only the old pilot entry and its directory is not enabled.

- [ ] **Step 3: Add the complete registry and navigation implementation.**

  Set `show_units = true` in `[[parts]] id = "part-03"`. Replace the old `u-03-12-01` TOML block with thirteen blocks from the canonical table. Use `chapter-08` as a prerequisite for `u-03-09-01` through `u-03-09-04`; use `chapter-09` for Chapter 10; use `chapter-10` and the relevant Chapter 8 completeness result for Chapter 11; use `chapter-10` plus `chapter-11` for Chapter 12. Only `u-03-12-02` needs `functions-loops.qmd` and Python prerequisites. Give all theory pages `concepts`, `proof`, and `mathematical_expression`; add `analytic_calculation` where limit estimates are computed; add `numerical_algorithm` to `u-03-12-02` and `u-03-12-03`.

  Replace the single Part III `_quarto.yml` page with the thirteen canonical paths in table order. Remove the old pilot QMD so its obsolete ID/path cannot remain discoverable.

- [ ] **Step 4: Generate the map and prove the registry is green.**

  Run: `python3.12 scripts/render_curriculum_map.py && python3.12 -m unittest tests.test_chapter_09 tests.test_chapter_10 tests.test_chapter_11 tests.test_chapter_12 tests.test_curriculum_map -v && python3.12 scripts/check_units.py`

  Expected: the map test sees 13 Part III links; the checker will still fail only until the thirteen QMD pages are created. Do not treat this intermediate checker failure as a baseline failure.

- [ ] **Step 5: Commit the registry and test contract.**

  ```bash
  git add curriculum/outline.toml curriculum/units.toml _quarto.yml book/curriculum-map.qmd \
    tests/test_chapter_09.py tests/test_chapter_10.py tests/test_chapter_11.py tests/test_chapter_12.py \
    tests/test_curriculum_map.py book/part-03/chapter-12/u-03-12-01-ivt-bisection.qmd
  git commit -m "feat: register part three learning units"
  ```

### Task 2: Write Chapter 9’s epsilon--delta-first function-limit pages

**Files:**
- Create: `book/part-03/chapter-09/u-03-09-01-local-neighborhoods.qmd`
- Create: `book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.qmd`
- Create: `book/part-03/chapter-09/u-03-09-03-function-limit-laws.qmd`
- Create: `book/part-03/chapter-09/u-03-09-04-sequential-function-limits.qmd`
- Modify: `tests/test_chapter_09.py`

- [ ] **Step 1: Add failing mathematical-scope assertions.**

  Add a `test_function_limit_pages_keep_epsilon_delta_as_the_main_language` method that reads the four pages and asserts these markers:

  ```python
  self.assertIn("def-u-03-09-01-neighborhood", local)
  self.assertIn("def-u-03-09-02-function-limit", epsilon_delta)
  self.assertIn(r"0<|x-a|<\delta", epsilon_delta)
  self.assertIn("thm-u-03-09-03-squeeze", laws)
  self.assertIn("thm-u-03-09-04-sequential-criterion", sequential)
  self.assertIn("反设", sequential)
  self.assertNotIn("连续函数", epsilon_delta)
  ```

- [ ] **Step 2: Run the Chapter 9 test and confirm RED.**

  Run: `python3.12 -m unittest tests.test_chapter_09 -v`

  Expected: failure because the four QMD files do not yet exist.

- [ ] **Step 3: Write the four pages.**

  In order, establish neighborhoods and deleted neighborhoods; the formal \(\varepsilon\)-\(\delta\) definition and definition-domain examples; limit laws, order preservation, and squeeze; then the sequential criterion with the contrapositive point-sequence construction. Give full proofs for the defining examples, limit laws needed later, squeeze, and both directions of the sequential criterion. Use sequence examples to test the definition, never to define it first. Include one-sided, infinite, and oscillatory counterexamples without calling on continuity or derivatives.

  Use these anchors exactly: `def-u-03-09-01-neighborhood`, `def-u-03-09-01-deleted-neighborhood`, `def-u-03-09-02-function-limit`, `thm-u-03-09-03-limit-laws`, `thm-u-03-09-03-squeeze`, and `thm-u-03-09-04-sequential-criterion`.

- [ ] **Step 4: Run Chapter 9 and unit-structure checks.**

  Run: `python3.12 -m unittest tests.test_chapter_09 -v && python3.12 scripts/check_units.py`

  Expected: Chapter 9 passes; the unit checker proceeds past all four Chapter 9 pages and reports only missing later registered pages.

- [ ] **Step 5: Commit Chapter 9.**

  ```bash
  git add book/part-03/chapter-09 tests/test_chapter_09.py
  git commit -m "feat: add function limit foundations"
  ```

### Task 3: Write Chapter 10’s continuity pages

**Files:**
- Create: `book/part-03/chapter-10/u-03-10-01-epsilon-delta-continuity.qmd`
- Create: `book/part-03/chapter-10/u-03-10-02-continuous-operations.qmd`
- Create: `book/part-03/chapter-10/u-03-10-03-discontinuities-elementary-functions.qmd`
- Modify: `tests/test_chapter_10.py`

- [ ] **Step 1: Add failing Chapter 10 boundary assertions.**

  Add a test that requires `def-u-03-10-01-continuity`, `thm-u-03-10-02-continuous-operations`, `thm-u-03-10-02-composition`, and `ex-u-03-10-03-discontinuity-types`; require `r"|f(x)-f(a)|<\varepsilon"` in the first page; require `可去`, `跳跃`, and `振荡` in the third; and assert the three pages do not contain `中值定理` or `导数`.

- [ ] **Step 2: Run the Chapter 10 test and confirm RED.**

  Run: `python3.12 -m unittest tests.test_chapter_10 -v`

  Expected: failure because the pages are absent.

- [ ] **Step 3: Write the three pages.**

  Define continuity by function limit and prove its \(\varepsilon\)-\(\delta\) form. Prove sum, product, quotient, and composition rules while naming every domain and nonzero-denominator condition. In the third page, use the already-proved sequence equivalence to diagnose removable, jump, and oscillatory discontinuities; establish elementary-function continuity only on their actual domains. Keep all three pages within the eight-heading contract and 3--6 answered exercises.

- [ ] **Step 4: Run Chapter 10 and unit-structure checks.**

  Run: `python3.12 -m unittest tests.test_chapter_10 -v && python3.12 scripts/check_units.py`

  Expected: Chapter 10 passes; remaining checker errors identify only Chapters 11--12 pages.

- [ ] **Step 5: Commit Chapter 10.**

  ```bash
  git add book/part-03/chapter-10 tests/test_chapter_10.py
  git commit -m "feat: add continuity theory"
  ```

### Task 4: Write Chapter 11’s compactness and global-control pages

**Files:**
- Create: `book/part-03/chapter-11/u-03-11-01-compact-intervals.qmd`
- Create: `book/part-03/chapter-11/u-03-11-02-extreme-value-theorem.qmd`
- Create: `book/part-03/chapter-11/u-03-11-03-uniform-continuity.qmd`
- Modify: `tests/test_chapter_11.py`

- [ ] **Step 1: Add failing Chapter 11 proof-contract assertions.**

  Require `def-u-03-11-01-open-cover`, `def-u-03-11-01-compactness`, `thm-u-03-11-01-heine-borel`, `thm-u-03-11-02-extreme-value`, and `thm-u-03-11-03-uniform-continuity`. Assert that the compactness page contains `上确界` and `有限子覆盖`, the uniform-continuity page contains `\min`, and none of the three pages contains `一般度量空间`.

- [ ] **Step 2: Run the Chapter 11 test and confirm RED.**

  Run: `python3.12 -m unittest tests.test_chapter_11 -v`

  Expected: failure because the pages are absent.

- [ ] **Step 3: Write the three pages.**

  First define open cover and compactness, use the specified upper-bound set proof to show `[a,b]` has a finite subcover, and connect this to the Chapter 8 Bolzano--Weierstrass result only after the definition. Then prove the extreme-value theorem, distinguishing boundedness from attainment and using `1/x` on `(0,1)` as a noncompact counterexample. Finally define uniform continuity and prove the closed-interval theorem by choosing a finite subcover and the minimum positive local radius; explicitly identify why pointwise `\delta_x` is not yet uniform.

- [ ] **Step 4: Run Chapter 11 and unit-structure checks.**

  Run: `python3.12 -m unittest tests.test_chapter_11 -v && python3.12 scripts/check_units.py`

  Expected: Chapter 11 passes; only Chapter 12 registrations remain without QMD content.

- [ ] **Step 5: Commit Chapter 11.**

  ```bash
  git add book/part-03/chapter-11 tests/test_chapter_11.py
  git commit -m "feat: add compact interval theorems"
  ```

### Task 5: Write Chapter 12’s existence, bisection, and fixed-point pages

**Files:**
- Create: `book/part-03/chapter-12/u-03-12-01-intermediate-value-theorem.qmd`
- Create: `book/part-03/chapter-12/u-03-12-02-certified-bisection.qmd`
- Create: `book/part-03/chapter-12/u-03-12-03-fixed-points-and-iteration.qmd`
- Modify: `tests/test_chapter_12.py`

- [ ] **Step 1: Add failing Chapter 12 theorem and algorithm assertions.**

  Require anchors `thm-u-03-12-01-intermediate-value`, `thm-u-03-12-01-zero`, `alg-u-03-12-02-bisection`, `thm-u-03-12-02-bisection-error`, and `thm-u-03-12-03-fixed-point`. Require the bisection page to contain `先验误差上界`, `mathbook_examples.bisection`, and `残差`; require the fixed-point page to contain `x_{n+1}=1-x_n`, `唯一不动点`, and `压缩映射定理`; assert all three pages omit `Newton` and `中值定理`.

- [ ] **Step 2: Run the Chapter 12 test and confirm RED.**

  Run: `python3.12 -m unittest tests.test_chapter_12 -v`

  Expected: failure because the replacement pages are absent.

- [ ] **Step 3: Write the intermediate-value page.**

  Prove the zero theorem by interval nesting: retain an endpoint-sign invariant, invoke the completed Chapter 7 interval-nesting theorem, and use continuity at the common point to rule out nonzero function values. Obtain the intermediate-value theorem from the zero theorem applied to `f-y`. State and exercise that existence does not imply uniqueness.

- [ ] **Step 4: Write the certified-bisection page.**

  Start from the zero theorem, then give assumptions, pseudocode, interval-inclusion invariant, midpoint error bound `(b-a)/2^{n+1}`, an integer stopping rule, and a static import from `mathbook_examples.bisection`. Explain that a small residual is not an unconditional root-error certificate. Do not modify `src/mathbook_examples/bisection.py`; its existing behavior tests remain the source of truth.

- [ ] **Step 5: Write the fixed-point page.**

  For continuous `g:[a,b]\to[a,b]`, set `h(x)=g(x)-x` and prove existence by the zero theorem. Reuse, rather than re-prove, the Chapter 8 closed-interval contraction theorem to state conditions that certify uniqueness and iteration convergence. Give the `x_{n+1}=1-x_n` counterexample and calculate its oscillation, so the page separates existence, uniqueness, and convergence.

- [ ] **Step 6: Run Chapter 12, algorithm, and full unit checks.**

  Run: `python3.12 -m unittest tests.test_chapter_12 tests.test_bisection tests.test_fixed_point -v && python3.12 scripts/check_units.py`

  Expected: all Chapter 12 and existing algorithm tests pass; `unit registry valid: 43 unit(s)`.

- [ ] **Step 7: Commit Chapter 12.**

  ```bash
  git add book/part-03/chapter-12 tests/test_chapter_12.py
  git commit -m "feat: add existence and certified solving"
  ```

### Task 6: Require Part III anchors in the rendered site

**Files:**
- Modify: `scripts/check_site.py`
- Modify: `tests/test_site.py`

- [ ] **Step 1: Add failing rendered-anchor tests.**

  Add a `test_part_three_rendered_anchors_are_required` test that asserts these exact mapping entries:

  ```python
  self.assertEqual(
      ["def-u-03-09-02-function-limit"],
      REQUIRED_RENDERED_ANCHORS[
          "book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.html"
      ],
  )
  self.assertEqual(
      ["thm-u-03-09-04-sequential-criterion"],
      REQUIRED_RENDERED_ANCHORS[
          "book/part-03/chapter-09/u-03-09-04-sequential-function-limits.html"
      ],
  )
  ```

  Also replace the pilot-page-specific `main()` check with a loop over three Part III marker pages: the Chapter 9 epsilon--delta page, the Chapter 11 compactness page, and the Chapter 12 certified-bisection page.

- [ ] **Step 2: Run the site test and confirm RED.**

  Run: `python3.12 -m unittest tests.test_site -v`

  Expected: failure because the Part III anchor mapping does not yet exist.

- [ ] **Step 3: Implement the anchor mapping.**

  Add one mapping per rendered page, without placing anchors from two source pages under one HTML page. Use:

  ```python
  "book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.html": [
      "def-u-03-09-02-function-limit",
  ],
  "book/part-03/chapter-09/u-03-09-04-sequential-function-limits.html": [
      "thm-u-03-09-04-sequential-criterion",
  ],
  "book/part-03/chapter-11/u-03-11-01-compact-intervals.html": [
      "def-u-03-11-01-compactness",
      "thm-u-03-11-01-heine-borel",
  ],
  "book/part-03/chapter-11/u-03-11-03-uniform-continuity.html": [
      "thm-u-03-11-03-uniform-continuity",
  ],
  "book/part-03/chapter-12/u-03-12-02-certified-bisection.html": [
      "alg-u-03-12-02-bisection",
      "thm-u-03-12-02-bisection-error",
  ],
  ```

- [ ] **Step 4: Run the site unit tests.**

  Run: `python3.12 -m unittest tests.test_site -v`

  Expected: all site-validation unit tests pass before the full Quarto render.

- [ ] **Step 5: Commit the rendered-site contract.**

  ```bash
  git add scripts/check_site.py tests/test_site.py
  git commit -m "test: require part three rendered anchors"
  ```

### Task 7: Regenerate, render, and perform the final verification pass

**Files:**
- Modify: `book/curriculum-map.qmd` (generated)

- [ ] **Step 1: Regenerate and run the complete verification suite.**

  Run: `make verify`

  Expected: all unit tests pass, `outline valid: 12 parts, 54 chapters, 270+90=360 hours`, `unit registry valid: 43 unit(s)`, Quarto renders all registered pages, and `site valid` reports no broken links or missing anchors.

- [ ] **Step 2: If Quarto reports an unable-to-open cache database, clear only reproducible caches and rerun.**

  Run: `rm -rf .quarto/deno-cache .quarto/deno .quarto/project-cache .quarto/preview && make verify`

  Expected: render completes; do not delete `_site`, source content, or any unlisted path.

- [ ] **Step 3: Inspect the generated Part III directory and the rendered HTML paths.**

  Run: `rg -n "u-03-(09|10|11|12)-" book/curriculum-map.qmd && find _site/book/part-03 -name '*.html' | sort`

  Expected: 13 curriculum links and 13 rendered Part III unit pages, with no `ivt-bisection.html` pilot page.

- [ ] **Step 4: Commit the generated curriculum map if it changed.**

  ```bash
  git add book/curriculum-map.qmd
  git diff --cached --quiet || git commit -m "docs: publish part three curriculum map"
  ```

## Plan self-review

- Spec coverage: Tasks 2--5 map all 13 units, complete the epsilon--delta-first dependency chain, introduce open-cover compactness, include extreme-value and uniform-continuity theorems, replace the pilot, retain certified bisection, and include the fixed-point oscillation counterexample. Tasks 1 and 6--7 close registration, navigation, rendering, and site validation.
- Dependency safety: Chapter 9 precedes continuous functions; Chapter 11 precedes intermediate values; Chapter 12 reuses only second-part contraction mapping and third-part IVT. The plan prohibits derivatives, Newton's method, integrals, and general metric spaces.
- Verification: every chapter begins with a deliberately failing regression test, then runs focused checks; the final task runs the complete project verification. The plan contains no unresolved placeholders.
