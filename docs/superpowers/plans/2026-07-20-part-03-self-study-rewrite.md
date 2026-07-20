# Part III Self-Study Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild Part III as a 20-unit, 40-hour core sequence plus a two-hour optional trigonometric-continuity appendix.

**Architecture:** Build on the version-2 content validator and completed Part II. Preserve all 13 published Part III URLs, add seven pages, make sequence compactness the Chapter 11 proof language, and keep contraction convergence owned by Part II.

**Tech Stack:** Quarto/QMD, TOML registries, Python 3.12 standard library, `unittest`, existing `mathbook_examples.bisection` and `mathbook_examples.fixed_point` modules.

---

## Preconditions and file map

Required starting state:

- Part II plan is complete and `make verify` passes with book totals 278 + 92 = 370.
- `scripts/check_units.py` supports `content_standard = 2`.
- `curriculum/parts-02-03-dependencies.md` matches the final Part III unit IDs below.

New core pages:

- `book/part-03/chapter-09/u-03-09-05-delta-workshop.qmd`
- `book/part-03/chapter-09/u-03-09-06-one-sided-limits.qmd`
- `book/part-03/chapter-09/u-03-09-07-infinite-limits.qmd`
- `book/part-03/chapter-09/u-03-09-08-limits-at-infinity.qmd`
- `book/part-03/chapter-10/u-03-10-04-elementary-continuity.qmd`
- `book/part-03/chapter-10/u-03-10-05-algebraic-continuity-bridge.qmd`
- `book/part-03/chapter-12/u-03-12-04-continuous-fixed-point.qmd`

New optional page:

- `book/appendices/trigonometric-continuity.qmd`

Final core hours:

| Chapter | Units | Theory | Applied |
|---|---:|---:|---:|
| 9 | 8 | 13.50 | 2.50 |
| 10 | 5 | 8.50 | 1.50 |
| 11 | 3 | 5.50 | 0.50 |
| 12 | 4 | 4.50 | 3.50 |

## Task 1: Rewrite Chapter 9 finite-limit foundations

**Files:**

- Modify: `tests/test_chapter_09.py`
- Modify: `curriculum/units.toml`
- Modify: `_quarto.yml`
- Rewrite: `book/part-03/chapter-09/u-03-09-01-local-neighborhoods.qmd`
- Rewrite: `book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.qmd`
- Create: `book/part-03/chapter-09/u-03-09-05-delta-workshop.qmd`

- [ ] **Step 1: Add the three-unit finite-foundation failing contract**

Require the first reading block `01, 02, 05` and its exact hours:

```python
expected_hours = {
    "u-03-09-01": (1.50, 0.50),
    "u-03-09-02": (2.00, 0.25),
    "u-03-09-05": (1.75, 0.25),
}
```

Assert subtotal 5.25 + 1.00 = 6.25.

Run: `python3.12 -m unittest tests.test_chapter_09 -v`

Expected: FAIL because unit 05 is absent and units 01–02 still have old hours.

- [ ] **Step 2: Rewrite the local-language unit**

Define domain-relative neighborhoods, deleted neighborhoods, one-sided neighborhoods and cluster points. Use examples where the domain has a gap or endpoint; explain why a cluster-point hypothesis prevents vacuous limits.

- [ ] **Step 3: Rewrite the finite-limit definition unit**

Give the full `epsilon-delta` definition, uniqueness proof, and basic linear examples. Separate `f(a)` from the limit and use a punctured-domain example.

- [ ] **Step 4: Write the delta workshop**

Teach backward estimation, auxiliary bounds such as `|x-a|<1`, minimum choices for delta, quadratic and rational examples, and the difference between discovering delta and presenting the forward proof.

- [ ] **Step 5: Register these three units as standard 2**

Preserve the existing URLs for 01 and 02, add 05 after 02, set exact hours and goals, and add all three to `_quarto.yml` in the final reading order.

- [ ] **Step 6: Run focused validation and commit**

Run: `python3.12 -m unittest tests.test_chapter_09 tests.test_units -v && python3.12 scripts/check_units.py`

Expected: the finite-foundation contract and all registry tests pass. Do not add the complete eight-unit contract until Task 2.

```bash
git add tests/test_chapter_09.py curriculum/units.toml _quarto.yml book/part-03/chapter-09
git commit -m "docs: rebuild finite function limits"
```

## Task 2: Complete Chapter 9 limit types and characterizations

**Files:**

- Create: `book/part-03/chapter-09/u-03-09-06-one-sided-limits.qmd`
- Create: `book/part-03/chapter-09/u-03-09-07-infinite-limits.qmd`
- Create: `book/part-03/chapter-09/u-03-09-08-limits-at-infinity.qmd`
- Rewrite: `book/part-03/chapter-09/u-03-09-03-function-limit-laws.qmd`
- Rewrite: `book/part-03/chapter-09/u-03-09-04-sequential-function-limits.qmd`
- Modify: `curriculum/units.toml`, `_quarto.yml`, `tests/test_chapter_09.py`

- [ ] **Step 1: Write the one-sided-limit unit**

Define left/right limits relative to the domain and prove that a two-sided finite limit exists exactly when both one-sided limits exist and agree. Include endpoint examples and a jump discontinuity preview.

- [ ] **Step 2: Write finite-point infinite limits**

Give quantified definitions for positive and negative infinity, one-sided variants, reciprocal examples, and explicit counterexamples. Do not define arithmetic such as `+infinity + (-infinity)`.

- [ ] **Step 3: Write limits at infinity**

Cover finite and infinite targets as `x` tends to positive or negative infinity. Include polynomial/rational order examples only through inequalities, not through later asymptotic-equivalence machinery.

- [ ] **Step 4: Rewrite laws and local properties**

Prove local boundedness, eventual sign, algebraic finite-limit laws, order/squeeze results and composition under the exact hypotheses. Cross-link to Part II rather than repeating sequence proofs verbatim.

- [ ] **Step 5: Rewrite Heine's sequential criterion**

Prove both directions for domain cluster points; in the converse construct a sequence recursively from the failure of `epsilon-delta`. Use the result for counterexamples but keep `epsilon-delta` as the primary definition.

- [ ] **Step 6: Register, publish, verify and commit Chapter 9**

Before verification, replace the finite-foundation-only test with the complete reading order `01, 02, 05, 06, 07, 08, 03, 04` and this exact contract:

```python
expected_hours = {
    "u-03-09-01": (1.50, 0.50),
    "u-03-09-02": (2.00, 0.25),
    "u-03-09-05": (1.75, 0.25),
    "u-03-09-06": (1.75, 0.25),
    "u-03-09-07": (1.75, 0.25),
    "u-03-09-08": (1.50, 0.50),
    "u-03-09-03": (1.75, 0.25),
    "u-03-09-04": (1.50, 0.25),
}
```

Assert totals 13.5 + 2.5 = 16.

Run: `python3.12 -m unittest tests.test_chapter_09 tests.test_units -v && python3.12 scripts/check_units.py`

Expected: all Chapter 9 and unit tests pass; eight standard-2 units total 16 hours.

```bash
git add tests/test_chapter_09.py curriculum/units.toml _quarto.yml book/part-03/chapter-09
git commit -m "docs: complete the function limit taxonomy"
```

## Task 3: Rewrite Chapter 10 and its required proof bridge

**Files:**

- Modify: `tests/test_chapter_10.py`
- Modify: `curriculum/units.toml`, `_quarto.yml`
- Rewrite: `book/part-03/chapter-10/u-03-10-01-epsilon-delta-continuity.qmd`
- Rewrite: `book/part-03/chapter-10/u-03-10-02-continuous-operations.qmd`
- Rewrite: `book/part-03/chapter-10/u-03-10-03-discontinuities-elementary-functions.qmd`
- Create: `book/part-03/chapter-10/u-03-10-04-elementary-continuity.qmd`
- Create: `book/part-03/chapter-10/u-03-10-05-algebraic-continuity-bridge.qmd`

- [ ] **Step 1: Add the five-unit failing contract**

Require `01=(1.75,.5)`, `02=(1.75,.25)`, `03=(1.5,.5)`, `04=(1.5,.25)`, `05=(2,0)`, totaling 8.5 + 1.5 = 10.

- [ ] **Step 2: Rewrite point and set continuity**

Connect continuity to a non-punctured local condition and to the function-limit criterion; prove the sequential characterization; distinguish isolated domain points and interval endpoints.

- [ ] **Step 3: Rewrite operation and composition closure**

Prove algebraic closure and composition with all domain conditions stated. Reuse Chapter 9 laws and do not introduce derivatives.

- [ ] **Step 4: Rewrite discontinuities**

Define removable, jump, infinite and oscillatory failure with one-sided evidence. Treat continuous extension as a theorem with a necessary and sufficient local-limit condition.

- [ ] **Step 5: Write the elementary-function contract unit**

List exactly which high-school properties are being cited for polynomial, rational, absolute-value, trigonometric, exponential and logarithmic functions. Link algebraic cases to unit 05 and trigonometric cases to the optional appendix; label exponential/logarithmic continuity as an explicit imported fact.

- [ ] **Step 6: Write the required algebraic proof bridge**

Derive continuity of constants and identity, then polynomials, rational functions off denominator zeros, absolute value, and finite compositions. This unit is core and counted; it must not construct exponential or logarithmic functions.

- [ ] **Step 7: Register, publish, verify and commit Chapter 10**

Run: `python3.12 -m unittest tests.test_chapter_10 tests.test_units -v && python3.12 scripts/check_units.py`

Expected: all focused checks pass.

```bash
git add tests/test_chapter_10.py curriculum/units.toml _quarto.yml book/part-03/chapter-10
git commit -m "docs: rebuild continuity and proof bridges"
```

## Task 4: Replace open-cover compactness with the sequence proof line

**Files:**

- Modify: `tests/test_chapter_11.py`
- Modify: `scripts/check_site.py`, `tests/test_site.py`
- Modify: `curriculum/units.toml`
- Rewrite: all three files under `book/part-03/chapter-11/`

- [ ] **Step 1: Change the regression test and confirm RED**

Require hours `01=(2,0)`, `02=(1.75,.25)`, `03=(1.75,.25)`. Replace open-cover markers with:

```python
self.assertIn("thm-u-03-11-01-sequential-compactness", compact)
self.assertIn("Bolzano--Weierstrass", compact)
self.assertNotIn("开覆盖", compact)
self.assertNotIn("有限子覆盖", compact)
```

Run: `python3.12 -m unittest tests.test_chapter_11 tests.test_site -v`

Expected: FAIL because the current unit uses open-cover compactness.

- [ ] **Step 2: Rewrite closed-interval sequential compactness**

State and prove that every sequence in `[a,b]` has a subsequence converging to a point of `[a,b]`, explicitly combining Part II Bolzano–Weierstrass with closedness of the interval. Put open-cover language only in an unproved forward-looking note.

- [ ] **Step 3: Rewrite boundedness and the extreme-value theorem**

Use contradiction sequences and sequential continuity. Prove both boundedness and attainment, and give failures on open or unbounded domains.

- [ ] **Step 4: Rewrite uniform continuity**

Define uniform continuity with quantifiers, prove Heine–Cantor by contradiction using paired sequences and a convergent subsequence, and contrast with pointwise continuity on an open interval.

- [ ] **Step 5: Update rendered anchor contracts**

Replace `def-u-03-11-01-open-cover`, `def-u-03-11-01-compactness`, and `thm-u-03-11-01-heine-borel` with the sequential-compactness anchor. Keep extreme-value and uniform-continuity anchors.

- [ ] **Step 6: Verify and commit Chapter 11**

Run: `python3.12 -m unittest tests.test_chapter_11 tests.test_site tests.test_units -v`

Expected: all focused checks pass and no Chapter 11 regression requires open-cover proofs.

```bash
git add tests/test_chapter_11.py tests/test_site.py scripts/check_site.py curriculum/units.toml book/part-03/chapter-11
git commit -m "docs: use sequence compactness in closed intervals"
```

## Task 5: Rewrite Chapter 12 existence and certificate comparison

**Files:**

- Modify: `tests/test_chapter_12.py`
- Modify: `curriculum/units.toml`, `_quarto.yml`
- Rewrite: `book/part-03/chapter-12/u-03-12-01-intermediate-value-theorem.qmd`
- Create: `book/part-03/chapter-12/u-03-12-04-continuous-fixed-point.qmd`
- Rewrite: `book/part-03/chapter-12/u-03-12-02-certified-bisection.qmd`
- Rewrite: `book/part-03/chapter-12/u-03-12-03-fixed-points-and-iteration.qmd`

- [ ] **Step 1: Add the four-unit failing contract**

Require reading order `01, 04, 02, 03` and the approved chapter total 4.5 + 3.5 = 8 with this exact contract:

```python
{
    "u-03-12-01": (1.50, 0.25),
    "u-03-12-04": (1.25, 0.50),
    "u-03-12-02": (1.00, 1.25),
    "u-03-12-03": (0.75, 1.50),
}
```

Run: `python3.12 -m unittest tests.test_chapter_12 -v`

Expected: FAIL only because unit 04/content is absent, not because totals disagree.

- [ ] **Step 2: Rewrite zero and intermediate values**

Prove the zero theorem by nested intervals or a supremum argument with every invariant stated, then derive the intermediate-value theorem by applying it to `f-y`. Separate existence from uniqueness.

- [ ] **Step 3: Write continuous fixed-point existence**

For a continuous `g:[a,b] -> [a,b]`, apply the intermediate-value theorem to `g(x)-x` and endpoint signs. Give multiple-fixed-point examples and state explicitly that existence gives neither uniqueness nor convergence of simple iteration.

- [ ] **Step 4: Rewrite certified bisection**

State the sign invariant, interval-length formula, midpoint error, step-count rule and stopping contract. Use only `mathbook_examples.bisection.bisect`; explain why residual size is not generally an error certificate.

- [ ] **Step 5: Rewrite the certificate-comparison unit**

Compare three contracts: IVT proves a root exists; bisection encloses a root with a width certificate; Part II contraction proves a unique fixed point and geometric convergence. Reuse links and code rather than re-proving contraction. Include cases where each method's assumptions fail.

- [ ] **Step 6: Verify code and chapter contracts**

Run: `python3.12 -m unittest tests.test_bisection tests.test_fixed_point tests.test_chapter_12 tests.test_units -v`

Expected: all focused tests pass; no Chapter 12 page proves the contraction theorem or mentions Newton/MVT/Taylor as an available tool.

- [ ] **Step 7: Commit Chapter 12**

```bash
git add tests/test_chapter_12.py curriculum/units.toml _quarto.yml book/part-03/chapter-12
git commit -m "docs: separate existence and convergence certificates"
```

## Task 6: Add the optional trigonometric-continuity appendix

**Files:**

- Create: `book/appendices/trigonometric-continuity.qmd`
- Modify: `_quarto.yml`
- Modify: `tests/test_project_structure.py`

- [ ] **Step 1: Add a failing appendix publication test**

Assert that `_quarto.yml` contains the appendix path and the file contains stable anchors for the sine inequality and sine/cosine continuity.

- [ ] **Step 2: Run and confirm RED**

Run: `python3.12 -m unittest tests.test_project_structure -v`

Expected: FAIL because the appendix does not exist.

- [ ] **Step 3: Write the optional appendix**

Prove the selected standard inequality used to control sine locally, derive continuity of sine and cosine from addition identities, and state the geometric prerequisite being used. Do not count the page in `curriculum/units.toml` or the core 40 hours.

- [ ] **Step 4: Publish under Quarto appendices and confirm GREEN**

Run: `python3.12 -m unittest tests.test_project_structure -v`

Expected: project-structure tests pass.

- [ ] **Step 5: Commit the appendix**

```bash
git add book/appendices/trigonometric-continuity.qmd _quarto.yml tests/test_project_structure.py
git commit -m "docs: add trigonometric continuity appendix"
```

## Task 7: Close the 40-hour Part III and 384-hour book baseline

**Files:**

- Modify: `curriculum/outline.toml`
- Modify: `scripts/check_outline.py`, `tests/test_outline.py`
- Modify: `tests/test_curriculum_map.py`
- Modify: `scripts/check_site.py`, `tests/test_site.py`
- Regenerate: `book/curriculum-map.qmd`

- [ ] **Step 1: Add failing final totals and page counts**

Require Part III `(32, 8)`, book `(290, 94, 384)`, 20 Part III registered links, and exactly 55 registered units: 14 Part I + 21 Part II + 20 Part III. The optional appendix is a published page but not a registered core unit.

- [ ] **Step 2: Run focused tests and confirm RED on old curriculum values**

Run: `python3.12 -m unittest tests.test_outline tests.test_curriculum_map tests.test_site -v`

Expected: FAIL on the old Part III hours/link count, not on arithmetic in the new test.

- [ ] **Step 3: Update outline contracts, render markers and curriculum map**

Change Part III and summed book values only; require anchors for finite limits, one-sided/infinite limits, Heine criterion, sequential compactness, uniform continuity, IVT, continuous fixed-point existence, bisection and certificate comparison.

- [ ] **Step 4: Run full verification**

```bash
python3.12 scripts/render_curriculum_map.py
DENO_DIR=/private/tmp/mathbook-quarto-deno make verify
```

Expected: all tests pass; outline reports 12 parts/54 chapters/290 theory + 94 application = 384; 55 core units are registered; Quarto renders the optional appendix; all internal links and required anchors pass.

- [ ] **Step 5: Perform the manual mathematical boundary audit**

Confirm: all four function-limit types are formal; `epsilon-delta` remains primary; Chapter 11 contains no open-cover proof; Chapter 12 does not re-prove contraction convergence; no derivative, MVT, Taylor, Newton or L'Hopital argument appears as an available theorem.

- [ ] **Step 6: Commit final Part III closure**

```bash
git add curriculum/outline.toml scripts/check_outline.py tests/test_outline.py tests/test_curriculum_map.py scripts/check_site.py tests/test_site.py book/curriculum-map.qmd
git commit -m "feat: close forty-hour part three"
```
