# Part Two Infinite Processes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the complete, machine-validated 16-unit second part of the mathematical-analysis book, including the closed-interval contraction example and all reader-facing navigation.

**Architecture:** Extend the existing TOML registry and Quarto book in chapter order, then render each learning unit as a standalone QMD file using the existing eight-section contract. A focused Python module demonstrates certified contraction iteration; prose and regression tests keep mathematical boundaries—especially the absence of calculus and general metric-space machinery—enforceable.

**Tech Stack:** Quarto Book, QMD/Markdown, TOML, Python 3.12 standard library (`unittest`, `dataclasses`, `math`), existing project validators, GitHub Pages.

---

## Target file structure

```text
curriculum/units.toml                         # append 16 Part II contracts
_quarto.yml                                   # add Part II in unit order
book/part-02/chapter-05/u-02-05-01-*.qmd      # four Chapter 5 units
book/part-02/chapter-06/u-02-06-01-*.qmd      # three Chapter 6 units
book/part-02/chapter-07/u-02-07-01-*.qmd      # four Chapter 7 units
book/part-02/chapter-08/u-02-08-01-*.qmd      # five Chapter 8 units
src/mathbook_examples/fixed_point.py          # certified contraction iteration
tests/test_fixed_point.py                      # behavior and error-bound tests
tests/test_chapter_05.py                       # Chapter 5 regression contracts
tests/test_chapter_06.py                       # Chapter 6 regression contracts
tests/test_chapter_07.py                       # Chapter 7 regression contracts
tests/test_chapter_08.py                       # Chapter 8 regression contracts
```

## Task 1: Register the Part II navigation and unit contracts

**Files:**

- Modify: `_quarto.yml`
- Modify: `curriculum/units.toml`
- Create: `tests/test_chapter_05.py`
- Create: `tests/test_chapter_06.py`
- Create: `tests/test_chapter_07.py`
- Create: `tests/test_chapter_08.py`

- [ ] **Step 1: Write the failing registry/navigation tests.**

Each test file loads `curriculum/units.toml` with `tomllib`, builds `by_id`, and asserts its chapter's IDs, paths, titles, hours, and essential capabilities. The exact chapter totals and unit sequence are:

| Chapter | IDs in order | Theory + applied |
|---|---|---:|
| 05 | `u-02-05-01`, `u-02-05-02`, `u-02-05-03`, `u-02-05-04` | 6.50 + 1.50 |
| 06 | `u-02-06-01`, `u-02-06-02`, `u-02-06-03` | 5.50 + 1.00 |
| 07 | `u-02-07-01`, `u-02-07-02`, `u-02-07-03`, `u-02-07-04` | 7.00 + 1.00 |
| 08 | `u-02-08-01`, `u-02-08-02`, `u-02-08-03`, `u-02-08-04`, `u-02-08-05` | 7.00 + 2.50 |

Also assert that `_quarto.yml` contains the Part II heading and all sixteen repository-relative QMD paths, in exactly the order above. For Chapter 8, assert the source text contains the closed-interval contraction condition, `0\\le q<1`, both named counterexamples, `\\overline{\\mathbb R}`, tail supremum/infimum, and no `g'(x)` or `中值定理`.

- [ ] **Step 2: Run the new tests and verify failure.**

Run:

```bash
python3.12 -m unittest tests.test_chapter_05 tests.test_chapter_06 tests.test_chapter_07 tests.test_chapter_08 -v
```

Expected: failures because the Part II registry entries and QMD files do not exist.

- [ ] **Step 3: Append all sixteen TOML contracts and add Quarto navigation.**

Append the following IDs, titles, hours, and paths to `curriculum/units.toml`; each entry must include every existing required list field, concrete book prerequisites, external prerequisites, capability list, and 3–4 measurable learning goals.

| ID | Title | Hours | Path suffix |
|---|---|---:|---|
| u-02-05-01 | 数列怎样记录无限过程？ | 1.25 + 0.50 | `chapter-05/u-02-05-01-sequences.qmd` |
| u-02-05-02 | “最终任意接近”怎样写成定义？ | 1.75 + 0.25 | `chapter-05/u-02-05-02-epsilon-n.qmd` |
| u-02-05-03 | 不收敛与趋于无穷怎样区分？ | 1.75 + 0.25 | `chapter-05/u-02-05-03-divergence-infinity.qmd` |
| u-02-05-04 | 迭代数据何时值得相信？ | 1.75 + 0.50 | `chapter-05/u-02-05-04-iteration-evidence.qmd` |
| u-02-06-01 | 极限怎样通过代数运算传递？ | 2.00 + 0.25 | `chapter-06/u-02-06-01-limit-laws.qmd` |
| u-02-06-02 | 序关系怎样给出极限估计？ | 1.75 + 0.25 | `chapter-06/u-02-06-02-order-squeeze.qmd` |
| u-02-06-03 | 误差如何穿过一次迭代？ | 1.75 + 0.50 | `chapter-06/u-02-06-03-error-propagation.qmd` |
| u-02-07-01 | 单调数列为什么会有极限？ | 1.50 + 0.50 | `chapter-07/u-02-07-01-monotone-sequences.qmd` |
| u-02-07-02 | 递推的界与单调性怎样建立？ | 2.00 + 0.25 | `chapter-07/u-02-07-02-recursive-invariants.qmd` |
| u-02-07-03 | 区间套怎样保证唯一目标？ | 1.75 + 0.25 | `chapter-07/u-02-07-03-nested-intervals.qmd` |
| u-02-07-04 | 完备性怎样成为收敛准则？ | 1.75 + 0.00 | `chapter-07/u-02-07-04-completeness-criteria.qmd` |
| u-02-08-01 | 子列揭示了原数列的什么行为？ | 1.00 + 0.25 | `chapter-08/u-02-08-01-subsequences.qmd` |
| u-02-08-02 | 有界数列为何总能抽出收敛子列？ | 1.50 + 0.25 | `chapter-08/u-02-08-02-bolzano-weierstrass.qmd` |
| u-02-08-03 | Cauchy 条件怎样不预知极限而判断收敛？ | 1.75 + 0.50 | `chapter-08/u-02-08-03-cauchy-criterion.qmd` |
| u-02-08-04 | 严格压缩怎样保证迭代找到唯一根？ | 1.25 + 1.00 | `chapter-08/u-02-08-04-contraction-mapping.qmd` |
| u-02-08-05 | 上/下极限怎样总结所有尾部行为？ | 1.50 + 0.50 | `chapter-08/u-02-08-05-limsup-liminf.qmd` |

Use `chapter-04` as the only book prerequisite for `u-02-05-01`; make each later unit depend only on the minimum earlier Part II chapter(s) needed. Add every path under a `part: "第二部：数列极限与无限过程"` block between the existing Part I and Part III blocks in `_quarto.yml`.

- [ ] **Step 4: Run registry and navigation tests.**

Run:

```bash
python3.12 -m unittest tests.test_chapter_05 tests.test_chapter_06 tests.test_chapter_07 tests.test_chapter_08 -v
python3.12 scripts/check_units.py
```

Expected: still fails only on missing QMD files; all TOML schema and hours errors are absent.

- [ ] **Step 5: Commit the registry/navigation slice.**

```bash
git add _quarto.yml curriculum/units.toml tests/test_chapter_05.py tests/test_chapter_06.py tests/test_chapter_07.py tests/test_chapter_08.py
git commit -m "feat: register part two learning units"
```

## Task 2: Add the certified contraction-iteration example

**Files:**

- Create: `src/mathbook_examples/fixed_point.py`
- Create: `tests/test_fixed_point.py`

- [ ] **Step 1: Write failing behavior tests.**

Test `iterate_contraction` with `lambda x: 1 / (2 + x)`, `initial=0.0`, `contraction=0.25`, and `tolerance=1e-8`. Assert the result is within its error bound of `sqrt(2) - 1`, the bound is at most tolerance, and iteration count is positive. Add tests that reject a non-finite or non-positive tolerance, a contraction outside `[0, 1)`, a non-finite initial value, a non-finite iterate, and too-small `max_iterations`.

- [ ] **Step 2: Run the fixed-point test and verify failure.**

Run:

```bash
python3.12 -m unittest tests.test_fixed_point -v
```

Expected: `ModuleNotFoundError: No module named 'mathbook_examples.fixed_point'`.

- [ ] **Step 3: Implement the minimal certified iterator.**

Create `FixedPointResult(value: float, error_bound: float, iterations: int)` and implement this public contract:

```python
def iterate_contraction(
    function: Callable[[float], float],
    initial: float,
    *,
    contraction: float,
    tolerance: float = 1e-8,
    max_iterations: int = 100,
) -> FixedPointResult:
    """Iterate a caller-certified contraction until its a-posteriori bound passes."""
```

For consecutive iterates `previous`, `current`, use the valid a-posteriori bound

\[
\frac{q}{1-q}|x_n-x_{n-1}|.
\]

Reject invalid scalar inputs with the same finite/positive style as `bisect`; reject a non-finite function result; raise `RuntimeError("maximum iterations reached before tolerance")` when no certificate is obtained. The function does not and cannot verify that the caller's map is actually a contraction; its docstring and the QMD must state that `contraction` is a mathematical precondition, not empirical input.

- [ ] **Step 4: Run example tests.**

Run:

```bash
python3.12 -m unittest tests.test_fixed_point tests.test_bisection -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit the example slice.**

```bash
git add src/mathbook_examples/fixed_point.py tests/test_fixed_point.py
git commit -m "feat: add certified contraction iteration example"
```

## Task 3: Write Chapter 5—definitions, quantifiers, and trustworthy evidence

**Files:**

- Create: `book/part-02/chapter-05/u-02-05-01-sequences.qmd`
- Create: `book/part-02/chapter-05/u-02-05-02-epsilon-n.qmd`
- Create: `book/part-02/chapter-05/u-02-05-03-divergence-infinity.qmd`
- Create: `book/part-02/chapter-05/u-02-05-04-iteration-evidence.qmd`
- Modify: `tests/test_chapter_05.py`

- [ ] **Step 1: Add failing content assertions.**

Require all four stable H1 anchors and the eight standard H2 headings. Assert the chapter contains the finite limit quantifier order, the negation of convergence, both `a_n\\to+\\infty` and `a_n\\to-\\infty` definitions, and explicit wording that finite numerical output is not a proof. Assert it does not use `limsup`, `Cauchy`, or `连续函数` as an established theorem.

- [ ] **Step 2: Run the Chapter 5 tests and verify failure.**

Run `python3.12 -m unittest tests.test_chapter_05 -v`. Expected: missing content files and anchors.

- [ ] **Step 3: Write all four QMD learning units.**

Use the exact titles and hours in Task 1. Each unit must retain the project metadata callout, the eight required headings, stable anchors for definitions/theorems/examples/exercises, 3–6 answered exercises, and one complete representative solution. Establish the following mathematical sequence:

1. A sequence is a function on positive integers; distinguish a displayed finite prefix from its defining rule.
2. State and use the `forall epsilon > 0, exists N, forall n >= N` definition, including an explicit construction of `N` for a rational/geometric example.
3. Negate that definition correctly; define divergence and both directions of divergence to infinity with threshold `M`, without extended-real arithmetic.
4. Revisit the primary iteration and the two failure modes as data: finite tables formulate a conjecture only; neither small changes nor one small residual supplies a convergence certificate.

- [ ] **Step 4: Run Chapter 5 tests and full validators.**

Run:

```bash
python3.12 -m unittest tests.test_chapter_05 -v
python3.12 scripts/check_units.py
```

Expected: pass.

- [ ] **Step 5: Commit Chapter 5.**

```bash
git add book/part-02/chapter-05 tests/test_chapter_05.py
git commit -m "feat: add part two chapter five"
```

## Task 4: Write Chapter 6—limit laws, order, and error propagation

**Files:**

- Create: `book/part-02/chapter-06/u-02-06-01-limit-laws.qmd`
- Create: `book/part-02/chapter-06/u-02-06-02-order-squeeze.qmd`
- Create: `book/part-02/chapter-06/u-02-06-03-error-propagation.qmd`
- Modify: `tests/test_chapter_06.py`

- [ ] **Step 1: Add failing mathematical-boundary tests.**

Assert complete proofs/anchors for sum, product, quotient (with a nonzero limit and eventually nonzero denominator), order preservation, and the squeeze theorem. Assert the error-propagation unit derives the difference identity for `1 / (2 + x)` and contains no derivative notation or mean-value theorem.

- [ ] **Step 2: Run Chapter 6 tests and verify failure.**

Run `python3.12 -m unittest tests.test_chapter_06 -v`. Expected: missing content files and proof anchors.

- [ ] **Step 3: Write the three QMD units.**

The algebra-laws proof must expose the separate epsilon choices for addition, multiplication, and quotient rather than writing “obvious by laws.” The order unit must prove the limit inequalities and squeeze theorem before using them. The error unit must derive

\[
|g(x)-g(y)|=\frac{|x-y|}{(2+x)(2+y)}
\]

on `[0, 1]`, distinguish one-step propagation from a global convergence theorem, and connect it to the later strict contraction condition.

- [ ] **Step 4: Run Chapter 6 tests and validators.**

Run:

```bash
python3.12 -m unittest tests.test_chapter_06 -v
python3.12 scripts/check_units.py
```

Expected: pass.

- [ ] **Step 5: Commit Chapter 6.**

```bash
git add book/part-02/chapter-06 tests/test_chapter_06.py
git commit -m "feat: add part two chapter six"
```

## Task 5: Write Chapter 7—completeness-driven convergence certificates

**Files:**

- Create: `book/part-02/chapter-07/u-02-07-01-monotone-sequences.qmd`
- Create: `book/part-02/chapter-07/u-02-07-02-recursive-invariants.qmd`
- Create: `book/part-02/chapter-07/u-02-07-03-nested-intervals.qmd`
- Create: `book/part-02/chapter-07/u-02-07-04-completeness-criteria.qmd`
- Modify: `tests/test_chapter_07.py`

- [ ] **Step 1: Add failing proof-chain tests.**

Assert that the chapter proves the monotone bounded convergence theorem from the supremum/infimum principle, uses induction to prove a recursive invariant, proves the nested interval theorem with lengths tending to zero and uniqueness, and does not introduce a subsequence or Cauchy condition as an established criterion.

- [ ] **Step 2: Run Chapter 7 tests and verify failure.**

Run `python3.12 -m unittest tests.test_chapter_07 -v`. Expected: missing content files and theorem anchors.

- [ ] **Step 3: Write the four QMD units.**

Make the proof direction explicit: use `s = sup{a_n}` for an increasing bounded sequence, show no fixed gap below `s` can contain all later terms, and conclude the epsilon statement. The recursive unit must make induction hypotheses and bounds explicit. The interval unit must distinguish nonempty intersection from uniqueness: the latter requires lengths tending to zero. The final unit compares the three currently available certificates—monotone boundedness, invariant-controlled recursion, and nested intervals—without calling any of them a necessary-and-sufficient Cauchy criterion.

- [ ] **Step 4: Run Chapter 7 tests and validators.**

Run:

```bash
python3.12 -m unittest tests.test_chapter_07 -v
python3.12 scripts/check_units.py
```

Expected: pass.

- [ ] **Step 5: Commit Chapter 7.**

```bash
git add book/part-02/chapter-07 tests/test_chapter_07.py
git commit -m "feat: add part two chapter seven"
```

## Task 6: Write Chapter 8—subsequences, Cauchy, contraction, and tail limits

**Files:**

- Create: `book/part-02/chapter-08/u-02-08-01-subsequences.qmd`
- Create: `book/part-02/chapter-08/u-02-08-02-bolzano-weierstrass.qmd`
- Create: `book/part-02/chapter-08/u-02-08-03-cauchy-criterion.qmd`
- Create: `book/part-02/chapter-08/u-02-08-04-contraction-mapping.qmd`
- Create: `book/part-02/chapter-08/u-02-08-05-limsup-liminf.qmd`
- Modify: `tests/test_chapter_08.py`

- [ ] **Step 1: Add failing Chapter 8 theorem and scope tests.**

Require stable anchors and answered exercises in every unit. Assert: the BW proof uses nested intervals; the Cauchy criterion proves both directions; the contraction unit states `g:[a,b]\\to[a,b]`, `0\\le q<1`, uniqueness, and a-priori/a-posteriori error bounds; the limsup/liminf unit uses tail `sup_{k\\ge n}` and `inf_{k\\ge n}`, constructs extremal subsequences, and states the finite convergence iff criterion. Assert no `g'(x)`, `中值定理`, `开覆盖`, `紧致空间`, or a definition of general metric spaces appears.

- [ ] **Step 2: Run Chapter 8 tests and verify failure.**

Run `python3.12 -m unittest tests.test_chapter_08 -v`. Expected: missing content files and anchors.

- [ ] **Step 3: Write the five QMD units in proof dependency order.**

1. Define subsequences and inherited convergence; include only a brief, clearly labelled preview of real cluster points.
2. Prove Bolzano–Weierstrass by recursively selecting closed half-intervals that contain infinitely many terms, then extracting increasing indices.
3. Prove Cauchy necessity by the triangle inequality and sufficiency through boundedness plus BW and the contradiction that a Cauchy sequence cannot stay away from its convergent subsubsequence limit.
4. Prove the closed-interval contraction theorem using the Cauchy criterion. Use the primary map `1/(2+x)` on `[0,1]`; prove the `1/4` estimate algebraically; include the oscillating `1-x` and slow `x/(1+x)` counterexamples; document the Python result and state that `contraction` is caller-certified.
5. Introduce ordered extended reals only here, define tail suprema/infima, prove their monotonicity and extended limits, construct subsequences reaching `limsup`/`liminf`, and prove the finite equality criterion. Put the cluster-set facts and general Banach theorem in non-core forward-looking callouts only.

- [ ] **Step 4: Run Chapter 8 tests, examples, and validators.**

Run:

```bash
python3.12 -m unittest tests.test_chapter_08 tests.test_fixed_point -v
python3.12 scripts/check_units.py
```

Expected: pass.

- [ ] **Step 5: Commit Chapter 8.**

```bash
git add book/part-02/chapter-08 tests/test_chapter_08.py
git commit -m "feat: add part two chapter eight"
```

## Task 7: Render and verify the complete Part II release slice

**Files:**

- Modify if required by a failing check: only the exact files identified by the check

- [ ] **Step 1: Regenerate the curriculum map.**

Run:

```bash
python3.12 scripts/render_curriculum_map.py
```

Expected: `book/curriculum-map.qmd` reflects the 12 parts, 54 chapters, and all registered units without duplicate or stale Part II entries.

- [ ] **Step 2: Run the full test and metadata suite.**

Run:

```bash
make test
make check
```

Expected: all unit tests and outline/unit validators pass.

- [ ] **Step 3: Render and inspect the site contract.**

Run:

```bash
make render
python3.12 scripts/check_site.py
```

Expected: Quarto exits 0; every Part II navigation link resolves; the generated pages retain their stable anchors; no raw executable notebook fence is emitted.

- [ ] **Step 4: Commit generated curriculum-map and any narrow check fixes.**

```bash
git add book/curriculum-map.qmd
git commit -m "docs: publish part two curriculum map"
```

- [ ] **Step 5: Review the final change set.**

Run:

```bash
git status --short
git log --oneline --max-count=8
```

Expected: only the planned Part II commits are present; no generated `_site`, `.quarto`, or unrelated user changes are staged.

## Plan self-review

- Spec coverage: Tasks 1 and 7 cover navigation, machine contracts, rendering, and deployment checks; Tasks 3–6 cover all sixteen units and every required theorem boundary; Task 2 covers the tested Python demonstration.
- Scope: general metric spaces, derivative criteria, open-cover compactness, and formal convergence-order theory are excluded by explicit Chapter 8 tests and prose rules.
- Consistency: every QMD path, unit ID, title, hour allocation, and dependency order matches `docs/superpowers/specs/2026-07-19-part-02-infinite-processes-design.md`.
- Placeholder scan: no TBD/TODO or deferred implementation instruction remains.
