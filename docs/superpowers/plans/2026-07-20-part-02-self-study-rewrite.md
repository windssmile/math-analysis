# Part II Self-Study Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild Part II as a 21-unit, 42-hour self-study sequence with complete proofs, graded examples and exercises, and certified fixed-point computation.

**Architecture:** Preserve every published Part II URL, insert five new units, and let registry order—not numeric suffix—define reading order. Introduce an opt-in `content_standard = 2` validator so rewritten units satisfy the new book baseline while Part I remains eligible for a later audit.

**Tech Stack:** Quarto/QMD, TOML registries, Python 3.12 standard library, `unittest`, existing `mathbook_examples.fixed_point` module.

---

## File map and final unit order

Shared validation changes:

- Modify `scripts/check_units.py`: validate the version-2 unit structure.
- Modify `tests/test_units.py`: cover the opt-in structure and backward compatibility.

Curriculum and publishing changes:

- Modify `curriculum/units.toml`: set all Part II entries to `content_standard = 2`, revise hours and goals, and add five units.
- Modify `curriculum/outline.toml`: change Part II to theory 34 + application 8 and the book interim total to 278 + 92 = 370.
- Modify `scripts/check_outline.py` and `tests/test_outline.py`: encode the interim Part II contract.
- Modify `_quarto.yml`: publish the 21 units in pedagogical order.
- Modify `tests/test_curriculum_map.py`, `scripts/check_site.py`, and `tests/test_site.py`: require the new page count and stable theorem anchors.
- Regenerate `book/curriculum-map.qmd`.

New Part II pages:

- Create `book/part-02/chapter-05/u-02-05-05-limit-consequences.qmd`.
- Create `book/part-02/chapter-06/u-02-06-04-reciprocal-quotient.qmd`.
- Create `book/part-02/chapter-08/u-02-08-06-fixed-point-certificates.qmd`.
- Create `book/part-02/chapter-08/u-02-08-07-iteration-lab.qmd`.
- Create `book/part-02/chapter-08/u-02-08-08-limsup-subsequences.qmd`.

Final registry/navigation order and hours:

| Chapter | IDs in reading order | Theory | Applied |
|---|---|---:|---:|
| 5 | 01, 02, 05, 03, 04 | 8.00 | 2.00 |
| 6 | 01, 04, 02, 03 | 6.50 | 1.50 |
| 7 | 01, 02, 03, 04 | 7.00 | 1.00 |
| 8 | 01, 02, 03, 04, 06, 07, 05, 08 | 12.50 | 3.50 |

## Task 0: Freeze the shared theorem dependency and ID map

**Files:**

- Create: `curriculum/parts-02-03-dependencies.md`
- Modify: `tests/test_project_structure.py`

- [ ] **Step 1: Add a failing project-structure test**

Require the dependency file and the ownership markers `supremum -> monotone`, `monotone -> nested intervals`, `nested intervals -> Bolzano-Weierstrass`, `Bolzano-Weierstrass -> Cauchy`, `Part II owns contraction convergence`, and `Part III owns continuous existence`.

```python
def test_parts_two_three_dependency_map_is_frozen(self) -> None:
    path = ROOT / "curriculum" / "parts-02-03-dependencies.md"
    content = path.read_text(encoding="utf-8")
    for marker in (
        "supremum -> monotone",
        "monotone -> nested intervals",
        "nested intervals -> Bolzano-Weierstrass",
        "Bolzano-Weierstrass -> Cauchy",
        "Part II owns contraction convergence",
        "Part III owns continuous existence",
    ):
        self.assertIn(marker, content)
```

- [ ] **Step 2: Run the test and confirm RED**

Run: `python3.12 -m unittest tests.test_project_structure -v`

Expected: FAIL because the dependency file does not exist.

- [ ] **Step 3: Write the dependency and migration map**

Record every final Part II and Part III unit ID in reading order, the theorem edges from the approved design, the content owner for contraction/continuity/existence/bisection, and the statement that all 29 existing URLs remain published so no migration page is needed in this implementation.

- [ ] **Step 4: Run the test and confirm GREEN**

Run: `python3.12 -m unittest tests.test_project_structure -v`

Expected: all project-structure tests pass.

- [ ] **Step 5: Commit the frozen map**

```bash
git add curriculum/parts-02-03-dependencies.md tests/test_project_structure.py
git commit -m "docs: freeze parts two and three dependencies"
```

## Task 1: Add the version-2 content validator

**Files:**

- Modify: `scripts/check_units.py`
- Modify: `tests/test_units.py`

- [ ] **Step 1: Add failing fixture tests for the new standard**

Add a `content_standard = 2` unit fixture and assert that it fails when it has fewer than two anchored examples, two immediate-answer callouts, five anchored exercises, five collapsed exercise answers, or the final boundary section. Keep the current pilot fixture without `content_standard` and assert that it still validates.

```python
def test_v2_requires_examples_checks_exercises_and_boundaries(self) -> None:
    data = copy.deepcopy(self.load_registry())
    self.pilot_unit(data)["content_standard"] = 2
    errors = self.validate_with_content(data, VALID_CONTENT)
    self.assertIn(f"{UNIT_ID} v2 content must contain at least 2 anchored examples", errors)
    self.assertIn(f"{UNIT_ID} v2 content must contain at least 5 anchored exercises", errors)
    self.assertIn(f"{UNIT_ID} content file is missing heading: ## 常见误区与后续", errors)
```

- [ ] **Step 2: Run the focused test and confirm RED**

Run: `python3.12 -m unittest tests.test_units.UnitValidationTests.test_v2_requires_examples_checks_exercises_and_boundaries -v`

Expected: FAIL because `content_standard` has no special validation.

- [ ] **Step 3: Implement the opt-in validator**

In `scripts/check_units.py`, accept only standards 1 and 2, treating a missing field as 1. For version 2, count only non-fenced lines and require:

```python
V2_REQUIRED_HEADINGS = REQUIRED_QMD_HEADINGS + ("## 常见误区与后续",)
V2_MINIMUMS = {
    "anchored examples": (r"^### .+\{#ex-", 2),
    "anchored exercises": (r"^### .+\{#pr-", 5),
    "collapsed answers": (r'^::: \{\.callout-note collapse="true"\}', 7),
}
```

Validate `content_standard` as a strict integer, pass it into `_validate_content_file`, and emit stable unit-ID-prefixed error messages.

- [ ] **Step 4: Run all registry tests and confirm GREEN**

Run: `python3.12 -m unittest tests.test_units -v`

Expected: all `tests.test_units` tests pass, including the unchanged version-1 fixture.

- [ ] **Step 5: Commit the validator foundation**

```bash
git add scripts/check_units.py tests/test_units.py
git commit -m "test: enforce self-study unit structure"
```

## Task 2: Rewrite Chapter 5

**Files:**

- Modify: `tests/test_chapter_05.py`
- Modify: `curriculum/units.toml`
- Modify: `_quarto.yml`
- Rewrite: `book/part-02/chapter-05/u-02-05-01-sequences.qmd`
- Rewrite: `book/part-02/chapter-05/u-02-05-02-epsilon-n.qmd`
- Create: `book/part-02/chapter-05/u-02-05-05-limit-consequences.qmd`
- Rewrite: `book/part-02/chapter-05/u-02-05-03-divergence-infinity.qmd`
- Rewrite: `book/part-02/chapter-05/u-02-05-04-iteration-evidence.qmd`

- [ ] **Step 1: Replace the Chapter 5 registry expectation and confirm RED**

Use this exact hour contract in `tests/test_chapter_05.py`:

```python
expected_hours = {
    "u-02-05-01": (1.50, 0.50),
    "u-02-05-02": (2.00, 0.25),
    "u-02-05-05": (2.00, 0.25),
    "u-02-05-03": (1.50, 0.25),
    "u-02-05-04": (1.00, 0.75),
}
self.assertEqual(sum(by_id[key]["theory_hours"] for key in expected_hours), 8.0)
self.assertEqual(sum(by_id[key]["applied_hours"] for key in expected_hours), 2.0)
```

Run: `python3.12 -m unittest tests.test_chapter_05 -v`

Expected: FAIL because `u-02-05-05` is absent and hours are old.

- [ ] **Step 2: Rewrite unit 01**

Define sequences as functions on positive integers; distinguish a finite table from an infinite rule; compare explicit and recursive definitions; establish tails and eventual statements without introducing subsequences. Use the main iteration (x_{n+1}=1/(2+x_n)), include at least two examples, and answer five exercises fully.

- [ ] **Step 3: Rewrite unit 02**

State the `epsilon-N` definition with exact quantifier order. Prove (1/n\to0), (c/n^p\to0) for (p>0) using the Archimedean property already available, and show why a single numerical tolerance does not prove convergence.

- [ ] **Step 4: Write unit 05 as the proof-and-consequences unit**

Teach backward design of `N(epsilon)`. Give complete proofs of uniqueness, convergence implying boundedness, and preservation of strict eventual inequalities with an explicit margin. Include a quantifier-negation counterexample and do not use limit laws from Chapter 6.

- [ ] **Step 5: Rewrite unit 03**

Give formal definitions of convergence to positive and negative infinity, negate finite convergence correctly, and separate oscillation, unboundedness, and divergence to infinity. Mention extended-real notation but do not perform extended-real arithmetic.

- [ ] **Step 6: Rewrite unit 04**

Use finite iteration tables to form conjectures; compare the main contraction candidate, (x_{n+1}=1-x_n), and (x_{n+1}=x_n/(1+x_n)). State explicitly that plots and small increments are evidence, not convergence certificates.

- [ ] **Step 7: Register and publish the five units**

Set `content_standard = 2`, the exact hours above, explicit prerequisites and goals, and order entries/pages as `01, 02, 05, 03, 04` in both `curriculum/units.toml` and `_quarto.yml`.

- [ ] **Step 8: Run Chapter 5 and registry verification**

Run: `python3.12 -m unittest tests.test_chapter_05 tests.test_units -v && python3.12 scripts/check_units.py`

Expected: all focused tests pass and `unit registry valid` is printed.

- [ ] **Step 9: Commit Chapter 5**

```bash
git add tests/test_chapter_05.py curriculum/units.toml _quarto.yml book/part-02/chapter-05
git commit -m "docs: rewrite sequence limit foundations"
```

## Task 3: Rewrite Chapter 6

**Files:**

- Modify: `tests/test_chapter_06.py`
- Modify: `curriculum/units.toml`
- Modify: `_quarto.yml`
- Rewrite: `book/part-02/chapter-06/u-02-06-01-limit-laws.qmd`
- Create: `book/part-02/chapter-06/u-02-06-04-reciprocal-quotient.qmd`
- Rewrite: `book/part-02/chapter-06/u-02-06-02-order-squeeze.qmd`
- Rewrite: `book/part-02/chapter-06/u-02-06-03-error-propagation.qmd`

- [ ] **Step 1: Make the four-unit hour test fail**

Require exact hours `01=(2,.25)`, `04=(1.75,.25)`, `02=(1.75,.25)`, `03=(1,.75)` and chapter totals 6.5 + 1.5 = 8.

Run: `python3.12 -m unittest tests.test_chapter_06 -v`

Expected: FAIL because unit 04 is absent.

- [ ] **Step 2: Rewrite unit 01**

Prove constant, sum, difference, scalar-multiple and product laws from `epsilon-N`; isolate the bounded-tail lemma used by the product proof. Include proof-selection examples rather than only limit calculations.

- [ ] **Step 3: Write unit 04**

Prove eventual separation from zero, the reciprocal law and the quotient law. Include counterexamples when the denominator limit is zero and prohibit indeterminate-form algebra.

- [ ] **Step 4: Rewrite unit 02**

Prove non-strict order preservation, strict eventual sign under a positive limit, and the squeeze theorem. Distinguish which strict inequalities survive and which do not.

- [ ] **Step 5: Rewrite unit 03**

Develop algebraic error decomposition and Lipschitz estimates without derivatives. Use (g(x)=1/(2+x)) only for one-step propagation; explicitly defer iteration convergence to Chapter 8.

- [ ] **Step 6: Register, publish and verify Chapter 6**

Set standard 2 and the exact order `01, 04, 02, 03`. Run:

`python3.12 -m unittest tests.test_chapter_06 tests.test_units -v && python3.12 scripts/check_units.py`

Expected: all focused checks pass.

- [ ] **Step 7: Commit Chapter 6**

```bash
git add tests/test_chapter_06.py curriculum/units.toml _quarto.yml book/part-02/chapter-06
git commit -m "docs: rebuild sequence limit laws"
```

## Task 4: Rewrite Chapter 7

**Files:**

- Modify: `tests/test_chapter_07.py`
- Modify: `curriculum/units.toml`
- Rewrite: all four files under `book/part-02/chapter-07/`

- [ ] **Step 1: Update and fail the hour/proof-boundary test**

Require exact hours `01=(2,.25)`, `02=(1.75,.5)`, `03=(1.75,.25)`, `04=(1.5,0)` and totals 7 + 1 = 8. Require the dependency phrases `确界原理`, `单调有界`, and `区间套`, while continuing to forbid a Chapter 7 proof of Cauchy completeness.

- [ ] **Step 2: Rewrite the monotone-convergence unit**

Prove increasing-bounded and decreasing-bounded cases from supremum/infimum; expose where nonemptiness and boundedness enter; include an unbounded monotone counterexample.

- [ ] **Step 3: Rewrite the recursive-invariants unit**

Use induction to prove an invariant interval and monotonicity before solving a fixed-point equation. Include examples where the candidate limit exists algebraically but the sequence oscillates.

- [ ] **Step 4: Rewrite the nested-interval unit**

Prove nonempty intersection and uniqueness when lengths tend to zero. Include counterexamples for missing nesting and missing shrinking length.

- [ ] **Step 5: Rewrite the completeness-map unit**

Build the explicit proof dependency map from the supremum principle through monotone convergence and nested intervals; compare when to use each certificate without claiming every bounded sequence converges.

- [ ] **Step 6: Register, verify and commit Chapter 7**

Run: `python3.12 -m unittest tests.test_chapter_07 tests.test_units -v && python3.12 scripts/check_units.py`

Expected: all focused checks pass.

```bash
git add tests/test_chapter_07.py curriculum/units.toml book/part-02/chapter-07
git commit -m "docs: expand completeness proof methods"
```

## Task 5: Rewrite Chapter 8 theory

**Files:**

- Modify: `tests/test_chapter_08.py`
- Modify: `curriculum/units.toml`
- Modify: `_quarto.yml`
- Rewrite: `book/part-02/chapter-08/u-02-08-01-subsequences.qmd`
- Rewrite: `book/part-02/chapter-08/u-02-08-02-bolzano-weierstrass.qmd`
- Rewrite: `book/part-02/chapter-08/u-02-08-03-cauchy-criterion.qmd`
- Rewrite: `book/part-02/chapter-08/u-02-08-04-contraction-mapping.qmd`
- Create: `book/part-02/chapter-08/u-02-08-06-fixed-point-certificates.qmd`
- Rewrite: `book/part-02/chapter-08/u-02-08-05-limsup-liminf.qmd`
- Create: `book/part-02/chapter-08/u-02-08-08-limsup-subsequences.qmd`

- [ ] **Step 1: Add the eight-unit failing contract**

Require hours `01=(1.5,.25)`, `02=(1.75,.25)`, `03=(1.75,.25)`, `04=(2,.25)`, `06=(1.5,.5)`, `07=(.75,1.25)`, `05=(1.75,.25)`, `08=(1.5,.5)`, totaling 12.5 + 3.5 = 16. Unit 07 is created in Task 6 but belongs in this final contract.

- [ ] **Step 2: Rewrite subsequences and cluster points**

Prove that subsequences of a convergent sequence share its limit; construct subsequences recursively; define real cluster points without introducing general topology.

- [ ] **Step 3: Rewrite Bolzano–Weierstrass**

Give the nested-interval proof, including the infinite-choice invariant and construction of strictly increasing indices. Prove the extracted limit belongs to the original closed interval.

- [ ] **Step 4: Rewrite the Cauchy criterion**

Prove convergence implies Cauchy; prove Cauchy implies bounded; use Bolzano–Weierstrass for a convergent subsequence and then prove the whole sequence converges to the same limit.

- [ ] **Step 5: Rewrite the contraction theorem**

On a real closed interval, prove invariant iterates, the geometric increment estimate, Cauchy convergence, fixed-point existence, uniqueness, and prior/posterior error bounds. Do not use derivatives or a general metric-space theorem.

- [ ] **Step 6: Write the certificate unit**

Separate: proof that `g([a,b])` is contained in `[a,b]`; proof of a contraction constant; selection of an initial value; prior and posterior stopping bounds; and the fact that a small observed increment alone is not a certificate.

- [ ] **Step 7: Rewrite the first limsup/liminf unit**

Define extended reals only as an ordered completion for this purpose. Define tail suprema/infima, prove their monotonicity, and define `limsup`/`liminf` including unbounded cases.

- [ ] **Step 8: Write the realizing-subsequence unit**

Construct strictly indexed subsequences tending to finite and infinite upper/lower limits; prove the finite convergence criterion; include alternating, dense-cluster, and unbounded examples without claiming the cluster set is an interval.

## Task 6: Build the iteration laboratory

**Files:**

- Modify: `tests/test_fixed_point.py`
- Modify: `src/mathbook_examples/fixed_point.py`
- Create: `book/part-02/chapter-08/u-02-08-07-iteration-lab.qmd`

- [ ] **Step 1: Add failing behavioral tests for trace output**

Add a separate trace helper rather than changing the certified result contract:

```python
def test_iteration_trace_preserves_requested_length(self) -> None:
    trace = iterate_trace(lambda x: 1 / (2 + x), 0.0, steps=4)
    self.assertEqual(len(trace), 5)
    self.assertEqual(trace[0], 0.0)
```

Also reject non-integer/non-positive `steps` and non-finite iterates.

- [ ] **Step 2: Run the focused test and confirm RED**

Run: `python3.12 -m unittest tests.test_fixed_point -v`

Expected: FAIL because `iterate_trace` does not exist.

- [ ] **Step 3: Implement the minimal trace helper**

```python
def iterate_trace(function: Callable[[float], float], initial: float, *, steps: int) -> tuple[float, ...]:
    _require_finite(initial, "initial value")
    if type(steps) is not int or steps <= 0:
        raise ValueError("steps must be a positive integer")
    values = [initial]
    for iteration in range(1, steps + 1):
        value = function(values[-1])
        if not isfinite(value):
            raise ValueError(f"function value at iteration {iteration} must be finite")
        values.append(value)
    return tuple(values)
```

- [ ] **Step 4: Write the laboratory unit**

Use the shared helper to compare the main contraction, the two-cycle (1-x), and (x/(1+x)). Plot or tabulate evidence, then state which theorem hypotheses have and have not been proved. Do not infer a contraction factor from samples.

- [ ] **Step 5: Run behavioral and chapter tests**

Run: `python3.12 -m unittest tests.test_fixed_point tests.test_chapter_08 tests.test_units -v`

Expected: all focused tests pass.

- [ ] **Step 6: Commit Chapter 8**

```bash
git add tests/test_chapter_08.py tests/test_fixed_point.py src/mathbook_examples/fixed_point.py curriculum/units.toml _quarto.yml book/part-02/chapter-08
git commit -m "docs: complete sequence compactness and iteration"
```

## Task 7: Close Part II curriculum and publishing contracts

**Files:**

- Modify: `curriculum/outline.toml`
- Modify: `scripts/check_outline.py`
- Modify: `tests/test_outline.py`
- Modify: `tests/test_curriculum_map.py`
- Modify: `scripts/check_site.py`
- Modify: `tests/test_site.py`
- Regenerate: `book/curriculum-map.qmd`

- [ ] **Step 1: Write failing outline and map totals**

Require Part II `(34, 8)`, book interim totals `(278, 92, 370)`, 21 Part II curriculum-map links, and stable rendered anchors for the Cauchy theorem, contraction theorem, tail-supremum definition, and finite limsup criterion.

- [ ] **Step 2: Run the focused tests and confirm RED**

Run: `python3.12 -m unittest tests.test_outline tests.test_curriculum_map tests.test_site -v`

Expected: FAIL on old hours, old link count, or missing anchor contracts.

- [ ] **Step 3: Update outline and validator constants**

Change only Part II and the summed book totals. Do not change Part III in this plan.

- [ ] **Step 4: Regenerate and run the complete verification**

Run:

```bash
python3.12 scripts/render_curriculum_map.py
DENO_DIR=/private/tmp/mathbook-quarto-deno make verify
```

Expected: all unit tests pass; outline reports 12 parts/54 chapters/278 theory + 92 application = 370; 14 Part I + 21 Part II + the unchanged 13 Part III units produce 48 registered units; Quarto renders and site validation passes.

- [ ] **Step 5: Audit the Part II writing baseline manually**

For every Part II unit, record that it has at least two anchored examples, two immediate checks, five anchored exercises, seven collapsed answers, a boundary section, and no forbidden derivative/mean-value/Taylor dependency.

- [ ] **Step 6: Commit the Part II closure**

```bash
git add curriculum/outline.toml scripts/check_outline.py tests/test_outline.py tests/test_curriculum_map.py scripts/check_site.py tests/test_site.py book/curriculum-map.qmd
git commit -m "feat: close forty-two-hour part two"
```
